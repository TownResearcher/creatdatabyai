import os
import re
import json
import time
from typing import Dict, List, Any, Optional
from tqdm import tqdm
import google.generativeai as genai
import spacy
import jieba
from transformers import BertTokenizer, BertModel
import torch
from pathlib import Path

from config import (
    GEMINI_API_KEY, PROXY, MODEL_CONFIG, STRUCTURE_PROMPT,
    GENERATION_CONFIG, SAFETY_SETTINGS, NLP_CONFIG, FILE_CONFIG,
    RETRY_CONFIG, OUTPUT_CONFIG
)

class NovelProcessor:
    def __init__(self):
        """初始化小说处理器"""
        self._setup_environment()
        self._init_nlp_tools()
        self._init_output_dirs()
        
    def _setup_environment(self):
        """设置环境和API"""
        # 设置代理
        if PROXY:
            os.environ["HTTPS_PROXY"] = PROXY["https"]
            print("\n当前代理设置:")
            print(f"HTTPS_PROXY: {PROXY['https']}")
        
        # 初始化 Gemini 客户端
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=MODEL_CONFIG["model_name"],
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS
        )
        
        # 测试 API 连接
        self._test_api_connection()
    
    def _init_nlp_tools(self):
        """初始化NLP工具"""
        print("\n初始化NLP工具...")
        
        # 初始化 spaCy
        if NLP_CONFIG["use_spacy"]:
            try:
                self.nlp = spacy.load(NLP_CONFIG["spacy_model"])
                print("✓ SpaCy 加载成功")
            except Exception as e:
                print(f"× SpaCy 加载失败: {str(e)}")
                self.nlp = None
        
        # 初始化 BERT
        if NLP_CONFIG["use_transformers"]:
            try:
                self.tokenizer = BertTokenizer.from_pretrained(NLP_CONFIG["bert_model"])
                self.bert_model = BertModel.from_pretrained(NLP_CONFIG["bert_model"])
                print("✓ BERT 模型加载成功")
            except Exception as e:
                print(f"× BERT 模型加载失败: {str(e)}")
                self.tokenizer = None
                self.bert_model = None
        
        # 初始化结巴分词
        if NLP_CONFIG["use_jieba"]:
            try:
                jieba.initialize()
                print("✓ 结巴分词初始化成功")
            except Exception as e:
                print(f"× 结巴分词初始化失败: {str(e)}")
    
    def _init_output_dirs(self):
        """初始化输出目录"""
        base_dir = Path(OUTPUT_CONFIG["output_structure"]["raw"]).parent
        for dir_name in OUTPUT_CONFIG["output_structure"].values():
            dir_path = base_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _test_api_connection(self):
        """测试API连接"""
        print("正在测试 Gemini API 连接...")
        try:
            response = self.model.generate_content("你好")
            print(f"模型响应: {response.text}")
            print("Gemini API 连接测试成功！\n")
            print(f"\n当前使用的模型：{MODEL_CONFIG['model_name']}")
        except Exception as e:
            print(f"API 连接测试失败: {str(e)}")
            raise

    def read_novel(self, file_path: str) -> str:
        """读取小说文件"""
        print("\n开始读取文件...")
        
        # 备份原始文件
        if OUTPUT_CONFIG["backup_original"]:
            self._backup_file(file_path)
        
        # 尝试不同编码读取文件
        content = None
        with tqdm(total=len(FILE_CONFIG["encodings"]), desc="尝试解码") as pbar:
            for encoding in FILE_CONFIG["encodings"]:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                        print(f"\n使用 {encoding} 编码成功读取文件")
                        break
                except UnicodeDecodeError:
                    pass
                finally:
                    pbar.update(1)
        
        if content is None:
            # 使用二进制模式读取并忽略错误
            with open(file_path, 'r', encoding='gb18030', errors='ignore') as f:
                content = f.read()
                print("\n使用 gb18030 编码（忽略错误）读取文件")
        
        return content

    def preprocess_text(self, text: str) -> str:
        """预处理文本"""
        print("\n开始文本预处理...")
        
        with tqdm(total=6, desc="预处理文本") as pbar:
            # 1. 清理特殊字符和广告
            for pattern in FILE_CONFIG["clean_patterns"]:
                text = re.sub(pattern, '', text)
            pbar.update(1)
            
            # 2. 使用结巴分词进行分句
            if NLP_CONFIG["use_jieba"]:
                sentences = []
                for chunk in jieba.cut(text):
                    if len(chunk) >= NLP_CONFIG["min_sentence_length"]:
                        sentences.append(chunk)
                text = "。".join(sentences)
            pbar.update(1)
            
            # 3. 使用 spaCy 进行实体识别和句法分析
            if self.nlp:
                doc = self.nlp(text)
                # 保留有意义的句子
                text = " ".join([sent.text for sent in doc.sents 
                               if len(sent.text) >= NLP_CONFIG["min_sentence_length"]])
            pbar.update(1)
            
            # 4. 规范化标点符号
            for splitter in FILE_CONFIG["sentence_splitters"]:
                text = text.replace(splitter * 2, splitter)
            pbar.update(1)
            
            # 5. 处理段落
            paragraphs = []
            current_para = []
            for line in text.split('\n'):
                line = line.strip()
                if line:
                    current_para.append(line)
                elif current_para:
                    paragraphs.append(''.join(current_para))
                    current_para = []
            if current_para:
                paragraphs.append(''.join(current_para))
            text = '\n'.join(paragraphs)
            pbar.update(1)
            
            # 6. 移除重复内容
            seen_paragraphs = set()
            unique_paragraphs = []
            for para in paragraphs:
                if len(para) > 50:  # 只检查长段落的重复
                    if para not in seen_paragraphs:
                        seen_paragraphs.add(para)
                        unique_paragraphs.append(para)
                else:
                    unique_paragraphs.append(para)
            text = '\n'.join(unique_paragraphs)
            pbar.update(1)
        
        # 保存预处理结果
        if OUTPUT_CONFIG["save_intermediate"]:
            self._save_intermediate("preprocessed.txt", text)
        
        return text.strip()

    def split_into_chunks(self, text: str) -> List[str]:
        """将文本分割成小块"""
        chunks = []
        current_pos = 0
        text_length = len(text)
        
        with tqdm(total=text_length, desc="分块处理") as pbar:
            while current_pos < text_length:
                # 获取当前块的结束位置
                end_pos = min(current_pos + FILE_CONFIG["chunk_size"], text_length)
                
                # 如果不是最后一块，尝试在句子边界处分割
                if end_pos < text_length:
                    # 在最大长度范围内查找最后一个句号
                    last_period = text[current_pos:end_pos].rfind('。')
                    if last_period != -1:
                        end_pos = current_pos + last_period + 1
                
                # 添加当前块
                chunk = text[current_pos:end_pos]
                if chunk.strip():  # 只添加非空块
                    chunks.append(chunk)
                
                # 更新位置，考虑重叠
                current_pos = max(current_pos + 1, end_pos - FILE_CONFIG["overlap"])
                pbar.update(end_pos - current_pos)
        
        return chunks

    def analyze_structure(self, chunk: str) -> Dict[str, Any]:
        """分析文本结构"""
        retry_count = 0
        while retry_count < RETRY_CONFIG["max_retries"]:
            try:
                # 添加请求间隔，避免频率限制
                if retry_count > 0:
                    delay = min(
                        RETRY_CONFIG["retry_delay"] * (RETRY_CONFIG["retry_backoff"] ** retry_count),
                        RETRY_CONFIG["max_retry_delay"]
                    )
                    print(f"\n等待 {delay} 秒后重试...")
                    time.sleep(delay)
                
                # 使用 BERT 进行情感分析
                if self.tokenizer and self.bert_model:
                    emotions = self._analyze_emotions(chunk)
                else:
                    emotions = {"primary_emotion": "未知", "emotional_changes": []}
                
                # 构建提示词
                prompt = f"{STRUCTURE_PROMPT}\n\n请分析以下文本：\n{chunk}"
                
                # 发送请求
                response = self.model.generate_content(
                    prompt,
                    generation_config=GENERATION_CONFIG,
                    safety_settings=SAFETY_SETTINGS
                )
                
                if not response or not hasattr(response, 'text'):
                    print(f"\n第 {retry_count + 1} 次尝试：无效响应")
                    retry_count += 1
                    continue
                
                # 处理响应
                result = self._process_api_response(response.text, emotions)
                if result:
                    return result
                
                retry_count += 1
                
            except Exception as e:
                error_type = type(e).__name__
                if error_type in RETRY_CONFIG["retry_exceptions"]:
                    print(f"\n遇到可重试的错误 ({error_type}): {str(e)}")
                    retry_count += 1
                    continue
                else:
                    print(f"\n遇到不可重试的错误: {str(e)}")
                    raise
        
        # 所有重试都失败后返回默认结构
        return self._get_default_structure()

    def _analyze_emotions(self, text: str) -> Dict[str, Any]:
        """使用BERT分析情感"""
        try:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                outputs = self.bert_model(**inputs)
            
            # 使用最后一层的[CLS]标记的输出作为特征
            features = outputs.last_hidden_state[:, 0, :]
            
            # 这里可以添加更复杂的情感分类逻辑
            # 当前仅返回一个示例结果
            return {
                "primary_emotion": "neutral",
                "emotional_changes": []
            }
        except Exception as e:
            print(f"情感分析失败: {str(e)}")
            return {
                "primary_emotion": "unknown",
                "emotional_changes": []
            }

    def _process_api_response(self, response_text: str, emotions: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """处理API响应"""
        try:
            # 提取JSON部分
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                
                # 解析JSON
                result = json.loads(json_str)
                
                # 合并情感分析结果
                if "emotions" in result:
                    result["emotions"].update(emotions)
                
                print("成功解析响应")
                return result
                
        except json.JSONDecodeError as e:
            print(f"\nJSON 解析错误: {str(e)}")
            print(f"原始响应: {response_text[:200]}...")
        
        return None

    def _get_default_structure(self) -> Dict[str, Any]:
        """获取默认的结构"""
        return {
            "act": "处理失败",
            "scene": "无法解析",
            "key_events": ["文本处理失败"],
            "characters": {
                "main_characters": [],
                "supporting_characters": []
            },
            "relationships": [],
            "emotions": {
                "primary_emotion": "unknown",
                "emotional_changes": []
            },
            "themes": ["无法识别"],
            "narrative_techniques": ["无法识别"]
        }

    def _backup_file(self, file_path: str):
        """备份原始文件"""
        try:
            source = Path(file_path)
            backup_dir = Path(OUTPUT_CONFIG["output_structure"]["backup"])
            backup_path = backup_dir / f"{source.stem}_backup{source.suffix}"
            
            import shutil
            shutil.copy2(source, backup_path)
            print(f"已备份原始文件到: {backup_path}")
        except Exception as e:
            print(f"备份文件失败: {str(e)}")

    def _save_intermediate(self, filename: str, content: str):
        """保存中间结果"""
        try:
            save_path = Path(OUTPUT_CONFIG["output_structure"]["processed"]) / filename
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"已保存中间结果到: {save_path}")
        except Exception as e:
            print(f"保存中间结果失败: {str(e)}")

    def process_novel(self, file_path: str) -> List[Dict[str, Any]]:
        """处理小说文件"""
        print("\n开始处理小说...")
        
        # 读取文件
        content = self.read_novel(file_path)
        
        # 预处理文本
        processed_text = self.preprocess_text(content)
        
        # 分割成块
        chunks = self.split_into_chunks(processed_text)
        print(f"\n文本已分割为 {len(chunks)} 个块")
        
        # 分析每个块
        results = []
        with tqdm(total=len(chunks), desc="分析进度") as pbar:
            for i, chunk in enumerate(chunks, 1):
                print(f"\n处理第 {i}/{len(chunks)} 个文本块")
                result = self.analyze_structure(chunk)
                results.append(result)
                pbar.update(1)
        
        # 保存结果
        if OUTPUT_CONFIG["save_format"] == "json":
            output_path = Path(OUTPUT_CONFIG["output_structure"]["analysis"]) / "analysis_results.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"\n分析结果已保存到: {output_path}")
        
        return results 
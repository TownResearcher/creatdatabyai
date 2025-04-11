import os
from dotenv import load_dotenv
import google.generativeai as genai

# API配置
GEMINI_API_KEY = "AIzaSyCSl55htF7SsJXnz9LYKOk3hqRcIHYauKs"  # Gemini API 密钥

# 网络配置
TIMEOUT = 120  # 超时时间（秒）
MAX_RETRIES = 3  # 最大重试次数
USE_PROXY = True  # 是否使用代理
PROXY = {
    "https": "http://127.0.0.1:7890"
}

# NLP配置
NLP_CONFIG = {
    "use_spacy": True,           # 是否使用 spaCy 进行文本分析
    "use_transformers": True,    # 是否使用 transformers 进行情感分析
    "use_jieba": True,          # 是否使用结巴分词
    "spacy_model": "zh_core_web_sm",  # spaCy 中文模型
    "bert_model": "bert-base-chinese",  # BERT 中文模型
    "min_sentence_length": 10,   # 最小句子长度
    "max_sentence_length": 500,  # 最大句子长度
}

# 处理配置
CHUNK_SIZE = 2000  # 调整为更合理的块大小
MAX_TOKENS = 8000  # 最大token数
OUTPUT_DIR = "output"  # 输出目录

# 模型配置
MODEL_CONFIG = {
    "model_name": "models/gemini-2.5-pro-preview-03-25",
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# 安全设置
SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

# 生成配置
GENERATION_CONFIG = {
    "temperature": MODEL_CONFIG["temperature"],
    "top_p": MODEL_CONFIG["top_p"],
    "top_k": MODEL_CONFIG["top_k"],
    "max_output_tokens": MODEL_CONFIG["max_output_tokens"],
}

# 结构分析配置
STRUCTURE_PROMPT = """
请对以下文本片段进行深度结构分析，返回严格的JSON格式：

{
    "act": "string",           # 当前叙事阶段/章节
    "scene": "string",         # 场景描述（100字以内）
    "key_events": [           # 关键事件列表
        "string",
        "string"
    ],
    "characters": {           # 人物分析
        "main_characters": [  # 主要人物
            {
                "name": "string",
                "role": "string",
                "description": "string"
            }
        ],
        "supporting_characters": []  # 配角
    },
    "relationships": [        # 人物关系
        {
            "character1": "string",
            "character2": "string",
            "relationship_type": "string",
            "description": "string"
        }
    ],
    "emotions": {            # 情感分析
        "primary_emotion": "string",
        "emotional_changes": [
            {
                "character": "string",
                "from": "string",
                "to": "string",
                "trigger": "string"
            }
        ]
    },
    "themes": [              # 主题元素
        "string"
    ],
    "narrative_techniques": [ # 叙事手法
        "string"
    ]
}

分析要求：
1. 保持客观准确
2. 结构完整，字段齐全
3. 严格遵守 JSON 格式
4. 重点关注人物关系和情感变化
5. 识别叙事技巧和主题元素
"""

# 文件处理配置
FILE_CONFIG = {
    "chunk_size": 2000,     # 调整块大小
    "overlap": 200,         # 增加重叠以保持上下文
    "min_chunk_size": 500,  # 最小块大小
    "encodings": [          # 文件编码尝试顺序
        'utf-8',
        'gbk',
        'gb2312',
        'gb18030',
        'big5',
        'utf-16',
        'utf-32',
        'ascii'
    ],
    "sentence_splitters": ['。', '！', '？', '…'],  # 句子分割符
    "paragraph_splitters": ['\n', '\r\n', '\r'],   # 段落分割符
    "clean_patterns": [      # 清理模式
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',  # URLs
        r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # 邮箱
        r'第\s*[0-9一二三四五六七八九十百千万]+\s*[章节回]',  # 章节标记
        r'本章完|未完待续|感谢.{0,20}打赏|欢迎.{0,20}收藏',   # 网文常见标记
        r'手机用户请到.{0,50}阅读|最新章节请百度搜索',        # 广告文本
    ]
}

# 重试配置
RETRY_CONFIG = {
    "max_retries": 3,          # 最大重试次数
    "retry_delay": 5,          # 初始重试延迟（秒）
    "max_retry_delay": 30,     # 最大重试延迟（秒）
    "retry_backoff": 2,        # 重试延迟倍数
    "max_chunk_retries": 5,    # 单个文本块最大重试次数
    "retry_exceptions": [      # 需要重试的异常
        "ConnectionError",
        "Timeout",
        "APIError",
        "RateLimitError"
    ]
}

# 输出配置
OUTPUT_CONFIG = {
    "save_format": "json",     # 输出格式
    "save_intermediate": True, # 是否保存中间结果
    "compress_output": True,   # 是否压缩输出
    "backup_original": True,   # 是否备份原始文件
    "output_structure": {      # 输出目录结构
        "raw": "raw",         # 原始文件
        "processed": "processed", # 处理后的文件
        "analysis": "analysis",   # 分析结果
        "backup": "backup"        # 备份
    }
} 
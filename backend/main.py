import os
import json
import google.generativeai as genai
from novel_processor import NovelProcessor
from config import OUTPUT_DIR
import requests

# 设置代理
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'

def test_gemini_connection():
    """测试 Gemini API 连接"""
    print("正在测试 Gemini API 连接...")
    try:
        print("当前代理设置:")
        print(f"HTTP_PROXY: {os.environ.get('HTTP_PROXY')}")
        print(f"HTTPS_PROXY: {os.environ.get('HTTPS_PROXY')}")
        
        # 配置 API 密钥
        genai.configure(api_key='AIzaSyCSl55htF7SsJXnz9LYKOk3hqRcIHYauKs')
        
        # 创建一个简单的模型调用
        model = genai.GenerativeModel('gemini-2.0-pro-exp')  # 使用新的模型名称
        response = model.generate_content("你好！")
        print(f"模型响应: {response.text}")
        
        print("Gemini API 连接测试成功！")
        return True
    except Exception as e:
        print(f"\nGemini API 连接测试失败")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        if hasattr(e, 'response'):
            print(f"响应状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
        return False

def ensure_output_dir():
    """确保输出目录存在"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def save_results(results: list, output_file: str):
    """保存处理结果"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

def main():
    # 测试 API 连接
    if not test_gemini_connection():
        print("API 连接失败，请检查网络设置")
        return

    # 确保输出目录存在
    ensure_output_dir()
    
    # 初始化处理器
    processor = NovelProcessor()
    
    # 处理小说
    input_file = "../No.001 姻缘.txt"
    output_file = os.path.join(OUTPUT_DIR, "姻缘_分析结果.json")
    
    print("开始处理小说...")
    results = processor.process_novel(input_file)
    
    # 保存结果
    save_results(results, output_file)
    print(f"处理完成，结果已保存至: {output_file}")

if __name__ == "__main__":
    main() 
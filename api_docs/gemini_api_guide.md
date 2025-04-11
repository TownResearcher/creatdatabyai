# Gemini API 使用指南

## 环境准备

### 安装依赖
```bash
pip install -q -U google-generativeai
```

### 导入必要的包
```python
import google.generativeai as genai
from dotenv import load_dotenv
import os
```

### 配置API密钥
```python
# 从.env文件加载环境变量
load_dotenv()

# 配置API密钥
GOOGLE_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
```

## 基本用法

### 1. 文本生成
```python
# 初始化模型
model = genai.GenerativeModel('gemini-1.5-pro')

# 生成文本
response = model.generate_content("请用一句话解释什么是人工智能？")
print(response.text)
```

### 2. 流式响应
```python
# 使用流式响应
response = model.generate_content("请用一句话解释什么是人工智能？", stream=True)
for chunk in response:
    print(chunk.text)
    print("_"*80)
```

### 3. 多轮对话
```python
# 初始化聊天
chat = model.start_chat(history=[])

# 发送消息
response = chat.send_message("请用一句话解释什么是人工智能？")
print(response.text)

# 继续对话
response = chat.send_message("能详细解释一下吗？")
print(response.text)
```

### 4. 图片分析
```python
import PIL.Image

# 加载图片
img = PIL.Image.open('image.jpg')

# 分析图片
response = model.generate_content(["请描述这张图片的内容", img])
print(response.text)
```

## 高级功能

### 1. 安全设置
```python
response = model.generate_content(
    "你的提示",
    safety_settings={
        'HARASSMENT': 'block_none',
        'HATE_SPEECH': 'block_none'
    }
)
```

### 2. 生成配置
```python
response = model.generate_content(
    "你的提示",
    generation_config=genai.types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=1000,
        temperature=0.7
    )
)
```

### 3. 嵌入功能
```python
# 生成文本嵌入
result = genai.embed_content(
    model="models/embedding-001",
    content="你的文本",
    task_type="retrieval_document",
    title="文档标题"
)

print(result['embedding'])
```

## 错误处理

```python
try:
    response = model.generate_content("你的提示")
    print(response.text)
except Exception as e:
    print(f"发生错误: {str(e)}")
```

## 最佳实践

1. 使用环境变量存储API密钥
2. 适当设置temperature参数（0-1之间）
3. 使用流式响应处理长文本
4. 实现错误处理和重试机制
5. 注意API调用频率限制

## 注意事项

1. API密钥安全：永远不要将API密钥直接写在代码中
2. 错误处理：始终实现适当的错误处理机制
3. 速率限制：注意API的调用频率限制
4. 成本控制：监控API使用情况，避免意外费用
5. 数据安全：不要发送敏感信息到API 
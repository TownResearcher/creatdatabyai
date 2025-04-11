# API密钥管理指南

## 配置文件说明

本项目使用`.env`文件来管理所有AI服务的API密钥。这种方式可以：
1. 保护您的敏感信息不被泄露
2. 方便在不同环境中切换不同的API密钥
3. 避免将密钥直接硬编码在代码中

## 使用方法

1. 复制`.env`文件中的所有内容
2. 将每个`your_xxx_api_key_here`替换为实际的API密钥
3. 确保`.env`文件已被添加到`.gitignore`中，避免意外提交到版本控制系统

## 支持的API服务

- OpenAI API
- Anthropic API
- Google API
- Mistral API
- Cohere API
- Google Gemini API

## 安全提示

- 永远不要将`.env`文件提交到代码仓库
- 定期更换API密钥
- 使用最小权限原则，只授予必要的API访问权限
- 考虑使用API密钥轮换机制

## 环境变量使用示例

在Python中使用示例：
```python
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')
``` 
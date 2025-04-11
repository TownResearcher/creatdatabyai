from flask import Flask
from dotenv import load_dotenv
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()
logger.info("环境变量已加载")

app = Flask(__name__)

@app.route('/')
def home():
    logger.info("访问首页")
    return 'Novel to Script Data Generator is running!'

@app.route('/health')
def health():
    logger.info("健康检查")
    return 'OK'

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    logger.info(f"应用启动在端口 {port}")
    app.run(host='0.0.0.0', port=port) 
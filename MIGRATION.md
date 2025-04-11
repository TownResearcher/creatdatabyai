# 项目迁移指南

## 需要迁移的文件

### 源代码
- 所有`.py`文件
- 所有`.md`文档文件
- 所有配置文件（包括.env）

### 配置文件
- docker-compose.yml
- Dockerfile
- .dockerignore
- requirements.txt
- .env
- 其他配置文件

### 文档
- README.md
- 其他文档文件

## 不需要迁移的文件
- __pycache__目录
- 虚拟环境目录
- IDE配置文件
- 系统临时文件

## 迁移步骤

1. 克隆仓库
```bash
git clone <repository_url>
```

2. 启动服务
```bash
docker-compose up --build
```

## 验证迁移
1. 检查所有服务是否正常运行
2. 验证API是否可访问
3. 检查日志是否有错误 
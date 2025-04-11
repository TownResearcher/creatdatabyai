# Novel-to-Script Data Generator

一个用于将小说转换为剧本数据集的AI工具。

## 项目结构

```
.
├── backend/           # 后端代码
├── frontend/         # 前端代码
├── api_docs/         # API文档
├── docs/             # 项目文档
├── tests/            # 测试文件
│   └── samples/      # 测试样本
├── scripts/          # 脚本文件
├── .env.example      # 环境变量模板
├── .gitignore        # Git忽略文件
├── Dockerfile        # Docker配置
├── docker-compose.yml # Docker编排
├── main.py           # 主程序入口
└── requirements.txt  # 依赖列表
```

## 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/TownResearcher/creatdatabyai.git
cd creatdatabyai
```

2. 配置环境：
```bash
cp .env.example .env
# 编辑.env文件填入您的配置
```

3. 启动服务：
```bash
docker-compose up --build -d
```

4. 访问应用：
打开浏览器访问 http://localhost:8000

## 文档

- [系统架构](docs/system_architecture.md)
- [迁移指南](docs/MIGRATION_CHECKLIST.md)
- [API文档](api_docs/README.md)

## 开发指南

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行测试：
```bash
python -m pytest tests/
```

3. 提交更改：
```bash
./scripts/sync_changes.bat
```

## 许可证

MIT License 
# 项目迁移清单

## 1. 项目文件（按重要性排序）

### 核心文件
- [ ] main.py（Flask应用主文件）
- [ ] requirements.txt（Python依赖）
- [ ] Dockerfile（Docker构建文件）
- [ ] docker-compose.yml（Docker编排文件）
- [ ] .env（环境变量配置）

### 配置文件
- [ ] .dockerignore
- [ ] .gitignore

### 文档文件
- [ ] README.md
- [ ] requirements.md
- [ ] system_architecture.md
- [ ] MIGRATION_CHECKLIST.md

### 数据文件
- [ ] No.001 姻缘.txt
- [ ] 其他小说文件

## 2. Docker相关

### 镜像
- [ ] creatdatabyai-app（导出或重新构建）

### 容器配置
- [ ] novel_to_script容器配置
- [ ] 端口映射（8000:8000）
- [ ] 环境变量

## 3. 迁移步骤

1. 准备工作
   ```bash
   # 在源电脑上
   mkdir project_backup
   cd project_backup
   ```

2. 复制所有项目文件
   ```bash
   # 复制整个项目目录
   cp -r /path/to/CreatDataByAI/* ./
   ```

3. 导出Docker镜像（可选）
   ```bash
   # 保存Docker镜像
   docker save creatdatabyai-app > creatdatabyai-app.tar
   ```

4. 在新电脑上

   a. 安装必要软件：
   - Docker Desktop
   - Git（可选）

   b. 复制项目文件：
   - 复制整个project_backup目录到新电脑

   c. 导入Docker镜像（如果已导出）：
   ```bash
   docker load < creatdatabyai-app.tar
   ```

   d. 或直接重新构建（推荐）：
   ```bash
   cd /path/to/project
   docker-compose up --build
   ```

## 4. 验证清单

- [ ] 所有文件已复制
- [ ] Docker已正确安装
- [ ] 项目可以成功构建
- [ ] 容器可以正常启动
- [ ] 应用可以访问（http://localhost:8000）
- [ ] 环境变量正确配置

## 5. 故障排查

如果遇到问题：
1. 检查Docker日志
2. 确认端口是否被占用
3. 验证环境变量
4. 检查网络连接 
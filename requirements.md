# 小说转剧本数据集生成工具需求文档

## 1. 项目概述

开发一个AI工具，用于将百万字量级的小说转化为可用于模型微调的数据集，特别针对剧本创作能力的训练。

## 2. 核心功能需求

### 2.1 数据预处理
- 支持多种格式的小说输入（txt, epub, pdf等）
- 自动识别章节结构
- 提取关键文本信息
- 处理百万字级别的文本数据
- 支持批量处理多部小说

### 2.2 剧本结构分析
- 自动识别并提取十二幕结构
- 分析并标记外部冲突
- 分析并标记内部冲突
- 提取人物关系网络
- 识别关键情节转折点

### 2.3 标签系统
- 灵感标签生成
  - 主题标签
  - 风格标签
  - 情感标签
  - 场景标签
- 冲突标签生成
  - 外部冲突标签
  - 内部冲突标签
  - 人物关系冲突标签

### 2.4 剧本元素提取
- 核心概念提取
- 人物小传生成
- 场景描述提取
- 对话内容提取
- 情感变化分析

### 2.5 数据集生成
- 结构化数据输出
- 支持多种格式（JSON, CSV等）
- 包含元数据信息
- 支持数据清洗和验证
- 支持数据增强

## 3. 十二幕结构详细需求

### 3.1 第一幕：设定
1. 普通世界
   - 已知的世界、现状、设定

2. 冒险的召唤
   - 一个改变命运的事件、行动的召唤、催化剂

3. 拒绝召唤
   - 关键时刻、分离、犹豫不决、挣扎、遇见导师、门槛、守护者

4. 跨越第一个门槛
   - 无法回头的时刻、进入第二幕、门槛、觉醒、坚定目标

### 3.2 第二幕：对抗
5. 考验、盟友与敌人
   - 鲸腹阶段、趣味与冒险、阻力与挣扎、障碍、次要角色和关系开始发展

6. 中点
   - 半途的震撼时刻、顿悟瞬间、故事的重大转折，提升冲突的强度

7. 接近最深洞穴
   - 面临重大选择或牺牲，敌人逼近、准备、挑战与诱惑、阻力与挣扎、复杂情况、更高的赌注

8. 进入最深洞穴
   - 似乎无法战胜对手或解决问题，考验、危机、灵魂黑夜、顿悟、关键战斗、自我死亡、跌入谷底、重大变化、顿悟

### 3.3 第三幕：解决
9. 觉醒时刻
   - 死里逃生，觉醒、反弹、牺牲

10. 高潮事件
    - 夺取宝剑、转变、夺取奖赏、进入第三幕

11. 带着智慧归来
    - 问题得到解决、转变与归来、归途、新生活、新的状态、后续影响

12. 结局
    - 为故事画上句号，给观众留下余韵，呼应故事的主题或开头

## 4. 技术需求

### 4.1 数据处理
- 高性能文本处理能力
- 大规模数据存储方案
- 分布式处理支持
- 数据备份机制

### 4.2 AI模型需求
- 自然语言处理能力
- 文本分类能力
- 情感分析能力
- 关系提取能力
- 场景识别能力

### 4.3 系统架构
- 模块化设计
- 可扩展架构
- 高可用性设计
- 性能优化方案

## 5. 输出格式

### 5.1 数据集结构
```json
{
  "novel_id": "string",
  "title": "string",
  "author": "string",
  "structure": {
    "act1": {
      "ordinary_world": {...},
      "call_to_adventure": {...},
      "refusal": {...},
      "crossing_threshold": {...}
    },
    "act2": {...},
    "act3": {...}
  },
  "characters": [...],
  "conflicts": [...],
  "themes": [...],
  "metadata": {...}
}
```

### 5.2 数据字段
- 原始文本
- 结构化数据
- 标签数据
- 元数据
- 关系数据

## 6. 非功能需求

### 6.1 性能需求
- 处理速度：每小时至少处理100万字
- 响应时间：单次分析不超过5分钟
- 并发处理：支持多部小说同时处理

### 6.2 安全需求
- 数据加密存储
- 访问权限控制
- 操作日志记录
- 数据备份机制

### 6.3 可用性需求
- 用户友好界面
- 操作简单直观
- 错误提示清晰
- 进度显示明确

## 7. 后续优化方向

### 7.1 功能扩展
- 支持更多输入格式
- 增加更多分析维度
- 提供可视化分析
- 支持自定义标签

### 7.2 性能优化
- 优化处理算法
- 提升处理速度
- 减少资源占用
- 优化存储方案 
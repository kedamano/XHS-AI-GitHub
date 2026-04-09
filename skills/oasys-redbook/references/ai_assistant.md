# OASYS AI 助手功能说明

## 概述

OASYS 集成智谱AI大模型（GLM-4），通过右下角悬浮按钮提供智能办公助手服务。

## 接入配置

```properties
# application.properties
zhipu.api.key=your_zhipu_api_key
zhipu.api.url=https://open.bigmodel.cn/api/paas/v4/chat/completions
zhipu.model=glm-4-flash  # 免费快速模型
```

**获取密钥**: https://open.bigmodel.cn/

## 核心功能

| 功能 | 说明 |
|------|------|
| 智能问答 | 解答OA系统使用问题 |
| 流程指导 | 协助发起请假/报销/出差申请 |
| 日程建议 | 任务安排和日程管理建议 |
| 功能导航 | 快速定位系统功能模块 |
| 办公辅助 | 协助撰写邮件、公告等内容 |

## 使用方法

1. 登录系统后，点击右下角悬浮AI助手按钮
2. 在对话框中输入问题
3. AI助手即时响应

## 快捷功能入口

- 请假申请
- 考勤查询
- 发送邮件
- 功能介绍

# OASYS 技术栈详解

## 后端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| Spring Boot | 1.5.6.RELEASE | 核心框架，快速构建应用 |
| Spring Data JPA | 1.5.6.RELEASE | 数据持久层，简化数据库操作 |
| MyBatis | 1.3.0 | SQL映射框架，复杂查询首选 |
| MySQL | 8.0.26 | 关系型数据库 |
| 智谱AI SDK | 2.0.2 | GLM-4 大模型接入 |
| Maven | 3.x | 项目构建和依赖管理 |

## 前端技术

| 技术 | 版本 | 说明 |
|------|------|------|
| FreeMarker | - | 模板引擎，动静结合 |
| Bootstrap | 3.3.7 | 响应式UI框架 |
| jQuery | 1.11.3 | JavaScript函数库 |
| KindEditor | 4.1.10 | 富文本编辑器 |
| My97 DatePicker | 4.8 | 日期选择组件 |

## 项目结构

```
cn.gson.oasys/
├── controller/          # 控制器层（REST API）
│   ├── ai/            # AI助手
│   ├── user/          # 用户管理
│   ├── attendce/      # 考勤
│   ├── process/       # 流程审批
│   ├── task/          # 任务
│   ├── mail/          # 邮件
│   ├── daymanage/     # 日程
│   ├── address/       # 通讯录
│   ├── file/          # 文件
│   ├── chat/          # 讨论区
│   ├── note/          # 公告
│   └── system/        # 系统管理
├── model/              # 数据模型
│   ├── entity/         # JPA实体类
│   └── dao/            # 数据访问接口
├── services/           # 业务逻辑层
├── common/             # 公共组件（工具类/拦截器）
└── OasysApplication.java  # 启动类
```

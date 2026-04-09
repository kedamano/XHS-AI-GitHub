#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OASYS 小红书配图 - 批量生成器
一次生成 6 张核心配图，覆盖项目全貌
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tech_draw import gen_card

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TOTAL = 6

# 图1: 项目介绍 + 核心亮点（蓝黑科技）
gen_card({
    "theme_idx": 0,
    "page_num": 1, "total": TOTAL,
    "kicker": "智能 OA 办公自动化",
    "title": "OASYS\n新一代 OA 系统",
    "subtitle": "集成智谱AI · Spring Boot + MySQL · 10大核心模块",
    "sections": [
        {"type": "label", "text": " 项目亮点"},
        {
            "type": "bullet",
            "items": [
                "AI 智能助手 - 集成 GLM-4 大模型，智能问答 + 流程指导",
                "全场景覆盖 - 考勤/审批/任务/邮件/日程/通讯录/文件",
                "灵活流程引擎 - 请假/报销/出差/转正/离职多模板",
                "现代化 UI - Bootstrap 响应式设计，多端适配",
                "完善权限体系 - 角色配置 + 动态菜单 + 操作日志",
            ]
        },
        {"type": "divider"},
        {
            "type": "text",
            "lines": [
                "GitHub: github.com/kedamano/oasys",
                "技术栈: Spring Boot 1.5.6 | Java 8 | MySQL 8.0 | 智谱AI",
            ]
        },
    ],
    "footer_tags": "#OASYS  #OA办公  #SpringBoot  #智谱AI  #开源项目",
}, os.path.join(OUTPUT_DIR, "01_intro.jpg"))

# 图2: 快速开始（紫黑极客）
gen_card({
    "theme_idx": 1,
    "page_num": 2, "total": TOTAL,
    "kicker": "5分钟快速部署",
    "title": "快速开始\n部署 OASYS",
    "sections": [
        {
            "type": "kv",
            "items": [
                ["Step 1  ", "git clone + cd oasys"],
                ["Step 2  ", "mysql -u root -p < oasys.sql"],
                ["Step 3  ", "配置 application.properties"],
                ["Step 4  ", "mvn spring-boot:run"],
                ["Step 5  ", "浏览器访问 localhost:8088/logins"],
            ]
        },
        {"type": "divider"},
        {"type": "label", "text": " 初始账号"},
        {
            "type": "kv",
            "items": [
                ["soli / 123456  ", "管理员账号"],
                ["test / test    ", "测试账号"],
            ]
        },
        {"type": "divider"},
        {
            "type": "code",
            "lines": [
                "# 关键配置项",
                "spring.datasource.password=your_password",
                "zhipu.api.key=your_zhipu_api_key",
                "file.root.path=D:/oasys/resources/static/file",
            ]
        },
    ],
    "footer_tags": "#OASYS部署  #SpringBoot  #MySQL  #新手教程",
}, os.path.join(OUTPUT_DIR, "02_quickstart.jpg"))

# 图3: AI 助手（青黑赛博）
gen_card({
    "theme_idx": 4,
    "page_num": 3, "total": TOTAL,
    "kicker": "GLM-4 大模型加持",
    "title": "AI 智能助手\n人机协同办公",
    "sections": [
        {"type": "label", "text": " 核心功能"},
        {
            "type": "bullet",
            "items": [
                "智能问答 - 解答 OA 系统使用问题，新手秒上手",
                "流程指导 - 协助发起请假/报销/出差等申请",
                "日程建议 - 提供任务安排和日程管理建议",
                "功能导航 - 快速定位系统功能模块",
                "办公辅助 - 协助撰写邮件、公告等内容",
            ]
        },
        {"type": "divider"},
        {"type": "label", "text": " 快捷入口"},
        {
            "type": "kv",
            "items": [
                ["快捷1  ", "请假申请  快捷2  考勤查询"],
                ["快捷3  ", "发送邮件  快捷4  功能介绍"],
            ]
        },
        {
            "type": "code",
            "lines": [
                "# 获取智谱AI密钥",
                "访问 open.bigmodel.cn 注册",
                "在 application.properties 配置:",
                "zhipu.api.key=your_api_key",
            ]
        },
    ],
    "footer_tags": "#AI助手  #智谱AI  #GLM4  #OASYS  #办公自动化",
}, os.path.join(OUTPUT_DIR, "03_ai.jpg"))

# 图4: 核心模块（橙黑工业）
gen_card({
    "theme_idx": 3,
    "page_num": 4, "total": TOTAL,
    "kicker": "10大核心模块",
    "title": "功能模块\n全景一览",
    "sections": [
        {
            "type": "kv",
            "items": [
                ["用户管理    ", "个人信息/密码/登录日志"],
                ["考勤管理    ", "签到签退/考勤统计/请假加班"],
                ["流程管理    ", "费用报销/出差/转正/离职"],
                ["任务管理    ", "任务分配/跟踪/统计/监控"],
                ["邮件管理    ", "邮件收发/模板/分类管理"],
                ["日程管理    ", "日程安排/提醒/日历视图"],
                ["通讯录      ", "内外部联系人/分组管理"],
                ["文件管理    ", "上传下载/共享/版本控制"],
                ["讨论区      ", "内部交流/话题讨论/投票"],
                ["公告通知    ", "系统公告/个人通知/提醒"],
            ]
        },
        {"type": "divider"},
        {
            "type": "text",
            "lines": [
                "系统管理: 角色权限/菜单配置/操作日志/系统监控",
            ]
        },
    ],
    "footer_tags": "#OA系统  #功能模块  #办公软件  #企业管理",
}, os.path.join(OUTPUT_DIR, "04_modules.jpg"))

# 图5: 技术架构（绿黑终端）
gen_card({
    "theme_idx": 2,
    "page_num": 5, "total": TOTAL,
    "kicker": "技术架构详解",
    "title": "技术栈\n与传统方案对比",
    "sections": [
        {"type": "label", "text": " 后端技术栈"},
        {
            "type": "kv",
            "items": [
                ["Spring Boot   ", "1.5.6.RELEASE  核心框架"],
                ["Spring Data JPA", "1.5.6.RELEASE  数据持久层"],
                ["MyBatis       ", "1.3.0  SQL映射框架"],
                ["MySQL         ", "8.0.26  数据库"],
                ["智谱AI SDK    ", "2.0.2  GLM-4 大模型"],
            ]
        },
        {"type": "label", "text": " 前端技术栈"},
        {
            "type": "kv",
            "items": [
                ["FreeMarker    ", "模板引擎"],
                ["Bootstrap     ", "3.3.7  UI框架"],
                ["jQuery        ", "1.11.3  JavaScript库"],
                ["KindEditor    ", "4.1.10  富文本编辑器"],
            ]
        },
        {"type": "divider"},
        {"type": "label", "text": " 项目结构"},
        {
            "type": "code",
            "lines": [
                "src/main/java/cn/gson/oasys/",
                "  controller/   # 控制器层",
                "  model/       # 实体 + DAO",
                "  services/    # 业务逻辑层",
                "  common/      # 公共组件",
            ]
        },
    ],
    "footer_tags": "#SpringBoot  #Java  #MyBatis  #MySQL  #架构设计",
}, os.path.join(OUTPUT_DIR, "05_architecture.jpg"))

# 图6: 配置说明（玫红极简）
gen_card({
    "theme_idx": 5,
    "page_num": 6, "total": TOTAL,
    "kicker": "配置文件指南",
    "title": "配置说明\n3分钟搞定",
    "sections": [
        {"type": "label", "text": " 数据库配置"},
        {
            "type": "code",
            "lines": [
                "spring.datasource.url=jdbc:mysql://",
                "  localhost:3306/oasys",
                "  ?autoReconnect=true&useSSL=false",
                "  &characterEncoding=utf-8",
                "spring.datasource.username=root",
                "spring.datasource.password=your_password",
            ]
        },
        {"type": "label", "text": " AI助手配置（必填）"},
        {
            "type": "code",
            "lines": [
                "zhipu.api.key=your_api_key",
                "# 模型可选: glm-4-flash(免费) / glm-4",
                "zhipu.model=glm-4-flash",
            ]
        },
        {"type": "label", "text": " 文件存储配置"},
        {
            "type": "kv",
            "items": [
                ["Windows  ", "D:/oasys/resources/static/file"],
                ["Linux    ", "/opt/oasys/file"],
            ]
        },
        {"type": "divider"},
        {
            "type": "text",
            "lines": [
                "访问: http://localhost:8088/logins",
                "默认端口 8088，可在 application.properties 修改",
            ]
        },
    ],
    "footer_tags": "#OASYS配置  #application.properties  #SpringBoot",
}, os.path.join(OUTPUT_DIR, "06_config.jpg"))

print(f"\n[Done] {TOTAL} images generated!")
print(f"[Path] {OUTPUT_DIR}")

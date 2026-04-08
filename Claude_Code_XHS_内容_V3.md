# Claude Code 小红书内容 V3

## 封面文案

**Anthropic 出品的 Claude Code！**

程序员的第二个大脑来了

---

## 图文系列内容

### 第1页：MCP 协议
**标题**: MCP 协议：连接一切的桥梁

通过 Model Context Protocol，Claude Code 可以连接 GitHub、Slack、Jira 等数百种工具，让 AI 直接操作你的开发工具链。

**技术要点**:
- 开源标准协议，连接 AI 与外部工具
- 支持 JIRA、GitHub、Sentry、PostgreSQL、Figma 等
- 动态工具更新，无需重启
- 支持 OAuth 2.0 认证

---

### 第2页：上下文管理
**标题**: 上下文管理：让 AI 真正懂你的代码

不是简单的对话，而是深度的代码库理解。

**技术要点**:
- 系统提示词定义基础角色和行为边界
- CLAUDE.md 持久化项目级上下文
- 会话历史保持对话连贯性
- 工作目录实时感知文件变化

---

### 第3页：安全机制
**标题**: 安全机制：风险最小化的设计

Anthropic 在安全上的投入，可能是你见过最认真的。

**技术要点**:
- 默认只读权限，修改需显式授权
- 沙盒化 bash 工具限制文件操作范围
- 命令黑名单防止高危操作
- 提示注入检测保护代码安全

---

### 第4页：权限控制
**标题**: 权限控制：细粒度的安全保障

对比传统 AI 编程工具，Claude Code 的权限控制更加精细。

**技术要点**:
- 默认权限：只读，禁止网络，禁止敏感命令
- 授权后权限：编辑文件，执行命令，访问网络
- 支持按代码库配置白名单
- SOC 2 Type 2、ISO 27001 认证

---

### 第5页：安装使用
**标题**: 快速开始：5分钟上手

```bash
# macOS / Linux
curl -sL https://claude.ai/install.sh | sh

# 或使用 Homebrew
brew install claude-code

# Windows (PowerShell)
winget install Claude.ClaudeCode
```

**技术要点**:
- 支持 macOS、Linux、Windows 全平台
- 配置简单，登录账号即可使用
- 输入 /help 查看所有命令

---

## 适合人群

- 每天和代码打交道超过 4 小时的开发者
- 厌倦了在 IDE 和 AI 助手之间来回切换
- 想要用自然语言驱动整个开发流程
- 对 AI 安全有要求，不想让 AI 随意执行命令

---

## 使用技巧

1. **CLAUDE.md** - 在项目根目录创建，定义项目背景和常用命令
2. **@文件引用** - 直接引用文件或代码片段让 AI 分析
3. **/help** - 查看所有可用命令
4. **MCP 扩展** - 按需添加工具集成

---

## 相关链接

- 官网: https://claude.ai/code
- 文档: https://code.claude.com/docs
- GitHub: https://github.com/anthropics/claude-code

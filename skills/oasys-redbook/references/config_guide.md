# OASYS 配置指南

## 配置文件位置

`src/main/resources/application.properties`

## 数据库配置

```properties
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/oasys?autoReconnect=true&useSSL=false&characterEncoding=utf-8
spring.datasource.username=root
spring.datasource.password=your_password
```

## AI助手配置（必填）

```properties
# 智谱AI API密钥
zhipu.api.key=your_zhipu_api_key

# API地址（通常不需要改）
zhipu.api.url=https://open.bigmodel.cn/api/paas/v4/chat/completions

# 使用的模型
# glm-4-flash: 免费快速（推荐开发用）
# glm-4: 标准模型
# glm-4-plus: 增强模型
zhipu.model=glm-4-flash
```

## 文件存储配置

```properties
# Windows
file.root.path=D:/oasys/resources/static/file
img.rootpath=D:/oasys/resources/static/images
attachment.roopath=D:/oasys/resources/static/attachment

# Linux/Mac
# file.root.path=/opt/oasys/resources/static/file
# img.rootpath=/opt/oasys/resources/static/images
# attachment.roopath=/opt/oasys/resources/static/attachment
```

## 端口配置

默认端口：`8088`

修改方式：
```properties
server.port=8088
```

访问地址：`http://localhost:8088/logins`

## 数据库初始化

```bash
mysql -u root -p < oasys.sql
```

确保创建名为 `oasys` 的数据库：
```sql
CREATE DATABASE oasys DEFAULT CHARACTER SET utf8mb4;
```

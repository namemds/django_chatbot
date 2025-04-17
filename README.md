# django_chatbot
基于vue+django+ollama的对话机器人
## 项目结构
```bash
my_django/
├── controller/             # 控制器（业务逻辑）
│    ├── Robot.py           # 聊天机器人核心逻辑
│    └── SystemController.py  # 页面控制
├── static/                 # 静态资源目录
├── templates/              # 前端模板
├── my_django/              # 项目配置
│   ├── settings.py         # 配置文件
│   ├── urls.py             # 路由配置
│   └── wsgi.py
├── utils/                  
│   └── MysqlUtil.py          # MySQL连接方法
├── .gitignore              
├── manage.py               # Django管理脚本
└── README.md      
```
##快速开始
###1.克隆项目
###2.安装依赖
自行安装cuda、ollama，本地部署一个模型，执行下面命令
```bash
pip install django pymysql requests bcrypt
```
###3.数据库配置
在utils/MysqlUtil.py和my_django/settings.py中的DATABASES中配置自己的数据库，数据库结构如下
```mysql
-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 会话表（属于某个用户）
CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 消息表（属于某个会话）
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    sender VARCHAR(10) NOT NULL, -- 'user' 或 'bot'
    text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
```
###4.运行项目
启动django服务，根据控制台输出的端口信息进入页面使用

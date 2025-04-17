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


# 影视剧论坛系统

一个基于Python Flask开发的影视剧论坛系统，支持多国影视剧分类、用户互动功能。

## 功能特性

### 核心功能
- **国家分类**：按国家浏览影视剧
- **题材分类**：喜剧、爱情、动作、科幻等多种题材
- **用户系统**：注册、登录、个人中心
- **互动功能**：点赞、收藏、评论
- **内容安全**：敏感词过滤，违规内容处理

### 页面风格
- 不同题材页面有不同的视觉风格
- 响应式设计，支持移动端
- 避免血腥暴力内容，专注于健康娱乐

## 技术栈

### 后端
- Flask (Python Web框架)
- SQLAlchemy (数据库ORM)
- JWT (用户认证)
- bcrypt (密码加密)

### 前端
- HTML5/CSS3/JavaScript
- Bootstrap 5 (UI框架)
- Font Awesome (图标库)

### 数据库
- SQLite (开发环境)

## 快速开始

### 1. 环境要求
- Python 3.7+
- pip 包管理器

### 2. 安装运行

**方法一：使用批处理文件（推荐）**
```bash
# Windows系统
double-click run.bat

# 或命令行运行
run.bat
```

**方法二：手动运行**
```bash
# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_data.py

# 启动服务器
python app.py
```

### 3. 访问应用
- 打开浏览器访问：http://localhost:5000
- 管理员账号：admin / 123456
- 测试用户：user1 / 123456 或 user2 / 123456

## 项目结构

```
├── app.py                 # 主应用文件
├── init_data.py           # 初始化数据脚本
├── requirements.txt       # 依赖包列表
├── run.bat               # Windows启动脚本
├── templates/            # HTML模板
│   ├── base.html         # 基础模板
│   ├── index.html        # 首页
│   ├── login.html        # 登录页
│   ├── register.html     # 注册页
│   ├── profile.html      # 个人中心
│   └── movie_detail.html # 影视详情页
└── static/               # 静态文件
    └── default-poster.jpg # 默认海报
```

## API接口

### 用户认证
- `POST /api/register` - 用户注册
- `POST /api/login` - 用户登录

### 影视数据
- `GET /api/movies` - 获取影视列表
- `GET /api/movie/<id>` - 获取影视详情
- `GET /api/countries` - 获取国家列表
- `GET /api/genres` - 获取题材列表

### 互动功能
- `POST /api/movie/<id>/comment` - 发表评论
- `POST /api/movie/<id>/like` - 点赞影视
- `POST /api/movie/<id>/favorite` - 收藏影视

## 安全特性

### 内容审查
- 自动检测敏感词（政治相关词汇）
- 违规内容自动封禁账号
- 评论内容实时过滤

### 数据保护
- 密码加密存储
- JWT token认证
- 防止SQL注入

## 开发说明

### 添加新题材
1. 在`init_data.py`中添加新的Genre记录
2. 在CSS中定义对应的样式类
3. 重启应用即可生效

### 自定义敏感词
修改`app.py`中的`sensitive_words`列表：
```python
sensitive_words = ['政治', '政府', '领导人', '敏感词']
```

### 数据库管理
- 重置数据库：删除`movie_forum.db`文件，然后重新运行`init_data.py`
- 查看数据：使用SQLite工具打开`movie_forum.db`

## 注意事项

1. **环境问题**：确保Python环境正确配置
2. **端口占用**：如果5000端口被占用，修改`app.py`中的端口号
3. **数据持久化**：SQLite数据库文件会保存在项目根目录
4. **生产环境**：部署到生产环境时需要修改密钥和数据库配置

## 许可证

本项目仅供学习使用，请遵守相关法律法规。
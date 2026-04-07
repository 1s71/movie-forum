from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from datetime import datetime, timedelta
import bcrypt
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')
CORS(app)

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-change-this'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# 文件上传配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

db = SQLAlchemy(app)
jwt = JWTManager(app)

# 数据库模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=False)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    style = db.Column(db.String(50))  # 页面风格

# 多对多关联表
movie_countries = db.Table('movie_countries',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'), primary_key=True)
)

movie_genres = db.Table('movie_genres',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(500))
    douban_score = db.Column(db.Float)          # 豆瓣评分
    douban_votes = db.Column(db.String(50))     # 评分人数（如"120万"）
    director = db.Column(db.String(200))        # 导演
    cast = db.Column(db.String(500))            # 主演
    duration = db.Column(db.String(50))         # 片长/集数
    is_series = db.Column(db.Boolean, default=False)  # 是否为剧集
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    countries = db.relationship('Country', secondary=movie_countries, backref='movies')
    genres = db.relationship('Genre', secondary=movie_genres, backref='movies')

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='comments')
    movie = db.relationship('Movie', backref='comments')

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='likes')
    movie = db.relationship('Movie', backref='likes')

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='favorites')
    movie = db.relationship('Movie', backref='favorites')

# 静态文件路由
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# 页面路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/profile')
def profile_page():
    return render_template('profile.html')

@app.route('/movie')
def movie_detail_page():
    return render_template('movie_detail.html')

# API路由

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已存在'}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': '注册成功'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'access_token': access_token,
            'user_id': user.id,
            'username': user.username,
            'role': user.role
        })
    
    return jsonify({'error': '用户名或密码错误'}), 401

@app.route('/api/movies', methods=['GET', 'POST'])
def movies():
    if request.method == 'GET':
        country_id = request.args.get('country_id')
        genre_id = request.args.get('genre_id')
        
        query = Movie.query
        
        if country_id:
            query = query.filter(Movie.countries.any(id=country_id))
        if genre_id:
            query = query.filter(Movie.genres.any(id=genre_id))
        
        movies = query.order_by(Movie.douban_score.desc()).all()
        return jsonify([{
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'year': movie.year,
            'countries': [c.name for c in movie.countries] if movie.countries else [],
            'genres': [g.name for g in movie.genres] if movie.genres else [],
            'poster_url': movie.poster_url,
            'douban_score': movie.douban_score,
            'douban_votes': movie.douban_votes,
            'director': movie.director,
            'cast': movie.cast,
            'duration': movie.duration,
            'is_series': movie.is_series
        } for movie in movies])
    
    elif request.method == 'POST':
        # 用户创建新影视剧
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({'error': '请先登录'}), 401
        
        data = request.get_json()
        
        # 验证必填项
        if not data.get('title'):
            return jsonify({'error': '标题不能为空'}), 400
        if not data.get('countries') or len(data['countries']) == 0:
            return jsonify({'error': '请至少选择一个国家'}), 400
        if not data.get('genres') or len(data['genres']) == 0:
            return jsonify({'error': '请至少选择一个题材'}), 400
        
        # 创建影视剧
        movie = Movie(
            title=data['title'],
            description=data.get('description', ''),
            year=data.get('year'),
            poster_url=data.get('poster_url', ''),
            douban_score=data.get('douban_score'),
            director=data.get('director', ''),
            cast=data.get('cast', ''),
            is_series=data.get('is_series', False),
            created_at=datetime.now()
        )
        
        # 关联国家和题材
        countries = Country.query.filter(Country.id.in_(data['countries'])).all()
        genres = Genre.query.filter(Genre.id.in_(data['genres'])).all()
        movie.countries = countries
        movie.genres = genres
        
        db.session.add(movie)
        db.session.commit()
        
        return jsonify({
            'message': '影视剧添加成功',
            'id': movie.id,
            'title': movie.title
        }), 201

@app.route('/api/countries')
def get_countries():
    countries = Country.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'code': c.code} for c in countries])

@app.route('/api/genres')
def get_genres():
    genres = Genre.query.all()
    return jsonify([{
        'id': g.id, 
        'name': g.name, 
        'description': g.description,
        'style': g.style
    } for g in genres])

@app.route('/api/movie/<int:movie_id>')
def get_movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'description': movie.description,
        'year': movie.year,
        'countries': [c.name for c in movie.countries] if movie.countries else [],
        'genres': [g.name for g in movie.genres] if movie.genres else [],
        'poster_url': movie.poster_url,
        'douban_score': movie.douban_score,
        'douban_votes': movie.douban_votes,
        'director': movie.director,
        'cast': movie.cast,
        'duration': movie.duration,
        'is_series': movie.is_series,
        'comments_count': len(movie.comments),
        'likes_count': len(movie.likes)
    })

@app.route('/api/movie/<int:movie_id>/comments')
def get_movie_comments(movie_id):
    comments = Comment.query.filter_by(movie_id=movie_id).order_by(Comment.created_at.desc()).all()
    return jsonify([{
        'id': c.id,
        'content': c.content,
        'username': c.user.username,
        'created_at': c.created_at.strftime('%Y-%m-%d %H:%M')
    } for c in comments])

@app.route('/api/movie/<int:movie_id>/comment', methods=['POST'])
@jwt_required()
def add_comment(movie_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # 内容安全检查
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'error': '评论内容不能为空'}), 400
    
    # 敏感词过滤（简单实现）
    sensitive_words = ['政治', '政府', '领导人', '敏感词']  # 实际项目中应该使用更完善的过滤机制
    for word in sensitive_words:
        if word in content:
            # 记录违规行为
            user = User.query.get(user_id)
            user.role = 'banned'  # 封号
            db.session.commit()
            return jsonify({'error': '涉及违规内容，账号已被封禁'}), 403
    
    comment = Comment(content=content, user_id=user_id, movie_id=movie_id)
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({'message': '评论成功'}), 201

@app.route('/api/movie/<int:movie_id>/like', methods=['POST'])
@jwt_required()
def like_movie(movie_id):
    user_id = get_jwt_identity()
    
    # 检查是否已经点赞，若已点赞则取消
    existing_like = Like.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({'message': '已取消点赞', 'status': 'unliked'}), 200
    
    like = Like(user_id=user_id, movie_id=movie_id)
    db.session.add(like)
    db.session.commit()
    
    return jsonify({'message': '点赞成功', 'status': 'liked'}), 201

@app.route('/api/movie/<int:movie_id>/favorite', methods=['POST'])
@jwt_required()
def favorite_movie(movie_id):
    user_id = get_jwt_identity()
    
    # 检查是否已经收藏，若已收藏则取消
    existing_fav = Favorite.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if existing_fav:
        db.session.delete(existing_fav)
        db.session.commit()
        return jsonify({'message': '已取消收藏', 'status': 'unfavorited'}), 200
    
    favorite = Favorite(user_id=user_id, movie_id=movie_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({'message': '收藏成功', 'status': 'favorited'}), 201

@app.route('/api/movie/<int:movie_id>/like', methods=['DELETE'])
@jwt_required()
def unlike_movie(movie_id):
    user_id = get_jwt_identity()
    existing_like = Like.query.filter_by(user_id=user_id, movie_id=movie_id).first()
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
    return jsonify({'message': '已取消点赞'}), 200

@app.route('/api/movie/<int:movie_id>/status')
@jwt_required(optional=True)
def get_movie_status(movie_id):
    """获取当前用户对某影视剧的点赞/收藏状态"""
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({'liked': False, 'favorited': False, 'likes_count': 0})
    
    movie = Movie.query.get_or_404(movie_id)
    liked = Like.query.filter_by(user_id=user_id, movie_id=movie_id).first() is not None
    favorited = Favorite.query.filter_by(user_id=user_id, movie_id=movie_id).first() is not None
    likes_count = Like.query.filter_by(movie_id=movie_id).count()
    
    return jsonify({'liked': liked, 'favorited': favorited, 'likes_count': likes_count})

@app.route('/api/user/profile')
@jwt_required()
def get_user_profile():
    """获取当前用户信息"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.strftime('%Y-%m-%d')
    })

@app.route('/api/user/favorites')
@jwt_required()
def get_user_favorites():
    """获取用户收藏列表"""
    user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=user_id).order_by(Favorite.created_at.desc()).all()
    result = []
    for fav in favorites:
        movie = Movie.query.get(fav.movie_id)
        if movie:
            result.append({
                'id': movie.id,
                'title': movie.title,
                'year': movie.year,
                'countries': [c.name for c in movie.countries] if movie.countries else [],
                'genres': [g.name for g in movie.genres] if movie.genres else [],
                'poster_url': movie.poster_url,
                'douban_score': movie.douban_score,
                'favorited_at': fav.created_at.strftime('%Y-%m-%d')
            })
    return jsonify(result)

@app.route('/api/user/likes')
@jwt_required()
def get_user_likes():
    """获取用户点赞列表"""
    user_id = get_jwt_identity()
    likes = Like.query.filter_by(user_id=user_id).order_by(Like.created_at.desc()).all()
    result = []
    for like in likes:
        movie = Movie.query.get(like.movie_id)
        if movie:
            result.append({
                'id': movie.id,
                'title': movie.title,
                'year': movie.year,
                'countries': [c.name for c in movie.countries] if movie.countries else [],
                'genres': [g.name for g in movie.genres] if movie.genres else [],
                'poster_url': movie.poster_url,
                'douban_score': movie.douban_score,
                'liked_at': like.created_at.strftime('%Y-%m-%d')
            })
    return jsonify(result)

# ===== 管理员 API =====
def admin_required(f):
    """管理员权限装饰器"""
    from functools import wraps
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': '需要管理员权限'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/api/admin/users')
@admin_required
def admin_get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id, 'username': u.username, 'email': u.email,
        'role': u.role, 'created_at': u.created_at.strftime('%Y-%m-%d')
    } for u in users])

@app.route('/api/admin/user/<int:user_id>/ban', methods=['POST'])
@admin_required
def admin_ban_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        return jsonify({'error': '不能封禁管理员'}), 400
    user.role = 'banned'
    db.session.commit()
    return jsonify({'message': f'用户 {user.username} 已被封禁'})

@app.route('/api/admin/user/<int:user_id>/unban', methods=['POST'])
@admin_required
def admin_unban_user(user_id):
    user = User.query.get_or_404(user_id)
    user.role = 'user'
    db.session.commit()
    return jsonify({'message': f'用户 {user.username} 已解除封禁'})

@app.route('/api/admin/movies')
@admin_required
def admin_get_movies():
    movies = Movie.query.all()
    return jsonify([{
        'id': m.id, 'title': m.title, 'year': m.year,
        'countries': [c.name for c in m.countries] if m.countries else [],
        'genres': [g.name for g in m.genres] if m.genres else [],
        'likes_count': len(m.likes), 'comments_count': len(m.comments)
    } for m in movies])

@app.route('/api/admin/movie', methods=['POST'])
@admin_required
def admin_add_movie():
    data = request.get_json()
    movie = Movie(
        title=data['title'],
        description=data.get('description', ''),
        year=data.get('year'),
        country_id=data.get('country_id'),
        genre_id=data.get('genre_id'),
        poster_url=data.get('poster_url', ''),
        douban_score=data.get('douban_score'),
        douban_votes=data.get('douban_votes', ''),
        director=data.get('director', ''),
        cast=data.get('cast', ''),
        duration=data.get('duration', ''),
        is_series=data.get('is_series', False)
    )
    db.session.add(movie)
    db.session.commit()
    return jsonify({'message': '影视剧添加成功', 'id': movie.id}), 201

@app.route('/api/admin/movie/<int:movie_id>', methods=['DELETE'])
@admin_required
def admin_delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    # 删除关联数据
    Comment.query.filter_by(movie_id=movie_id).delete()
    Like.query.filter_by(movie_id=movie_id).delete()
    Favorite.query.filter_by(movie_id=movie_id).delete()
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': '影视剧已删除'})

@app.route('/api/admin/comment/<int:comment_id>', methods=['DELETE'])
@admin_required
def admin_delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': '评论已删除'})

@app.route('/api/admin/stats')
@admin_required
def admin_stats():
    return jsonify({
        'total_users': User.query.count(),
        'total_movies': Movie.query.count(),
        'total_comments': Comment.query.count(),
        'total_likes': Like.query.count(),
        'total_favorites': Favorite.query.count(),
        'banned_users': User.query.filter_by(role='banned').count()
    })

# 搜索API
@app.route('/api/search')
def search_movies():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])
    movies = Movie.query.filter(Movie.title.like(f'%{q}%')).order_by(Movie.douban_score.desc()).limit(20).all()
    return jsonify([{
        'id': m.id, 'title': m.title, 'year': m.year,
        'countries': [c.name for c in m.countries] if m.countries else [],
        'genres': [g.name for g in m.genres] if m.genres else [],
        'poster_url': m.poster_url,
        'douban_score': m.douban_score
    } for m in movies])

# 图片上传API
@app.route('/api/upload/poster', methods=['POST'])
@jwt_required()
def upload_poster():
    """上传影视剧海报图片"""
    if 'poster' not in request.files:
        return jsonify({'error': '没有上传文件'}), 400
    
    file = request.files['poster']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    if file and allowed_file(file.filename):
        # 生成唯一文件名
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # 返回图片URL
        return jsonify({
            'message': '上传成功',
            'url': f'/static/uploads/{filename}'
        })
    
    return jsonify({'error': '不支持的文件格式'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # 初始化示例数据
        if not Country.query.first():
            countries = [
                Country(name='中国', code='CN'),
                Country(name='美国', code='US'),
                Country(name='日本', code='JP'),
                Country(name='韩国', code='KR'),
                Country(name='英国', code='UK')
            ]
            db.session.add_all(countries)
        
        if not Genre.query.first():
            genres = [
                Genre(name='喜剧', description='欢乐搞笑的影视作品', style='funny'),
                Genre(name='爱情', description='浪漫温馨的情感故事', style='romantic'),
                Genre(name='动作', description='精彩刺激的打斗场面', style='action'),
                Genre(name='科幻', description='未来科技与想象力的碰撞', style='sci-fi'),
                Genre(name='悬疑', description='扣人心弦的推理故事', style='mystery')
            ]
            db.session.add_all(genres)
        
        db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
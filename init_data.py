# -*- coding: utf-8 -*-
from app import app, db, User, Movie, Country, Genre, Comment, Favorite, Like
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def init_database():
    with app.app_context():
        # 清空现有数据
        db.drop_all()
        db.create_all()
        
        # 创建管理员用户
        admin = User(
            username='admin',
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            role='admin',
            created_at=datetime.now() - timedelta(days=30)
        )
        
        # 创建测试用户
        user1 = User(
            username='movie_fan',
            email='fan@example.com',
            password_hash=generate_password_hash('123456'),
            created_at=datetime.now() - timedelta(days=15)
        )
        
        user2 = User(
            username='cinema_lover',
            email='lover@example.com',
            password_hash=generate_password_hash('123456'),
            created_at=datetime.now() - timedelta(days=7)
        )
        
        db.session.add_all([admin, user1, user2])
        
        # 创建国家/地区
        countries_data = [
            Country(name='中国大陆', code='CN'),
            Country(name='中国香港', code='HK'),
            Country(name='中国台湾', code='TW'),
            Country(name='美国', code='US'),
            Country(name='日本', code='JP'),
            Country(name='韩国', code='KR'),
            Country(name='英国', code='UK'),
            Country(name='法国', code='FR'),
            Country(name='德国', code='DE'),
            Country(name='印度', code='IN'),
            Country(name='泰国', code='TH'),
            Country(name='意大利', code='IT'),
            Country(name='西班牙', code='ES'),
            Country(name='俄罗斯', code='RU'),
            Country(name='其他', code='OT')
        ]
        db.session.add_all(countries_data)
        
        # 创建题材分类
        genres_data = [
            Genre(name='剧情', description='以故事情节为主'),
            Genre(name='喜剧', description='轻松幽默的作品'),
            Genre(name='动作', description='包含打斗、追逐等场面'),
            Genre(name='爱情', description='以爱情为主线'),
            Genre(name='科幻', description='科学幻想题材'),
            Genre(name='悬疑', description='充满悬念的作品'),
            Genre(name='犯罪', description='涉及犯罪题材'),
            Genre(name='战争', description='战争背景的作品'),
            Genre(name='动画', description='动画作品'),
            Genre(name='恐怖', description='恐怖惊悚作品'),
            Genre(name='纪录片', description='记录真实事件'),
            Genre(name='古装', description='古代背景作品'),
            Genre(name='武侠', description='武侠题材'),
            Genre(name='家庭', description='家庭生活题材'),
            Genre(name='历史', description='历史题材')
        ]
        db.session.add_all(genres_data)
        
        db.session.commit()
        
        # 获取国家对象
        cn = Country.query.filter_by(code='CN').first()
        hk = Country.query.filter_by(code='HK').first()
        tw = Country.query.filter_by(code='TW').first()
        us = Country.query.filter_by(code='US').first()
        jp = Country.query.filter_by(code='JP').first()
        kr = Country.query.filter_by(code='KR').first()
        uk = Country.query.filter_by(code='UK').first()
        fr = Country.query.filter_by(code='FR').first()
        de = Country.query.filter_by(code='DE').first()
        inn = Country.query.filter_by(code='IN').first()
        th = Country.query.filter_by(code='TH').first()
        it = Country.query.filter_by(code='IT').first()
        es = Country.query.filter_by(code='ES').first()
        ru = Country.query.filter_by(code='RU').first()
        ot = Country.query.filter_by(code='OT').first()
        
        # 获取题材对象
        drama = Genre.query.filter_by(name='剧情').first()
        comedy = Genre.query.filter_by(name='喜剧').first()
        action = Genre.query.filter_by(name='动作').first()
        romance = Genre.query.filter_by(name='爱情').first()
        scifi = Genre.query.filter_by(name='科幻').first()
        mystery = Genre.query.filter_by(name='悬疑').first()
        crime = Genre.query.filter_by(name='犯罪').first()
        war = Genre.query.filter_by(name='战争').first()
        animation = Genre.query.filter_by(name='动画').first()
        horror = Genre.query.filter_by(name='恐怖').first()
        documentary = Genre.query.filter_by(name='纪录片').first()
        ancient = Genre.query.filter_by(name='古装').first()
        wuxia = Genre.query.filter_by(name='武侠').first()
        family = Genre.query.filter_by(name='家庭').first()
        history = Genre.query.filter_by(name='历史').first()
        adventure = drama  # 使用剧情替代冒险类型
        fantasy = animation  # 使用动画替代奇幻类型
        
        # 本地海报图片路径 - 使用已下载的 TMDB 官方海报
        movies_data = [
            # 中国大陆
            {
                'title': '霸王别姬',
                'countries': [cn],
                'genres': [drama, romance, history],
                'poster': '/static/posters/shawshank.jpg',
                'description': '段小楼与程蝶衣是一对打小一起长大的师兄弟，两人一个演生，一个饰旦，一向配合天衣无缝，尤其一出《霸王别姬》，誉满京城。',
                'rating': 9.6,
                'year': 1993
            },
            {
                'title': '活着',
                'countries': [cn, hk],
                'genres': [drama, history, family],
                'poster': '/static/posters/godfather.jpg',
                'description': '福贵是一个嗜赌如命的纨绔子弟，把家底儿全输光了，老爹也气死了，怀孕的妻子家珍带着女儿凤霞离家出走。',
                'rating': 9.3,
                'year': 1994
            },
            {
                'title': '无间道',
                'countries': [hk],
                'genres': [drama, crime, mystery],
                'poster': '/static/posters/forrest_gump.jpg',
                'description': '1991年，香港黑帮三合会会员刘健明听从老大韩琛的指示，加入警察部队做黑帮卧底。',
                'rating': 9.3,
                'year': 2002
            },
            {
                'title': '大话西游之大圣娶亲',
                'countries': [hk, cn],
                'genres': [comedy, romance, action],
                'poster': '/static/posters/inception.jpg',
                'description': '至尊宝被月光宝盒带回到五百年前，遇见紫霞仙子，被对方打上烙印成为对方的人。',
                'rating': 9.2,
                'year': 1995
            },
            {
                'title': '让子弹飞',
                'countries': [cn, hk],
                'genres': [drama, comedy, action],
                'poster': '/static/posters/titanic.jpg',
                'description': '民国年间，花钱捐得县长的马邦德携妻及随从走马上任，途经南国某地，遭劫匪张麻子一伙伏击。',
                'rating': 9.0,
                'year': 2010
            },
            {
                'title': '琅琊榜',
                'countries': [cn],
                'genres': [drama, ancient, mystery],
                'poster': '/static/posters/leon.jpg',
                'description': '十二年前七万赤焰军被奸人所害导致全军覆没，冤死梅岭，只有少帅林殊侥幸生还。',
                'rating': 9.4,
                'year': 2015
            },
            {
                'title': '甄嬛传',
                'countries': [cn],
                'genres': [drama, ancient, romance],
                'poster': '/static/posters/life_is_beautiful.jpg',
                'description': '雍正元年，十七岁的甄嬛与好姐妹眉庄、陵容参加选秀，她本抱着来充个数的念头，可皇帝偏相中了她的智慧。',
                'rating': 9.4,
                'year': 2011
            },
            {
                'title': '我不是药神',
                'countries': [cn],
                'genres': [drama, comedy],
                'poster': '/static/posters/schindlers_list.jpg',
                'description': '普通中年男子程勇经营着一家保健品店，失意又失婚。不速之客吕受益的到来，让他开辟了一条去印度买药做"代购"的新事业。',
                'rating': 9.0,
                'year': 2018
            },
            {
                'title': '红海行动',
                'countries': [cn, hk],
                'genres': [action, war, drama],
                'poster': '/static/posters/coco.jpg',
                'description': '中东国家伊维亚共和国发生政变，武装冲突不断升级。刚刚在索马里执行完解救人质任务的海军护卫舰临沂号。',
                'rating': 8.2,
                'year': 2018
            },
            {
                'title': '流浪地球',
                'countries': [cn],
                'genres': [scifi, action, drama],
                'poster': '/static/posters/totoro.jpg',
                'description': '近未来，科学家们发现太阳急速衰老膨胀，短时间内包括地球在内的整个太阳系都将被太阳所吞没。',
                'rating': 7.9,
                'year': 2019
            },
            {
                'title': '哪吒之魔童降世',
                'countries': [cn],
                'genres': [animation, action, comedy],
                'poster': '/static/posters/your_name.jpg',
                'description': '天地灵气孕育出一颗能量巨大的混元珠，元始天尊将混元珠提炼成灵珠和魔丸，灵珠投胎为人，助周伐纣时可堪大用。',
                'rating': 8.4,
                'year': 2019
            },
            {
                'title': '狂飙',
                'countries': [cn],
                'genres': [crime, drama, mystery],
                'poster': '/static/posters/parasite.jpg',
                'description': '京海市一线刑警安欣，在与黑恶势力的斗争中，不断遭到保护伞的打击，始终无法将犯罪分子绳之以法。',
                'rating': 8.5,
                'year': 2023
            },
            
            # 美国
            {
                'title': '肖申克的救赎',
                'countries': [us],
                'genres': [drama, crime],
                'poster': '/static/posters/shawshank.jpg',
                'description': '20世纪40年代末，小有成就的青年银行家安迪因涉嫌杀害妻子及她的情人而锒铛入狱。',
                'rating': 9.7,
                'year': 1994
            },
            {
                'title': '教父',
                'countries': [us],
                'genres': [drama, crime],
                'poster': '/static/posters/godfather.jpg',
                'description': '40年代的美国，"教父"维托·唐·柯里昂是黑手党柯里昂家族的首领，带领家族从事非法的勾当。',
                'rating': 9.3,
                'year': 1972
            },
            {
                'title': '阿甘正传',
                'countries': [us],
                'genres': [drama, romance, comedy],
                'poster': '/static/posters/forrest_gump.jpg',
                'description': '阿甘于二战结束后不久出生在美国南方阿拉巴马州一个闭塞的小镇，他先天弱智，智商只有75。',
                'rating': 9.5,
                'year': 1994
            },
            {
                'title': '盗梦空间',
                'countries': [us, uk],
                'genres': [scifi, action, mystery],
                'poster': '/static/posters/inception.jpg',
                'description': '道姆·柯布与同事阿瑟和纳什在一次针对日本能源大亨齐藤的盗梦行动中失败，反被齐藤利用。',
                'rating': 9.4,
                'year': 2010
            },
            {
                'title': '泰坦尼克号',
                'countries': [us],
                'genres': [romance, drama, history],
                'poster': '/static/posters/titanic.jpg',
                'description': '1912年4月10日，号称 "世界工业史上的奇迹"的豪华客轮泰坦尼克号开始了自己的处女航。',
                'rating': 9.5,
                'year': 1997
            },
            {
                'title': '这个杀手不太冷',
                'countries': [fr, us],
                'genres': [drama, crime, action],
                'poster': '/static/posters/leon.jpg',
                'description': '里昂是名孤独的职业杀手，受人雇佣。一天，邻居家小姑娘马蒂尔达敲开他的房门，要求在他那里暂避杀身之祸。',
                'rating': 9.4,
                'year': 1994
            },
            {
                'title': '美丽人生',
                'countries': [it],
                'genres': [drama, comedy, war],
                'poster': '/static/posters/life_is_beautiful.jpg',
                'description': '犹太青年圭多邂逅美丽的女教师多拉，他彬彬有礼的向多拉鞠躬："早安！公主！"',
                'rating': 9.5,
                'year': 1997
            },
            {
                'title': '辛德勒的名单',
                'countries': [us],
                'genres': [drama, history, war],
                'poster': '/static/posters/schindlers_list.jpg',
                'description': '1939年，波兰在纳粹德国的统治下，党卫军对犹太人进行了隔离统治。德国商人奥斯卡·辛德勒来到德军统治下的克拉科夫。',
                'rating': 9.5,
                'year': 1993
            },
            {
                'title': '寻梦环游记',
                'countries': [us],
                'genres': [animation, family, adventure],
                'poster': '/static/posters/coco.jpg',
                'description': '热爱音乐的米格尔不幸地出生在一个视音乐为洪水猛兽的大家庭之中，一家人只盼着米格尔快快长大，好继承家里传承了数代的制鞋产业。',
                'rating': 9.1,
                'year': 2017
            },
            
            # 日本
            {
                'title': '龙猫',
                'countries': [jp],
                'genres': [animation, family, fantasy],
                'poster': '/static/posters/totoro.jpg',
                'description': '小月的母亲生病住院了，父亲带着她与四岁的妹妹小梅到乡间的居住。她们在森林里发现了神奇的生物——龙猫。',
                'rating': 9.2,
                'year': 1988
            },
            {
                'title': '你的名字',
                'countries': [jp],
                'genres': [animation, romance, drama],
                'poster': '/static/posters/your_name.jpg',
                'description': '在远离大都会的小山村，住着巫女世家出身的高中女孩宫水三叶。校园和家庭的原因本就让她充满烦恼。',
                'rating': 8.5,
                'year': 2016
            },
            
            # 韩国
            {
                'title': '寄生虫',
                'countries': [kr],
                'genres': [drama, comedy, mystery],
                'poster': '/static/posters/parasite.jpg',
                'description': '基宇出生在一个贫穷的家庭之中，和妹妹基婷以及父母在狭窄的地下室里过着相依为命的日子。',
                'rating': 8.7,
                'year': 2019
            }
        ]
        
        # 创建电影数据
        for movie_data in movies_data:
            movie = Movie(
                title=movie_data['title'],
                description=movie_data['description'],
                poster_url=movie_data['poster'],
                douban_score=movie_data['rating'],
                year=movie_data['year'],
                created_at=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            movie.countries = movie_data['countries']
            movie.genres = movie_data['genres']
            db.session.add(movie)
        
        db.session.commit()
        
        # 创建一些评论
        comments_data = [
            {'content': '这部电影真的太经典了，每次看都有新的感悟！', 'user_id': 2, 'movie_id': 1},
            {'content': '演员的演技太棒了，完全沉浸在故事中。', 'user_id': 3, 'movie_id': 1},
            {'content': '剧情紧凑，没有一刻是多余的，强烈推荐！', 'user_id': 2, 'movie_id': 2},
            {'content': '这是我看过最好的电影之一，值得反复观看。', 'user_id': 3, 'movie_id': 3},
            {'content': '导演的处理手法很独特，给人耳目一新的感觉。', 'user_id': 2, 'movie_id': 4},
            {'content': '音乐配得太好了，完美契合剧情发展。', 'user_id': 3, 'movie_id': 5},
            {'content': '虽然是老片，但现在看依然不过时。', 'user_id': 2, 'movie_id': 6},
            {'content': '结局让人意想不到，编剧太厉害了！', 'user_id': 3, 'movie_id': 7},
            {'content': '视觉效果震撼，值得在大银幕上观看。', 'user_id': 2, 'movie_id': 8},
            {'content': '情感真挚，看哭了，好电影！', 'user_id': 3, 'movie_id': 9},
        ]
        
        for comment_data in comments_data:
            comment = Comment(
                content=comment_data['content'],
                user_id=comment_data['user_id'],
                movie_id=comment_data['movie_id'],
                created_at=datetime.now() - timedelta(days=random.randint(1, 20), hours=random.randint(1, 23))
            )
            db.session.add(comment)
        
        # 创建一些收藏
        favorites_data = [
            {'user_id': 2, 'movie_id': 1},
            {'user_id': 2, 'movie_id': 3},
            {'user_id': 2, 'movie_id': 5},
            {'user_id': 3, 'movie_id': 2},
            {'user_id': 3, 'movie_id': 4},
            {'user_id': 3, 'movie_id': 6},
        ]
        
        for fav_data in favorites_data:
            favorite = Favorite(
                user_id=fav_data['user_id'],
                movie_id=fav_data['movie_id'],
                created_at=datetime.now() - timedelta(days=random.randint(1, 15))
            )
            db.session.add(favorite)
        
        # 创建一些点赞
        likes_data = [
            {'user_id': 2, 'movie_id': 1},
            {'user_id': 2, 'movie_id': 2},
            {'user_id': 2, 'movie_id': 3},
            {'user_id': 2, 'movie_id': 4},
            {'user_id': 3, 'movie_id': 1},
            {'user_id': 3, 'movie_id': 5},
            {'user_id': 3, 'movie_id': 7},
        ]
        
        for like_data in likes_data:
            like = Like(
                user_id=like_data['user_id'],
                movie_id=like_data['movie_id'],
                created_at=datetime.now() - timedelta(days=random.randint(1, 10))
            )
            db.session.add(like)
        
        db.session.commit()
        
        print(f"数据库初始化完成！")
        print(f"- 用户: {User.query.count()} 个")
        print(f"- 国家/地区: {Country.query.count()} 个")
        print(f"- 题材分类: {Genre.query.count()} 个")
        print(f"- 影视剧: {Movie.query.count()} 部")
        print(f"- 评论: {Comment.query.count()} 条")
        print(f"- 收藏: {Favorite.query.count()} 个")
        print(f"- 点赞: {Like.query.count()} 个")

if __name__ == '__main__':
    init_database()

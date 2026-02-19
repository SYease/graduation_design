"""
数据库模型定义
============================================================
思路说明：
使用 Flask-SQLAlchemy ORM 定义数据库表结构。
每个 class 对应数据库中的一张表。

为什么需要这些表：
1. UserProfile - 存储用户的学习画像数据（标注了哪些行、提问了什么）
   这样用户刷新页面后数据不会丢失，也方便后端做分析
2. LearningRecord - 记录每次学习会话的详细行为数据
   用于追踪用户的学习轨迹，为推荐算法提供输入
3. ChatHistory - 保存AI对话历史
   方便用户回顾之前的问答，也用于分析用户的知识薄弱点
============================================================
"""
from app import db
from datetime import datetime


class UserProfile(db.Model):
    """
    用户学习画像表
    存储用户的累计学习行为数据和各知识点掌握度
    """
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
    # 用户标识（简化版用session_id，正式版应关联用户账号）
    session_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    # 累计查看的排序步骤数
    total_steps_viewed = db.Column(db.Integer, default=0)
    # 标记过疑问的代码行号列表，用JSON字符串存储，如 "[3,5,12]"
    marked_lines = db.Column(db.Text, default='[]')
    # 累计向AI提问的次数
    questions_asked = db.Column(db.Integer, default=0)
    # 提问涉及的知识点列表，JSON字符串，如 '["分治思想","递归调用"]'
    question_topics = db.Column(db.Text, default='[]')
    # 完成排序的次数
    completed_runs = db.Column(db.Integer, default=0)
    # 各知识点掌握度，JSON字符串，如 '{"分治思想":60,"基准选择":40,...}'
    skill_scores = db.Column(db.Text, default='{}')
    # 创建和更新时间
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    # 关联的学习记录和对话历史
    learning_records = db.relationship('LearningRecord', backref='user', lazy=True)
    chat_histories = db.relationship('ChatHistory', backref='user', lazy=True)

    def to_dict(self):
        """将模型对象转为字典，方便JSON序列化返回给前端"""
        import json
        return {
            'id': self.id,
            'session_id': self.session_id,
            'total_steps_viewed': self.total_steps_viewed,
            'marked_lines': json.loads(self.marked_lines),
            'questions_asked': self.questions_asked,
            'question_topics': json.loads(self.question_topics),
            'completed_runs': self.completed_runs,
            'skill_scores': json.loads(self.skill_scores),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class LearningRecord(db.Model):
    """
    学习记录表
    每次用户的一个学习行为（标注代码行、完成排序等）记录一条
    """
    __tablename__ = 'learning_record'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    # 行为类型：mark_line(标注代码行), complete_sort(完成排序), view_step(查看步骤)
    action_type = db.Column(db.String(50), nullable=False)
    # 行为详情，JSON字符串，如 '{"line":12,"knowledge":"基准选择","note":"不理解i的作用"}'
    action_data = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        import json
        return {
            'id': self.id,
            'action_type': self.action_type,
            'action_data': json.loads(self.action_data),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ChatHistory(db.Model):
    """
    AI对话历史表
    保存用户和AI之间的每一轮对话
    """
    __tablename__ = 'chat_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    # 用户的问题
    question = db.Column(db.Text, nullable=False)
    # AI的回答
    answer = db.Column(db.Text, nullable=False)
    # 该问题匹配到的知识点主题
    topic = db.Column(db.String(50), default='')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'topic': self.topic,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

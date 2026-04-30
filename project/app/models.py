import json
from datetime import datetime

from app import db


class KnowledgeNode(db.Model):
    __tablename__ = 'knowledge_node'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    summary = db.Column(db.Text, default='')
    difficulty = db.Column(db.String(20), default='medium')
    category = db.Column(db.String(50), default='algorithm')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    outgoing_edges = db.relationship(
        'KnowledgeEdge',
        foreign_keys='KnowledgeEdge.source_node_id',
        backref='source_node',
        lazy=True,
        cascade='all, delete-orphan',
    )
    incoming_edges = db.relationship(
        'KnowledgeEdge',
        foreign_keys='KnowledgeEdge.target_node_id',
        backref='target_node',
        lazy=True,
        cascade='all, delete-orphan',
    )

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'summary': self.summary,
            'difficulty': self.difficulty,
            'category': self.category,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }


class KnowledgeEdge(db.Model):
    __tablename__ = 'knowledge_edge'

    id = db.Column(db.Integer, primary_key=True)
    source_node_id = db.Column(db.Integer, db.ForeignKey('knowledge_node.id'), nullable=False)
    target_node_id = db.Column(db.Integer, db.ForeignKey('knowledge_node.id'), nullable=False)
    relation_type = db.Column(db.String(30), default='prerequisite')
    weight = db.Column(db.Float, default=1.0)

    def to_dict(self):
        return {
            'id': self.id,
            'source_node_id': self.source_node_id,
            'target_node_id': self.target_node_id,
            'relation_type': self.relation_type,
            'weight': self.weight,
        }


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class UserProfile(db.Model):
    __tablename__ = 'user_profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(64), unique=True, nullable=False, index=True)
    total_steps_viewed = db.Column(db.Integer, default=0)
    marked_lines = db.Column(db.Text, default='[]')
    questions_asked = db.Column(db.Integer, default=0)
    question_topics = db.Column(db.Text, default='[]')
    completed_runs = db.Column(db.Integer, default=0)
    skill_scores = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    learning_records = db.relationship('LearningRecord', backref='user', lazy=True)
    chat_histories = db.relationship('ChatHistory', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
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
    __tablename__ = 'learning_record'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    action_type = db.Column(db.String(50), nullable=False)
    action_data = db.Column(db.Text, default='{}')
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'action_type': self.action_type,
            'action_data': json.loads(self.action_data),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ChatHistory(db.Model):
    __tablename__ = 'chat_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
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


class Algorithm(db.Model):
    __tablename__ = 'algorithm'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    difficulty = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty,
        }

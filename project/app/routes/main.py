import json
import os
import uuid

from flask import Blueprint, render_template, request, session

from app.models import KnowledgeNode, KnowledgeEdge, User, UserProfile

from app.utils.decorators import admin_required


main_bp = Blueprint('main', __name__)


def _ensure_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())[:8]


@main_bp.route('/')
def index():
    _ensure_session()
    return render_template('graph_home.html', session_id=session['session_id'])


@main_bp.route('/learn/<string:node_code>')
def learn_detail(node_code):
    _ensure_session()
    node = KnowledgeNode.query.filter_by(code=node_code, is_active=True).first()
    if not node:
        return render_template('index.html', message='未找到该知识点'), 404

    edge_from = KnowledgeEdge.query.filter_by(source_node_id=node.id).all()
    edge_to = KnowledgeEdge.query.filter_by(target_node_id=node.id).all()

    prerequisites = [
        {
            'code': e.source_node.code,
            'name': e.source_node.name,
            'difficulty': e.source_node.difficulty,
            'summary': e.source_node.summary,
        }
        for e in edge_to
        if e.source_node
    ]
    successors = [
        {
            'code': e.target_node.code,
            'name': e.target_node.name,
            'difficulty': e.target_node.difficulty,
            'summary': e.target_node.summary,
        }
        for e in edge_from
        if e.target_node
    ]

    # Load learning content for this node
    content_data = {}
    content_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'learning_content.json')
    try:
        with open(content_path, 'r', encoding='utf-8') as f:
            all_content = json.load(f)
            content_data = all_content.get(node_code, {})
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return render_template(
        'kruskal_learning.html',
        node=node.to_dict(),
        prerequisites=prerequisites,
        successors=successors,
        content=content_data,
        session_id=session['session_id'],
    )


@main_bp.route('/admin/users')
@admin_required
def admin_users_page():
    _ensure_session()
    users = User.query.order_by(User.created_at.desc()).all()
    user_list = []
    for u in users:
        profile = UserProfile.query.filter_by(user_id=u.id).first()
        user_list.append({
            'id': u.id,
            'username': u.username,
            'role': u.role,
            'created_at': u.created_at.isoformat() if u.created_at else '',
            'questions_asked': profile.questions_asked if profile else 0,
            'completed_runs': profile.completed_runs if profile else 0,
        })
    return render_template('admin_users.html', users=user_list, session_id=session['session_id'])


@main_bp.route('/path')
def path_plan():
    _ensure_session()
    nodes = KnowledgeNode.query.filter_by(is_active=True).all()
    return render_template('path_plan.html', nodes=[n.to_dict() for n in nodes], session_id=session['session_id'])


@main_bp.route('/profile')
def profile_page():
    _ensure_session()
    return render_template('profile.html', session_id=session['session_id'])


@main_bp.route('/seed')
def seed_graph_data():
    _ensure_session()
    if KnowledgeNode.query.count() > 0:
        return {'success': True, 'message': '已有图谱数据，无需重复导入'}

    from app import db
    from werkzeug.security import generate_password_hash

    from config import Config

    # Create default admin user
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(
            username='admin',
            password=generate_password_hash('admin123'),
            role='admin',
        ))

    with open(Config.KNOWLEDGE_GRAPH_FILE, 'r', encoding='utf-8') as f:
        raw_nodes = json.load(f)

    code_to_node = {}
    for item in raw_nodes:
        node = KnowledgeNode(
            code=item['code'],
            name=item['name'],
            summary=item.get('summary', ''),
            difficulty=item.get('difficulty', 'medium'),
            category=item.get('category', 'algorithm'),
            is_active=True,
        )
        code_to_node[item['code']] = node

    from app import db

    db.session.add_all(code_to_node.values())
    db.session.flush()

    # Load edges from generated file
    edges_path = os.path.join(os.path.dirname(Config.KNOWLEDGE_GRAPH_FILE), 'seed_edges.json')
    default_edges = []
    try:
        with open(edges_path, 'r', encoding='utf-8') as f:
            default_edges = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    for source_code, target_code in default_edges:
        source = code_to_node.get(source_code)
        target = code_to_node.get(target_code)
        if source and target:
            db.session.add(
                KnowledgeEdge(
                    source_node_id=source.id,
                    target_node_id=target.id,
                    relation_type='prerequisite',
                    weight=1.0,
                )
            )

    db.session.commit()
    return {'success': True, 'message': '图谱种子数据导入成功'}

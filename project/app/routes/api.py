import json
import os

from flask import Blueprint, jsonify, request, session, current_app

from app import db
from app.models import (
    ChatHistory,
    KnowledgeEdge,
    KnowledgeNode,
    LearningRecord,
    User,
    UserProfile,
)
from app.utils.chat_engine import QA_KNOWLEDGE_BASE
from app.utils.chat_provider import get_provider
from app.utils.decorators import admin_required
from app.utils.recommendation import (
    ADVICE_MAP,
    KNOWLEDGE_GRAPH_RESOURCES,
    KNOWLEDGE_MAP,
    calculate_skill_scores,
    generate_recommendations,
)

api_bp = Blueprint('api', __name__)


def get_or_create_user():
    # If logged in, always use their user_id — never steal another user's profile
    if 'user_id' in session:
        user_profile = UserProfile.query.filter_by(user_id=session['user_id']).first()
        if not user_profile:
            sid = session.get('session_id', '')
            user_profile = UserProfile(
                session_id=sid,
                user_id=session['user_id'],
            )
            db.session.add(user_profile)
            db.session.commit()
        return user_profile

    # Fallback: anonymous session-based tracking
    sid = session.get('session_id', 'anonymous')
    user = UserProfile.query.filter_by(session_id=sid).first()
    if not user:
        user = UserProfile(session_id=sid)
        db.session.add(user)
        db.session.commit()
    return user


@api_bp.route('/knowledge', methods=['GET'])
def get_knowledge():
    nodes = KnowledgeNode.query.filter_by(is_active=True).all()
    edges = KnowledgeEdge.query.all()
    return jsonify(
        {
            'success': True,
            'nodes': [n.to_dict() for n in nodes],
            'edges': [e.to_dict() for e in edges],
            'knowledge_map': KNOWLEDGE_MAP,
            'resources': KNOWLEDGE_GRAPH_RESOURCES,
            'advice_map': ADVICE_MAP,
            'qa_knowledge_base': QA_KNOWLEDGE_BASE,
        }
    )


@api_bp.route('/search', methods=['GET'])
def search_knowledge():
    q = (request.args.get('q') or '').strip().lower()
    if not q:
        return jsonify({'success': True, 'items': []})

    nodes = KnowledgeNode.query.filter_by(is_active=True).all()
    results = []
    for node in nodes:
        haystack = f"{node.code} {node.name} {node.summary}".lower()
        if q in haystack:
            results.append(
                {
                    'code': node.code,
                    'name': node.name,
                    'summary': node.summary,
                    'difficulty': node.difficulty,
                    'action_locate': {'type': 'locate', 'node_code': node.code},
                    'action_learn': {'type': 'learn', 'url': f"/learn/{node.code}"},
                }
            )
    return jsonify({'success': True, 'items': results[:10]})


@api_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    question = (data.get('question') or '').strip()
    if not question:
        return jsonify({'success': False, 'error': '缺少question参数'}), 400

    provider = get_provider(current_app.config)
    answer, topic = provider.ask(question)

    user = get_or_create_user()
    db.session.add(ChatHistory(user_id=user.id, question=question, answer=answer, topic=topic))

    user.questions_asked += 1
    if topic:
        topics = json.loads(user.question_topics)
        topics.append(topic)
        user.question_topics = json.dumps(topics, ensure_ascii=False)

    db.session.commit()

    return jsonify({'success': True, 'answer': answer, 'topic': topic, 'provider': provider.name})


@api_bp.route('/profile', methods=['GET'])
def get_profile():
    user = get_or_create_user()
    return jsonify({'success': True, 'profile': user.to_dict()})


@api_bp.route('/profile', methods=['POST'])
def update_profile():
    data = request.get_json() or {}
    user = get_or_create_user()

    if 'total_steps_viewed' in data:
        user.total_steps_viewed = int(data['total_steps_viewed'])
    if 'marked_lines' in data:
        user.marked_lines = json.dumps(data['marked_lines'], ensure_ascii=False)
    if 'completed_runs' in data:
        user.completed_runs = int(data['completed_runs'])

    db.session.commit()
    return jsonify({'success': True})


@api_bp.route('/mark', methods=['POST'])
def save_mark():
    data = request.get_json() or {}
    line_num = data.get('line')
    if line_num is None:
        return jsonify({'success': False, 'error': '缺少line参数'}), 400

    user = get_or_create_user()
    db.session.add(
        LearningRecord(
            user_id=user.id,
            action_type='mark_line',
            action_data=json.dumps(data, ensure_ascii=False),
        )
    )

    marked = json.loads(user.marked_lines)
    if line_num not in marked:
        marked.append(line_num)
        user.marked_lines = json.dumps(marked)

    db.session.commit()
    return jsonify({'success': True})


@api_bp.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json() or {}
    total_steps = int(data.get('total_animation_steps', 50))

    user = get_or_create_user()
    profile_dict = {
        'total_steps_viewed': user.total_steps_viewed,
        'marked_lines': json.loads(user.marked_lines),
        'questions_asked': user.questions_asked,
        'question_topics': json.loads(user.question_topics),
        'completed_runs': user.completed_runs,
    }

    skill_scores = calculate_skill_scores(profile_dict, total_steps)
    recommendations = generate_recommendations(skill_scores, current_app.config.get('MAX_RECOMMENDATIONS', 5))

    user.skill_scores = json.dumps(skill_scores, ensure_ascii=False)
    db.session.commit()

    return jsonify({'success': True, 'skill_scores': skill_scores, 'recommendations': recommendations})


@api_bp.route('/path/plan', methods=['POST'])
def generate_path():
    data = request.get_json() or {}
    target_code = data.get('target_code')
    mastered_codes = set(data.get('mastered_codes') or [])

    target_node = KnowledgeNode.query.filter_by(code=target_code, is_active=True).first() if target_code else None
    if not target_node:
        return jsonify({'success': False, 'error': '目标知识点不存在'}), 400

    visited = set()
    ordered = []

    def dfs(node):
        if node.code in visited:
            return
        visited.add(node.code)

        incoming = KnowledgeEdge.query.filter_by(target_node_id=node.id).all()
        for edge in incoming:
            if edge.source_node:
                dfs(edge.source_node)

        ordered.append(node)

    dfs(target_node)

    path_items = []
    for node in ordered:
        path_items.append(
            {
                'code': node.code,
                'name': node.name,
                'difficulty': node.difficulty,
                'status': 'mastered' if node.code in mastered_codes else 'todo',
            }
        )

    return jsonify({'success': True, 'target': target_node.to_dict(), 'path': path_items})


@api_bp.route('/records', methods=['GET'])
def get_records():
    user = get_or_create_user()
    records = LearningRecord.query.filter_by(user_id=user.id).order_by(LearningRecord.created_at.desc()).limit(100).all()
    return jsonify({'success': True, 'records': [r.to_dict() for r in records]})


@api_bp.route('/quiz', methods=['GET'])
def get_quiz():
    difficulty = (request.args.get('difficulty') or '').strip().lower()
    concept = (request.args.get('concept') or '').strip().lower()

    quiz_path = os.path.join(current_app.config.get('BASE_DIR', ''), 'data', 'quiz_bank.json')
    if not os.path.exists(quiz_path):
        quiz_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'quiz_bank.json')

    try:
        with open(quiz_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({'success': False, 'error': '题库加载失败'}), 500

    if difficulty:
        questions = [q for q in questions if q.get('difficulty', '') == difficulty]
    if concept:
        questions = [q for q in questions if q.get('concept', '') == concept]

    return jsonify({'success': True, 'questions': questions, 'total': len(questions)})


@api_bp.route('/admin/nodes', methods=['POST'])
@admin_required
def admin_add_node():
    data = request.get_json() or {}
    code = (data.get('code') or '').strip()
    name = (data.get('name') or '').strip()
    if not code or not name:
        return jsonify({'success': False, 'error': 'code 和 name 必填'}), 400

    exists = KnowledgeNode.query.filter_by(code=code).first()
    if exists:
        return jsonify({'success': False, 'error': 'code 已存在'}), 400

    node = KnowledgeNode(
        code=code,
        name=name,
        summary=(data.get('summary') or '').strip(),
        difficulty=(data.get('difficulty') or 'medium').strip(),
        category=(data.get('category') or 'algorithm').strip(),
        is_active=True,
    )
    db.session.add(node)
    db.session.commit()
    return jsonify({'success': True, 'node': node.to_dict()})


@api_bp.route('/admin/edges', methods=['POST'])
@admin_required
def admin_add_edge():
    data = request.get_json() or {}
    source_code = (data.get('source_code') or '').strip()
    target_code = (data.get('target_code') or '').strip()
    if not source_code or not target_code:
        return jsonify({'success': False, 'error': 'source_code 和 target_code 必填'}), 400

    source = KnowledgeNode.query.filter_by(code=source_code, is_active=True).first()
    target = KnowledgeNode.query.filter_by(code=target_code, is_active=True).first()
    if not source or not target:
        return jsonify({'success': False, 'error': '节点不存在'}), 400

    edge = KnowledgeEdge(
        source_node_id=source.id,
        target_node_id=target.id,
        relation_type=(data.get('relation_type') or 'prerequisite').strip(),
        weight=float(data.get('weight') or 1.0),
    )
    db.session.add(edge)
    db.session.commit()

    return jsonify({'success': True, 'edge': edge.to_dict()})


@api_bp.route('/admin/users', methods=['GET'])
@admin_required
def admin_list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify({'success': True, 'users': [u.to_dict() for u in users]})


@api_bp.route('/admin/users/<int:user_id>/reset-password', methods=['POST'])
@admin_required
def admin_reset_password(user_id):
    from werkzeug.security import generate_password_hash

    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'error': '用户不存在'}), 404

    data = request.get_json() or {}
    new_password = (data.get('password') or '123456').strip()
    user.password = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'success': True, 'message': f'用户 {user.username} 的密码已重置为 {new_password}'})

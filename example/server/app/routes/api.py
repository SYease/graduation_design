"""
API路由蓝图
============================================================
思路说明：
api_bp 负责所有前端通过 fetch/AJAX 调用的JSON接口。
前端页面通过这些接口与后端交互，实现：
1. /api/chat - AI对话（知识库匹配 + 对话历史持久化）
2. /api/profile - 用户画像的保存和读取
3. /api/analyze - 掌握度计算 + 个性化推荐生成
4. /api/mark - 代码行标注的保存

所有接口统一返回JSON格式：{ "success": true/false, "data": ... }

为什么这些逻辑放后端而不是前端：
- chat: 知识库数据和匹配算法是业务逻辑，后续要接入真AI服务，Key不能暴露给前端
- profile: 用户数据需要持久化到数据库，前端内存刷新就丢了
- analyze: 掌握度计算是核心算法，放后端方便迭代（比如换IRT模型）
- mark: 标注数据需要持久化，且要关联到用户画像
============================================================
"""
from flask import Blueprint, jsonify, request, session
import json

from app import db
from app.models import UserProfile, LearningRecord, ChatHistory
from app.utils.chat_engine import match_answer
from app.utils.recommendation import (
    calculate_skill_scores, generate_recommendations,
    KNOWLEDGE_MAP, KNOWLEDGE_GRAPH_RESOURCES, ADVICE_MAP
)
from app.utils.chat_engine import QA_KNOWLEDGE_BASE

# 创建API蓝图，注册时会加上 /api 前缀
api_bp = Blueprint('api', __name__)


def get_or_create_user():
    """
    获取当前用户的画像记录，如果不存在则创建一条新的。

    通过 session 中的 session_id 识别用户。
    这是一个辅助函数，多个接口都需要用到。

    返回:
        UserProfile 模型实例
    """
    sid = session.get('session_id', 'anonymous')
    user = UserProfile.query.filter_by(session_id=sid).first()
    if not user:
        user = UserProfile(session_id=sid)
        db.session.add(user)
        db.session.commit()
    return user


@api_bp.route('/chat', methods=['POST'])
def chat():
    """
    AI对话接口

    请求体: { "question": "用户的问题" }
    响应体: { "success": true, "answer": "AI的回答", "topic": "匹配到的知识点" }

    处理流程：
    1. 从请求中获取用户问题
    2. 调用知识库匹配引擎获取回答
    3. 将对话记录保存到数据库（ChatHistory表）
    4. 更新用户画像中的提问次数和提问主题
    5. 返回回答给前端
    """
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({'success': False, 'error': '缺少question参数'}), 400

    question = data['question']

    # 调用知识库匹配引擎获取回答和匹配到的知识点主题
    answer, topic = match_answer(question)

    # 获取当前用户，保存对话历史和更新画像
    user = get_or_create_user()

    # 保存对话记录到 ChatHistory 表
    chat_record = ChatHistory(
        user_id=user.id,
        question=question,
        answer=answer,
        topic=topic
    )
    db.session.add(chat_record)

    # 更新用户画像：提问次数+1，记录提问主题
    user.questions_asked += 1
    if topic:
        topics = json.loads(user.question_topics)
        topics.append(topic)
        user.question_topics = json.dumps(topics, ensure_ascii=False)

    db.session.commit()

    return jsonify({
        'success': True,
        'answer': answer,
        'topic': topic
    })


@api_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    获取当前用户的学习画像

    响应体: { "success": true, "profile": { ... } }

    前端在页面加载时调用此接口，恢复用户之前的学习状态。
    """
    user = get_or_create_user()
    return jsonify({
        'success': True,
        'profile': user.to_dict()
    })


@api_bp.route('/profile', methods=['POST'])
def update_profile():
    """
    更新用户学习画像

    请求体: {
        "total_steps_viewed": 50,
        "marked_lines": [3, 12, 17],
        "completed_runs": 2
    }
    响应体: { "success": true }

    前端在用户学习过程中定期调用此接口，同步行为数据到后端。
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请求体为空'}), 400

    user = get_or_create_user()

    # 更新各字段（只更新前端传来的字段）
    if 'total_steps_viewed' in data:
        user.total_steps_viewed = data['total_steps_viewed']
    if 'marked_lines' in data:
        user.marked_lines = json.dumps(data['marked_lines'], ensure_ascii=False)
    if 'completed_runs' in data:
        user.completed_runs = data['completed_runs']

    db.session.commit()

    return jsonify({'success': True})


@api_bp.route('/mark', methods=['POST'])
def save_mark():
    """
    保存代码行标注

    请求体: {
        "line": 12,
        "knowledge": "基准选择",
        "note": "不理解为什么选最后一个元素"
    }
    响应体: { "success": true }

    处理流程：
    1. 保存标注到 LearningRecord 表（action_type='mark_line'）
    2. 更新用户画像中的 marked_lines 列表
    """
    data = request.get_json()
    if not data or 'line' not in data:
        return jsonify({'success': False, 'error': '缺少line参数'}), 400

    user = get_or_create_user()

    # 保存学习记录
    record = LearningRecord(
        user_id=user.id,
        action_type='mark_line',
        action_data=json.dumps(data, ensure_ascii=False)
    )
    db.session.add(record)

    # 更新用户画像中的标注行号列表
    marked = json.loads(user.marked_lines)
    line_num = data['line']
    if line_num not in marked:
        marked.append(line_num)
        user.marked_lines = json.dumps(marked)

    db.session.commit()

    return jsonify({'success': True})


@api_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    个性化分析接口 - 计算掌握度 + 生成推荐

    请求体: { "total_animation_steps": 65 }
        total_animation_steps: 前端当前排序的总动画步骤数，用于计算查看比例
    响应体: {
        "success": true,
        "skill_scores": { "分治思想": 60, ... },
        "recommendations": [ { "knowledge": "分区操作", "score": 20, ... }, ... ]
    }

    处理流程：
    1. 从数据库读取当前用户的画像数据
    2. 调用 calculate_skill_scores 计算各知识点掌握度
    3. 调用 generate_recommendations 生成个性化推荐
    4. 将计算结果保存回数据库
    5. 返回给前端展示
    """
    data = request.get_json() or {}
    total_steps = data.get('total_animation_steps', 50)

    user = get_or_create_user()

    # 构建用户画像字典，传给计算函数
    profile_dict = {
        'total_steps_viewed': user.total_steps_viewed,
        'marked_lines': json.loads(user.marked_lines),
        'questions_asked': user.questions_asked,
        'question_topics': json.loads(user.question_topics),
        'completed_runs': user.completed_runs,
    }

    # 调用后端算法计算掌握度
    skill_scores = calculate_skill_scores(profile_dict, total_steps)

    # 将计算结果保存到数据库
    user.skill_scores = json.dumps(skill_scores, ensure_ascii=False)
    db.session.commit()

    # 生成个性化推荐
    recommendations = generate_recommendations(skill_scores)

    return jsonify({
        'success': True,
        'skill_scores': skill_scores,
        'recommendations': recommendations
    })


@api_bp.route('/knowledge', methods=['GET'])
def get_knowledge():
    """
    知识图谱数据接口

    响应体: {
        "success": true,
        "knowledge_map": { "分治思想": [1,2,7,8], ... },
        "resources": { "分治思想": { "next": "归并排序", ... }, ... },
        "advice_map": { "分治思想": "...", ... },
        "qa_knowledge_base": [ { "keywords": [...], "topic": "...", "answer": "..." }, ... ]
    }

    将原本硬编码在前端JS中的知识图谱数据、QA知识库等
    通过API暴露，前端不再需要维护这些重复数据。
    """
    return jsonify({
        'success': True,
        'knowledge_map': KNOWLEDGE_MAP,
        'resources': KNOWLEDGE_GRAPH_RESOURCES,
        'advice_map': ADVICE_MAP,
        'qa_knowledge_base': QA_KNOWLEDGE_BASE
    })

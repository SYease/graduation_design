"""
掌握度计算与个性化推荐引擎
============================================================
思路说明：
将原本在前端JS中的 calculateSkillScores 和 renderRecommendations
逻辑移到后端Python实现。

为什么放后端：
1. 掌握度计算是核心业务逻辑，放后端方便迭代算法（比如换成IRT模型）
2. 推荐需要读取知识图谱数据，后端可以直接访问数据文件/数据库
3. 计算结果需要持久化到数据库，后端直接操作更高效
4. 前端只负责展示，不关心计算细节

掌握度计算模型（简化版认知诊断）：
  掌握度 = 基础分 + 步骤加分 + 完成加分 + 提问加分 - 疑问扣分
  结果限制在 0~100 之间
============================================================
"""

# 知识点与代码行号的映射关系
# 这个映射定义了快速排序代码中每一行属于哪个知识点
KNOWLEDGE_MAP = {
    '分治思想': [1, 2, 7, 8],
    '基准选择': [11, 12, 20, 21],
    '分区操作': [4, 10, 13, 14, 15, 16, 17, 18, 19, 22],
    '递归调用': [3, 5, 6],
    '复杂度分析': [],  # 没有直接对应的代码行，通过提问行为推断
}

# 知识图谱中的推荐资源
# 每个知识点对应一个推荐的进阶学习内容
KNOWLEDGE_GRAPH_RESOURCES = {
    '分治思想': {
        'next': '归并排序',
        'difficulty': 'medium',
        'tip': '理解分治后，可以学习同样基于分治的归并排序'
    },
    '基准选择': {
        'next': '随机化快排',
        'difficulty': 'medium',
        'tip': '掌握基准选择后，尝试实现随机化版本'
    },
    '分区操作': {
        'next': 'Hoare分区法',
        'difficulty': 'hard',
        'tip': '掌握Lomuto分区后，可以学习更高效的Hoare分区'
    },
    '递归调用': {
        'next': '尾递归优化',
        'difficulty': 'hard',
        'tip': '理解递归后，学习如何用尾递归优化减少栈空间'
    },
    '复杂度分析': {
        'next': '主定理',
        'difficulty': 'hard',
        'tip': '深入学习主定理(Master Theorem)来分析递归算法复杂度'
    },
}

# 学习建议模板
ADVICE_MAP = {
    '分治思想': '建议重新阅读算法思想面板，理解"分而治之"的核心：先分区，再递归处理子问题。',
    '基准选择': '试着思考：如果选不同的元素作为基准，分区结果会怎样？可以向AI助手提问"基准选择策略"。',
    '分区操作': '分区是快速排序最关键的步骤。建议用单步模式仔细观察第11-22行代码的执行过程。',
    '递归调用': '递归可能比较抽象。建议关注第5-6行，观察排序是如何被分解为更小的子问题的。',
    '复杂度分析': '试着向AI助手提问"时间复杂度"或"最坏情况"，深入理解快速排序的性能特征。',
}


def calculate_skill_scores(user_profile_dict, total_animation_steps=50):
    """
    计算各知识点的掌握度评分

    参数:
        user_profile_dict: 用户画像字典，包含以下字段：
            - total_steps_viewed: 查看的总步骤数
            - marked_lines: 标记过疑问的行号列表
            - questions_asked: 提问次数
            - question_topics: 提问涉及的主题列表
            - completed_runs: 完成排序的次数
        total_animation_steps: 动画总步骤数（前端传入，用于计算查看比例）

    返回:
        dict: { '分治思想': 60, '基准选择': 40, ... }

    计算公式：
        掌握度 = 基础分(10) + 步骤加分(0~30) + 完成加分(0~30) + 提问加分(0~15) - 疑问扣分(每行10分)
    """
    scores = {}

    # 基础分：用户开始学习就给10分底分
    total_viewed = user_profile_dict.get('total_steps_viewed', 0)
    base_score = 10 if total_viewed > 0 else 0

    # 步骤查看加分：按查看比例给分，最高30分
    step_bonus = min(30, round((total_viewed / max(total_animation_steps, 1)) * 30))

    # 完成排序加分：每完成一次给15分，最高30分
    completed = user_profile_dict.get('completed_runs', 0)
    complete_bonus = min(30, completed * 15)

    marked_lines = user_profile_dict.get('marked_lines', [])
    question_topics = user_profile_dict.get('question_topics', [])

    for knowledge, lines in KNOWLEDGE_MAP.items():
        score = base_score + step_bonus + complete_bonus

        # 提问加分：提问了相关主题 +15分
        if knowledge in question_topics:
            score += 15

        # 疑问扣分：标注了该知识点的代码行，每行 -10分
        marked_count = sum(1 for ln in marked_lines if ln in lines)
        score -= marked_count * 10

        # 特殊处理"复杂度分析"：没有对应代码行，通过提问次数评估
        if knowledge == '复杂度分析':
            complexity_q_count = question_topics.count('复杂度分析')
            score += complexity_q_count * 10

        # 限制在 0~100
        scores[knowledge] = max(0, min(100, score))

    return scores


def generate_recommendations(skill_scores, top_n=5):
    """
    根据掌握度生成个性化学习建议

    参数:
        skill_scores: 各知识点掌握度字典 { '分治思想': 60, ... }
        top_n: 返回前N个建议

    返回:
        list: 建议列表，每项包含知识点名称、掌握度、难度标签、建议内容、进阶推荐

    推荐算法：
        按掌握度从低到高排序，优先推荐掌握度最低的知识点
    """
    # 按掌握度从低到高排序
    sorted_scores = sorted(skill_scores.items(), key=lambda x: x[1])

    recommendations = []
    for name, score in sorted_scores[:top_n]:
        # 根据掌握度确定难度标签
        if score >= 70:
            tag = '掌握良好'
            tag_class = 'easy'
        elif score >= 40:
            tag = '需要加强'
            tag_class = 'medium'
        else:
            tag = '建议重点学习'
            tag_class = 'hard'

        rec = {
            'knowledge': name,
            'score': score,
            'tag': tag,
            'tag_class': tag_class,
            'advice': ADVICE_MAP.get(name, ''),
        }

        # 添加知识图谱中的进阶推荐
        if name in KNOWLEDGE_GRAPH_RESOURCES:
            resource = KNOWLEDGE_GRAPH_RESOURCES[name]
            rec['next_topic'] = resource['next']
            rec['next_difficulty'] = resource['difficulty']
            rec['next_tip'] = resource['tip']

        recommendations.append(rec)

    return recommendations

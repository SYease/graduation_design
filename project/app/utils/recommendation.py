KNOWLEDGE_MAP = {
    '最小生成树目标': [8, 16, 32, 33, 34],
    '边排序': [2, 3, 4, 5, 6, 7, 9, 10],
    '成环判断': [27, 28],
    '并查集合并': [4, 5, 7, 8, 9, 10, 13, 14, 15, 16, 17, 18, 23, 24, 29, 30],
    '选边与终止': [25, 29, 30, 31, 32],
    '复杂度分析': [],
    '快速排序': [],
    '归并排序': [],
    '动态规划入门': [],
    'BFS遍历': [],
    'DFS遍历': [],
    'Dijkstra最短路径': [],
    'Prim算法': [],
    '01背包问题': [],
    '二叉树基础': [],
    # 基础算法
    '枚举与模拟': [], '递归与分治': [], '二分查找': [], '前缀和与差分': [],
    '双指针': [], '滑动窗口': [], '位运算': [], '离散化': [], '区间合并': [],
    # 数据结构
    '单链表': [], '双链表': [], '栈与队列': [], '单调栈': [], '单调队列': [],
    '堆': [], '哈希表': [], '树状数组': [], '线段树': [], 'KMP字符串匹配': [],
    'Trie字典树': [], '字符串哈希': [], '平衡树': [],
    # 图论
    '拓扑排序': [], 'Bellman-Ford': [], 'SPFA': [], 'Floyd算法': [],
    '匈牙利算法': [], 'Tarjan强连通': [], '网络流': [],
    # DP
    '线性DP': [], '区间DP': [], '计数DP': [], '状态压缩DP': [], '树形DP': [],
    '记忆化搜索': [], '概率DP': [],
    # 字符串
    'AC自动机': [], 'Manacher': [], '后缀数组': [],
    # 数论
    '质数筛法': [], '约数': [], '欧拉函数': [], '快速幂': [],
    '扩展欧几里得': [], '中国剩余定理': [], '高斯消元': [], '组合计数': [],
    '容斥原理': [], '博弈论': [], '矩阵快速幂': [],
    # 贪心
    '区间选点': [], 'Huffman树': [], '排序不等式': [], '绝对值不等式': [],
    # 计算几何
    '向量基础': [], '凸包': [],
    '图的表示': [],
    '图论基础': [],
    '贪心策略': [],
    '并查集': [],
    'Kruskal 核心流程': [],
    'Kruskal 与 Prim 对比': [],
    '最短路径概述': [],
    '排序算法对比': [],
    'DP与贪心对比': [],
    '二叉搜索树操作': [],
    '树的遍历': [],
    '二分答案': [],
    '可持久化数据结构': [],
    '树与图的存储': [],
    '染色法判定二分图': [],
    'Tarjan强连通分量': [],
    '最近公共祖先LCA': [],
    '差分约束': [],
    '网络流初步': [],
    '计数类DP': [],
    '数位统计DP': [],
    '单调队列优化DP': [],
    '斜率优化DP': [],
    'Manacher算法': [],
    '区间覆盖': [],
    '区间分组': [],
    '点与线段': [],
    '线段相交': [],
    '点在多边形内': [],
}

KNOWLEDGE_GRAPH_RESOURCES = {
    '最小生成树目标': {
        'next': '图论基础题组',
        'difficulty': 'easy',
        'tip': '先巩固生成树、连通分量和无环判定。',
    },
    '边排序': {
        'next': '贪心排序策略',
        'difficulty': 'easy',
        'tip': '练习边排序与候选边遍历顺序。',
    },
    '成环判断': {
        'next': '并查集判环',
        'difficulty': 'medium',
        'tip': '对比标号法与并查集判环逻辑。',
    },
    '并查集合并': {
        'next': '成环判断',
        'difficulty': 'medium',
        'tip': '练习 find 路径压缩和 union 按秩合并。',
    },
    '选边与终止': {
        'next': 'Kruskal 流程题',
        'difficulty': 'medium',
        'tip': '重点练习 n-1 终止条件。',
    },
    '复杂度分析': {
        'next': '算法复杂度专题',
        'difficulty': 'hard',
        'tip': '系统比较 Kruskal/Prim 复杂度。',
    },
    '快速排序': {
        'next': '归并排序',
        'difficulty': 'medium',
        'tip': '重点练习分区(partition)操作和基准选择策略。',
    },
    '归并排序': {
        'next': '排序算法对比',
        'difficulty': 'medium',
        'tip': '练习合并两个有序数组的归并过程。',
    },
    '动态规划入门': {
        'next': '01背包问题',
        'difficulty': 'medium',
        'tip': '从斐波那契数列理解状态转移和记忆化搜索。',
    },
    'BFS遍历': {
        'next': 'DFS遍历',
        'difficulty': 'easy',
        'tip': '练习队列操作和层级遍历。',
    },
    'DFS遍历': {
        'next': 'Dijkstra最短路径',
        'difficulty': 'easy',
        'tip': '练习递归实现和栈模拟两种方式。',
    },
    'Dijkstra最短路径': {
        'next': '最短路径题组',
        'difficulty': 'medium',
        'tip': '理解松弛操作和优先队列优化的关键。',
    },
    '并查集': {
        'next': 'Kruskal 核心流程',
        'difficulty': 'medium',
        'tip': '重点练习 find 路径压缩和 union 按秩合并。',
    },
    'Prim算法': {
        'next': 'Kruskal 与 Prim 对比',
        'difficulty': 'medium',
        'tip': '对比从边出发(Kruskal)和从点出发(Prim)两种策略。',
    },
    '01背包问题': {
        'next': 'DP与贪心对比',
        'difficulty': 'medium',
        'tip': '重点理解二维 DP 表和一维空间优化。',
    },
    '二叉树基础': {
        'next': '二叉搜索树操作',
        'difficulty': 'easy',
        'tip': '从完全二叉树性质入手，理解树的递归定义。',
    },
}

ADVICE_MAP = {
    '最小生成树目标': '先明确连通、无环、最小权值三个条件。',
    '边排序': '观察边序列，理解为什么全局排序是第一步。',
    '成环判断': '关注被拒绝的边，理解 find(u)==find(v) 判环逻辑。',
    '并查集合并': '重点练习 find 路径压缩与 unite 按秩合并。',
    '选边与终止': '结合 n-1 条边规则理解何时结束。',
    '复杂度分析': '区分排序成本与合并维护成本。',
    '快速排序': '以基准选择为核心，练习分区过程。',
    '归并排序': '分而治之，重点掌握合并有序数组。',
    '动态规划入门': '先找最优子结构，再写出状态转移方程。',
    'BFS遍历': '用队列逐层探索，适合最短路径问题。',
    'DFS遍历': '递归深入，回溯时注意恢复状态。',
    'Dijkstra最短路径': '贪心扩展最近节点，注意不能处理负权边。',
    '并查集': 'find 找根 + union 合并，路径压缩是关键。',
    'Prim算法': '从顶点出发逐步扩展 MST，适合稠密图。',
    '01背包问题': '二维 DP 转一维优化是面试常考点。',
    '二叉树基础': '递归是处理树结构的最自然方式。',
    '枚举与模拟': '先想清楚所有可能的情况，再逐一验证。',
    '二分查找': '注意边界：l=mid+1 还是 r=mid，循环条件是 < 还是 <=。',
    '前缀和与差分': '预处理 O(n)，查询 O(1)，适合频繁区间操作。',
    '单链表': '用数组存储 next 指针，避免指针操作出错。',
    '栈与队列': '栈用数组尾端操作，队列用数组循环使用。',
    '单调栈': '求每个元素左右第一个比它大/小的元素。',
    'KMP字符串匹配': 'next[i] 表示模式串前缀的最长公共前后缀长度。',
    'Trie字典树': '每个节点存 26 个子节点指针和一个结束标记。',
    '堆': '数组模拟完全二叉树，上浮和下潜维护堆性质。',
    '树状数组': 'lowbit(x) = x & -x 定位要更新的节点。',
    '线段树': '每个节点存区间聚合值，lazy 标记延迟更新。',
    '拓扑排序': '统计入度，BFS 从入度为 0 的节点开始。',
    'Bellman-Ford': '外层循环 n-1 次，内层松弛每条边。',
    '线性DP': '定义 dp[i] 为以 i 结尾的最优解。',
    '区间DP': '枚举区间长度 len=2..n，再枚举起点。',
    '记忆化搜索': '递归改写为 DP 的好方法：先写暴力再缓存。',
    '质数筛法': '线性筛保证每个数只被最小质因子筛一次。',
    '快速幂': 'while b: if b&1: res=res*a%mod; a=a*a%mod; b>>=1',
    '区间选点': '按区间右端点排序，每次选最右点。',
    'Huffman树': '用小根堆维护当前最小的两个元素。',
}


#贝叶斯
#参数
BKT_PRIOR  = 0.15   # p(L₀): 先验参数
BKT_LEARN  = 0.12   # p(T): 学习参数
BKT_GUESS  = 0.20   # p(G): 猜对参数
BKT_SLIP   = 0.08   # p(S): 失误参数


def bkt_update(mastery, correct):
    # 根据是否答对，用贝叶斯公式更新掌握概率
    L = mastery
    if correct:
        p_correct_given_known = 1.0 - BKT_SLIP
        p_correct_given_unknown = BKT_GUESS
        posterior = (L * p_correct_given_known) / max(
            L * p_correct_given_known + (1 - L) * p_correct_given_unknown, 0.001)
    else:
        p_wrong_given_known = BKT_SLIP
        p_wrong_given_unknown = 1.0 - BKT_GUESS
        posterior = (L * p_wrong_given_known) / max(
            L * p_wrong_given_known + (1 - L) * p_wrong_given_unknown, 0.001)
    #更新掌握度
    L_next = posterior + (1 - posterior) * BKT_LEARN
    return min(0.99, max(0.01, L_next))


def calculate_skill_scores(user_profile_dict, total_animation_steps=50):
    scores = {}

    total_viewed = user_profile_dict.get('total_steps_viewed', 0)
    completed = user_profile_dict.get('completed_runs', 0)
    marked_lines = user_profile_dict.get('marked_lines', [])
    question_topics = user_profile_dict.get('question_topics', [])
    wrong_topics = user_profile_dict.get('wrong_topics', [])

    #加载此前的掌握度，并且转化为小数
    prev_states = user_profile_dict.get('skill_scores', {})
    if isinstance(prev_states, str):
        import json
        prev_states = json.loads(prev_states) if prev_states else {}
    #过滤数据防止出现没答题有分
    prev_states = {k: (v / 100.0 if v > 1.0 else float(v))
                   for k, v in prev_states.items() if v > 0}

    # 统计对的次数
    quiz_correct_count = {}
    for t in question_topics:
        quiz_correct_count[t] = quiz_correct_count.get(t, 0) + 1

    #统计错的次数
    quiz_wrong_count = {}
    for t in wrong_topics:
        quiz_wrong_count[t] = quiz_wrong_count.get(t, 0) + 1

    #活跃度加权
    activity_boost = min(0.06, (total_viewed / max(total_animation_steps, 1)) * 0.03 +
                              completed * 0.015)

    for knowledge in KNOWLEDGE_MAP:
        #优先有的
        mastery = float(prev_states.get(knowledge, BKT_PRIOR))

        quiz_correct = quiz_correct_count.get(knowledge, 0)
        quiz_wrong = quiz_wrong_count.get(knowledge, 0)
        lines_for_topic = KNOWLEDGE_MAP.get(knowledge, [])
        mark_hits = sum(1 for ln in marked_lines if ln in lines_for_topic)

        has_activity = quiz_correct > 0 or quiz_wrong > 0 or mark_hits > 0
        was_scored_before = knowledge in prev_states
        if not has_activity and not was_scored_before:
            continue

        for _ in range(quiz_correct):
            mastery = bkt_update(mastery, correct=True)
        for _ in range(quiz_wrong):
            mastery = bkt_update(mastery, correct=False)
        for _ in range(mark_hits):
            mastery = bkt_update(mastery, correct=False)

        #观看可视化得分
        if total_viewed > 0 and quiz_wrong == 0:
            mastery = min(0.99, mastery + activity_boost * 0.15)

        scores[knowledge] = round(mastery * 100)

    return scores


def generate_recommendations(skill_scores, top_n=5):
    sorted_scores = sorted(skill_scores.items(), key=lambda x: x[1])

    recommendations = []
    for name, score in sorted_scores[:top_n]:
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

        if name in KNOWLEDGE_GRAPH_RESOURCES:
            resource = KNOWLEDGE_GRAPH_RESOURCES[name]
            rec['next_topic'] = resource['next']
            rec['next_difficulty'] = resource['difficulty']
            rec['next_tip'] = resource['tip']

        recommendations.append(rec)

    return recommendations

QA_KNOWLEDGE_BASE = [
    {
        'keywords': ['最小生成树', 'mst', '生成树'],
        'topic': '最小生成树目标',
        'answer': '最小生成树要求连通、无环、总权值最小；若图不连通则结果是最小生成森林。',
    },
    {
        'keywords': ['排序', '边排序', '先排序', '为什么先排'],
        'topic': '边排序',
        'answer': 'Kruskal 先按边权排序，再按从小到大顺序判断是否可加入。',
    },
    {
        'keywords': ['成环', '判环', 'cycle'],
        'topic': '成环判断',
        'answer': '若当前边两个端点已在同一连通分量，加入后会形成环，应拒绝。',
    },
    {
        'keywords': ['并查集', 'union find', 'find', 'union', '合并', '路径压缩'],
        'topic': '并查集合并',
        'answer': '并查集用 parent 数组 + 路径压缩 + 按秩合并实现高效集合管理。find(x) 找到根节点，unite(x,y) 合并两个集合。在 Kruskal 中替代传统标号法。',
    },
    {
        'keywords': ['复杂度', '效率', 'o(e log e)'],
        'topic': '复杂度分析',
        'answer': 'Kruskal 主要成本是边排序 O(E log E)，标号法合并还会带来扫描顶点的额外开销。',
    },
    {
        'keywords': ['快速排序', '快排', 'quicksort', '基准', 'partition'],
        'topic': '快速排序',
        'answer': '快速排序是分治法排序：选基准元素(pivot)，分区使左侧小于基准、右侧大于基准，再递归排序左右子数组。平均 O(n log n)，最坏 O(n²)。',
    },
    {
        'keywords': ['归并排序', 'mergesort', '合并'],
        'topic': '归并排序',
        'answer': '归并排序将数组递归二分至单元素，再自底向上合并有序子数组。时间复杂度稳定 O(n log n)，需要 O(n) 额外空间，是稳定排序。',
    },
    {
        'keywords': ['动态规划', 'dp', '最优子结构', '重叠子问题'],
        'topic': '动态规划入门',
        'answer': '动态规划(DP)适用于有最优子结构和重叠子问题的场景。核心步骤：定义状态、找到状态转移方程、确定边界条件。经典问题包括背包、LCS 等。',
    },
    {
        'keywords': ['bfs', '广度优先', '队列'],
        'topic': 'BFS遍历',
        'answer': 'BFS(广度优先搜索)使用队列逐层遍历图，适合求无权图最短路径。时间复杂度 O(V+E)，空间复杂度 O(V)。',
    },
    {
        'keywords': ['dfs', '深度优先', '递归', '回溯'],
        'topic': 'DFS遍历',
        'answer': 'DFS(深度优先搜索)递归深入探索分支，适合拓扑排序、连通分量检测、回溯问题。时间复杂度 O(V+E)。',
    },
    {
        'keywords': ['dijkstra', '最短路径', '单源'],
        'topic': 'Dijkstra最短路径',
        'answer': 'Dijkstra 算法求解非负权图的单源最短路径。使用优先队列每次选取距离最小的未访问节点松弛邻边，时间复杂度 O((V+E) log V)。',
    },
    {
        'keywords': ['并查集', 'union find', 'find', 'union'],
        'topic': '并查集',
        'answer': '并查集(Disjoint Set Union)支持高效合并和查询连通分量。使用路径压缩和按秩合并后，单次操作近乎 O(1)。在 Kruskal 中可用于判环。',
    },
    {
        'keywords': ['prim', 'prim算法'],
        'topic': 'Prim算法',
        'answer': 'Prim 算法从任一顶点出发，每次选择连接已选集合和未选集合的最小权边。适合稠密图，时间复杂度 O((V+E) log V) 或 O(V²) 取决于实现。',
    },
    {
        'keywords': ['背包', '01背包', 'knapsack'],
        'topic': '01背包问题',
        'answer': '01背包：有 n 个物品各含重量 w[i] 和价值 v[i]，背包容量 W，每物品选或不选，求最大总价值。DP 状态转移：dp[i][j] = max(dp[i-1][j], dp[i-1][j-w[i]] + v[i])。',
    },
    {
        'keywords': ['二叉树', 'bst', '二叉搜索树'],
        'topic': '二叉树基础',
        'answer': '二叉树每个节点最多有两个子节点。二叉搜索树(BST)满足左子树 < 根 < 右子树，查找/插入/删除平均 O(log n)，最坏退化为链表 O(n)。',
    },
]


def match_answer(question):
    q = (question or '').lower()
    best_match = None
    best_score = 0

    for qa in QA_KNOWLEDGE_BASE:
        score = sum(1 for kw in qa['keywords'] if kw.lower() in q)
        if score > best_score:
            best_score = score
            best_match = qa

    if best_match and best_score > 0:
        return best_match['answer'], best_match['topic']

    return (
        '可以继续问我：最小生成树定义、为什么先排序边、并查集如何判环、路径压缩与按秩合并、复杂度分析。',
        '',
    )

QA_KNOWLEDGE_BASE = [
    # ===== Kruskal / MST =====
    {'keywords':['最小生成树','mst','生成树'],'topic':'最小生成树目标','answer':'最小生成树要求连通、无环、总权值最小；若图不连通则结果是最小生成森林。'},
    {'keywords':['排序','边排序','先排序','为什么先排'],'topic':'边排序','answer':'Kruskal 先按边权排序，再按从小到大顺序判断是否可加入。排序复杂度 O(E log E)。'},
    {'keywords':['成环','判环','cycle'],'topic':'成环判断','answer':'若当前边两个端点已在同一连通分量，加入后会形成环，应拒绝。并查集中用 find(u)==find(v) 判环。'},
    {'keywords':['并查集','union find','find','union','合并','路径压缩'],'topic':'并查集合并','answer':'并查集用 parent 数组 + 路径压缩 + 按秩合并实现高效集合管理。find(x) 找到根节点，unite(x,y) 合并两个集合。每次操作近乎 O(1)。'},
    {'keywords':['复杂度','效率','o(e log e)','时间复杂度'],'topic':'复杂度分析','answer':'Kruskal 主要成本是边排序 O(E log E)，并查集操作近乎 O(1)，总复杂度为 O(E log E)。'},
    {'keywords':['prim','prim算法'],'topic':'Prim算法','answer':'Prim 算法从任一顶点出发，每次选择连接已选集合和未选集合的最小权边。适合稠密图，O((V+E)log V) 或 O(V²)。'},
    # ===== 排序 =====
    {'keywords':['快速排序','快排','quicksort','基准','partition','分区'],'topic':'快速排序','answer':'快速排序是分治法排序：选基准 pivot，分区使左侧小于基准、右侧大于基准，再递归。平均 O(n log n)，最坏 O(n²)，不稳定，空间 O(log n)。'},
    {'keywords':['归并排序','mergesort','归并','合并'],'topic':'归并排序','answer':'归并排序二分数组递归至单元素，自底向上合并有序子数组。O(n log n)，稳定，需要 O(n) 额外空间。适合链表排序和外部排序。'},
    # ===== 基础算法 =====
    {'keywords':['枚举','穷举','暴力','模拟'],'topic':'枚举与模拟','answer':'枚举算法穷举所有可能解逐一验证。适用于解空间有限的问题。模拟则按规则逐步执行。两者都是最基础的算法思想。'},
    {'keywords':['递归','分治','divide and conquer'],'topic':'递归与分治','answer':'分治三步骤：分解(Divide)→解决(Conquer)→合并(Combine)。递归函数必须有终止条件(base case)。经典应用：快速排序、归并排序、二分查找。'},
    {'keywords':['二分','折半','binary search','二分查找'],'topic':'二分查找','answer':'二分查找在有序序列中折半搜索，每次排除一半元素。时间复杂度 O(log n)。关键：mid 取法、边界 l=mid+1 还是 r=mid。'},
    {'keywords':['前缀和','差分','区间和','区间修改'],'topic':'前缀和与差分','answer':'前缀和预处理 O(n)，查询任意区间和 O(1)。差分数组实现 O(1) 区间修改后还原原数组。两者的核心是预处理思想。'},
    {'keywords':['双指针','two pointer','对撞指针','快慢指针'],'topic':'双指针','answer':'双指针算法用两个指针协同移动，常用于有序数组的查找、去重、两数之和等。时间复杂度 O(n)，比暴力枚举 O(n²) 高效。'},
    {'keywords':['滑动窗口','sliding window','窗口'],'topic':'滑动窗口','answer':'滑动窗口维护一个可变长度的连续子区间。区别于双指针的是窗口大小可动态变化。常用于子串匹配、最值查询等问题。'},
    {'keywords':['位运算','bit','异或','与','或','移位'],'topic':'位运算','answer':'位运算利用二进制位操作实现高效计算：&与、|或、^异或、~取反、<<左移、>>右移。常用技巧：n&(n-1)消去最低位1，n&-n取最低位1。'},
    {'keywords':['离散化','坐标压缩','映射'],'topic':'离散化','answer':'离散化将大范围稀疏数据映射到紧凑的连续下标。步骤：排序+去重+二分查找映射。节省数组空间，是处理大数值范围的常用技巧。'},
    {'keywords':['区间合并','merge interval','区间覆盖'],'topic':'区间合并','answer':'区间合并算法先按左端点排序，然后顺序扫描，有交集则合并且更新右端点，无交集则新区间开始。O(n log n)。'},
    # ===== 数据结构 =====
    {'keywords':['链表','单链表','linked list'],'topic':'单链表','answer':'单链表每个节点有值和指向下一个节点的指针。用数组模拟时，head 指向头节点，ne[i] 存下一个节点的下标。头插/删除 O(1)。'},
    {'keywords':['栈','stack','LIFO','后进先出'],'topic':'栈与队列','answer':'栈是后进先出(LIFO)结构，用数组尾端操作模拟；队列是先进先出(FIFO)结构，用循环数组实现。两者都是基础线性数据结构。'},
    {'keywords':['单调栈','next greater','NGE','单调性'],'topic':'单调栈','answer':'单调栈维护栈内元素的单调性（递增/递减）。典型应用：求每个元素左右第一个比它大/小的元素(Next Greater Element)。O(n)。'},
    {'keywords':['单调队列','滑动窗口最值'],'topic':'单调队列','answer':'单调队列的队头始终保持区间最优元素。典型应用：滑动窗口内的最大/最小值查询。入队时从队尾弹出不优的元素，O(n)。'},
    {'keywords':['kmp','字符串匹配','next数组','前缀函数'],'topic':'KMP字符串匹配','answer':'KMP 算法利用 next 数组（前缀函数）避免暴力匹配的回退。next[i] 表示模式串前 i 个字符的最长公共前后缀长度。O(n+m)。'},
    {'keywords':['trie','字典树','前缀树','自动补全'],'topic':'Trie字典树','answer':'Trie 树利用字符串公共前缀共享节点来节省空间。每个节点存 26 个子节点指针和一个结束标记。常用于自动补全、拼写检查。'},
    {'keywords':['堆','heap','优先队列','小根堆','大根堆'],'topic':'堆','answer':'堆是完全二叉树结构，小根堆的父节点 ≤ 子节点。用数组模拟，插入上浮 O(log n)，删除取堆顶+下潜 O(log n)。堆排序 O(n log n)。'},
    {'keywords':['哈希表','hash','散列表','拉链法','开放寻址'],'topic':'哈希表','answer':'哈希表通过哈希函数将键映射到数组下标。冲突处理方法：拉链法(链表)和开放寻址法(线性探测)。平均 O(1) 插入/查询。'},
    {'keywords':['字符串哈希','string hash','子串相等'],'topic':'字符串哈希','answer':'字符串哈希将字符串映射为整数，预处理前缀哈希后用公式 O(1) 判定任意子串是否相等。使用大质数取模防冲突。'},
    {'keywords':['树状数组','fenwick','BIT','lowbit'],'topic':'树状数组','answer':'树状数组(Fenwick Tree)支持单点更新+前缀查询，O(log n)。核心操作：lowbit(x)=x&-x 定位更新节点。代码短于线段树。'},
    {'keywords':['线段树','segment tree','区间查询','lazy标记'],'topic':'线段树','answer':'线段树每个节点存区间聚合值，支持区间查询和区间修改 O(log n)。lazy 标记延迟下推实现区间更新。比树状数组功能更强。'},
    {'keywords':['平衡树','treap','splay','avl','红黑树'],'topic':'平衡树','answer':'平衡树通过旋转或随机优先级保持树高度 O(log n)，防止 BST 退化为链表。常见：Treap(堆+树)、Splay(伸展)、AVL(严格平衡)、红黑树。'},
    # ===== 图论 =====
    {'keywords':['拓扑排序','topological sort','DAG','入度'],'topic':'拓扑排序','answer':'拓扑排序适用于有向无环图(DAG)。BFS 实现：统计入度，入度为 0 的节点入队，出队时邻点入度减 1，新入度为 0 者入队。O(V+E)。'},
    {'keywords':['bellman ford','负权边'],'topic':'Bellman-Ford','answer':'Bellman-Ford 可处理负权边的单源最短路。外层循环 n-1 轮，每轮松弛所有边。第 n 轮仍有更新说明存在负权环。O(VE)。'},
    {'keywords':['spfa','队列优化'],'topic':'SPFA','answer':'SPFA 是 Bellman-Ford 的队列优化版：只有被松弛的节点才入队。稀疏图效率高，但最坏仍为 O(VE)，可能被卡。'},
    {'keywords':['floyd','全源最短路','Warshall'],'topic':'Floyd算法','answer':'Floyd 算法求全源最短路（任意两点间）。三重循环：for k for i for j，dp[i][j]=min(dp[i][j],dp[i][k]+dp[k][j])。O(n³)。'},
    {'keywords':['二分图','染色法','bipartite'],'topic':'染色法判定二分图','answer':'染色法用两种颜色交替染图节点，若出现相邻同色则不是二分图。DFS/BFS 实现，O(V+E)。二分图可划分为两个内部无边集合。'},
    {'keywords':['匈牙利','hungarian','二分图匹配','增广路'],'topic':'匈牙利算法','answer':'匈牙利算法求二分图最大匹配。核心是寻找增广路：从左侧未匹配点出发，交替走未匹配边和匹配边，终点也是未匹配点则增广成功。O(nm)。'},
    {'keywords':['tarjan','强连通','SCC','缩点'],'topic':'Tarjan强连通','answer':'Tarjan 算法求有向图强连通分量(SCC)。基于 DFS 序(dfn)和 low 数组。low[u]=min(dfn[u],low[v],dfn[back-edge])。dfn==low 时弹出 SCC。'},
    {'keywords':['lca','最近公共祖先','倍增'],'topic':'LCA','answer':'LCA(最近公共祖先)的倍增法：预处理每个节点向上 2^k 层的祖先表 O(n log n)，查询时将两节点跳到同深度再一起上跳 O(log n)。'},
    {'keywords':['差分约束','不等式','spfa判环'],'topic':'差分约束','answer':'差分约束系统将不等式组 x_i-x_j≤c 转化为图论最短路：边 j→i 权 c。用 SPFA 判负环验证可行性。'},
    {'keywords':['网络流','最大流','dinic','最小割'],'topic':'网络流','answer':'网络流求解从源点 s 到汇点 t 的最大流量。Dinic 算法：BFS 分层图 + DFS 多路增广 + 当前弧优化。最大流=最小割。'},
    # ===== DP =====
    {'keywords':['背包','01背包','完全背包','多重背包'],'topic':'01背包问题','answer':'01背包：n 个物品，第 i 个重 w[i] 价值 v[i]，每物品选或不选，求容量 W 内最大价值。dp[i][j]=max(dp[i-1][j],dp[i-1][j-w[i]]+v[i])。一维优化需倒序遍历。'},
    {'keywords':['线性dp','lis','最长上升','编辑距离'],'topic':'线性DP','answer':'线性 DP 按一维或二维顺序递推。典型：最长上升子序列(LIS) dp[i]=max(dp[j]+1), j<i, a[j]<a[i]。编辑距离 dp[i][j]=min(插入,删除,替换)。'},
    {'keywords':['区间dp','石子合并','区间断点'],'topic':'区间DP','answer':'区间 DP 的状态定义为区间 [l,r]。枚举区间长度 len=2..n，再枚举起点 i，断点 k∈[i,i+len-1) 划分区间。典型：石子合并问题。'},
    {'keywords':['计数dp','方案数','取模'],'topic':'计数DP','answer':'计数类 DP 求满足条件的方案总数。通常需要对大质数取模(1e9+7)。关键在于找出递推关系和初始化边界 dp[0]=1。'},
    {'keywords':['数位dp','digit dp','逐位统计','记忆化'],'topic':'数位DP','answer':'数位 DP 按数位逐位 DP，通常用记忆化搜索实现。如统计 1~n 中数字 3 的出现次数。注意前导零和上界限制。'},
    {'keywords':['状态压缩','状压dp','bitmask','TSP'],'topic':'状态压缩DP','answer':'状态压缩 DP 用二进制位掩码表示集合状态。如 TSP 问题：dp[mask][i] 表示已访问 mask 集合、当前在 i 的最短路径。mask 从 0 到 2^n-1 枚举。'},
    {'keywords':['树形dp','树上dp','后序遍历'],'topic':'树形DP','answer':'树形 DP 在树结构上做自底向上递归：先处理子树结果，再汇总到根。如求树的最大独立集、树的重心。常用后序遍历顺序。'},
    {'keywords':['记忆化搜索','memo','缓存','自上而下'],'topic':'记忆化搜索','answer':'记忆化搜索是 DP 的递归实现：DFS 函数内先查缓存，已算过直接返回，否则计算后存入缓存。等价于自顶向下的 DP。比迭代 DP 更直观。'},
    {'keywords':['概率dp','期望','expected value'],'topic':'概率DP','answer':'概率 DP 的状态转移带概率，通常求期望值 E。关键公式：E(X)=Σ(P_i×V_i)。如抛硬币直到连续正面朝上的期望次数。'},
    # ===== 字符串 =====
    {'keywords':['ac自动机','AC自动机','fail指针','多模匹配'],'topic':'AC自动机','answer':'AC 自动机 = Trie + KMP。在 Trie 上构建 fail 指针（指向最长可匹配后缀），实现多模式串同时匹配。复杂度 O(n+m+匹配次数)。'},
    {'keywords':['manacher','最长回文','回文子串'],'topic':'Manacher','answer':'Manacher 算法 O(n) 求最长回文子串。核心技巧：利用已求的回文半径对称性减少重复计算，维护当前最右回文边界。'},
    {'keywords':['后缀数组','suffix array','height','LCP'],'topic':'后缀数组','answer':'后缀数组将所有后缀排序。sa[i] 第 i 小后缀的起始位置，rank[i] 后缀 i 的排名，height[i]=LCP(sa[i],sa[i-1])。可在 O(n) 或 O(n log n) 构建。'},
    # ===== 数论 =====
    {'keywords':['质数','素数','筛法','埃氏筛','线性筛','分解质因数'],'topic':'质数筛法','answer':'埃氏筛 O(n log log n) 标记质数的倍数；线性筛 O(n) 保证每个合数只被最小质因子筛一次。分解质因数 O(√n) 试除。'},
    {'keywords':['约数','因数','divisor','约数个数','约数和'],'topic':'约数','answer':'求约数 O(√n) 试除。约数个数公式：n=Πp_i^a_i，则 d(n)=Π(a_i+1)。约数和公式：σ(n)=Π(p_i^(a_i+1)-1)/(p_i-1)。'},
    {'keywords':['欧拉函数','euler','phi','互质','φ'],'topic':'欧拉函数','answer':'φ(n)=1~n 中与 n 互质的数的个数。φ(n)=n×Π(1-1/p_i)。性质：Σφ(d)=n (d|n)。用于欧拉定理 a^φ(m)≡1(mod m)。'},
    {'keywords':['快速幂','快速幂','power','二分幂','模幂'],'topic':'快速幂','answer':'快速幂用二分思想求 a^b mod p：while b>0: if b&1: res=res*a%p; a=a*a%p; b>>=1。O(log b)。'},
    {'keywords':['扩展欧几里得','exgcd','扩展gcd','乘法逆元'],'topic':'扩展欧几里得','answer':'扩展欧几里得求 ax+by=gcd(a,b) 的整数解。可用于求乘法逆元：若 gcd(a,m)=1，则 a×x≡1(mod m)，x 即 a 的逆元。'},
    {'keywords':['中国剩余定理','CRT','同余','孙子定理'],'topic':'中国剩余定理','answer':'CRT 解同余方程组 x≡a_i(mod m_i)，其中 m_i 两两互质。x=Σ(a_i×M_i×inv_i) mod M，M=Πm_i。'},
    {'keywords':['高斯消元','消元','线性方程组','gauss'],'topic':'高斯消元','answer':'高斯消元用初等行变换将增广矩阵化为阶梯形，求解线性方程组。O(n³)。步骤：选主元→消去下方→回代求解。'},
    {'keywords':['组合数','C(n,m)','组合计数','卢卡斯','lucas'],'topic':'组合计数','answer':'C(n,m) 的递推：C(n,m)=C(n-1,m)+C(n-1,m-1)。Lucas 定理用于 n 很大 p 为质数时：C(n,m)≡Π C(n_i,m_i)(mod p)。'},
    {'keywords':['容斥原理','inclusion exclusion','并集','交集'],'topic':'容斥原理','answer':'容斥原理：|∪A_i|=Σ|A_i|-Σ|A_i∩A_j|+Σ|A_i∩A_j∩A_k|-...。用于求多个集合并集的大小。对称性可用于计数问题。'},
    {'keywords':['博弈论','nim','SG函数','必胜必败'],'topic':'博弈论','answer':'Nim 游戏：所有堆异或和 ≠ 0 则先手必胜。SG 函数：mex{后继状态的 SG 值}，SG=0 必败，SG>0 必胜。适用于有向图游戏。'},
    {'keywords':['矩阵快速幂','matrix','矩阵乘法','加速递推'],'topic':'矩阵快速幂','answer':'矩阵快速幂 = 矩阵乘法 + 快速幂。用于加速线性递推 O(log n)，如斐波那契：[[1,1],[1,0]]^n 求 F(n)。'},
    # ===== 贪心 =====
    {'keywords':['贪心','greedy','局部最优','区间选点'],'topic':'区间选点','answer':'贪心每步选局部最优，希望得到全局最优。MST 问题中贪心正确。区间选点：按右端点排序，每选最右点。Huffman：每次合并最小两堆。'},
    {'keywords':['huffman','哈夫曼','编码','前缀编码'],'topic':'Huffman树','answer':'Huffman 树是最优前缀编码树。用小根堆每次取最小的两个节点合并为新节点，权值为两者之和。WPL=Σ叶子权值×深度。'},
    # ===== 计算几何 =====
    {'keywords':['向量','叉积','点积','cross product','dot product'],'topic':'向量基础','answer':'点积 a·b=|a||b|cosθ 用于求夹角、投影。叉积 a×b=|a||b|sinθ 用于求面积、判断方向。叉积 >0 表示逆时针方向。'},
    {'keywords':['凸包','convex hull','graham','andrew'],'topic':'凸包','answer':'凸包是包含所有点的最小凸多边形。Andrew 算法：按 x 排序→求下凸壳(从左到右)→求上凸壳(从右到左)。O(n log n)。'},
    # ===== 树结构 =====
    {'keywords':['BST','二叉搜索树','插入','删除','查找'],'topic':'BST操作','answer':'BST 性质：左子树 < 根 < 右子树。查找/插入：从根开始比较大小走左/右。删除分三种：叶子直接删、单子用子替、双子找后继替。'},
    {'keywords':['树遍历','前序','中序','后序','层序'],'topic':'树的遍历','answer':'前序：根左右；中序：左根右；后序：左右根；层序：队列 BFS。BST 中序遍历得到升序序列。前序+中序可唯一确定二叉树。'},
    {'keywords':['二叉树','完全二叉树','满二叉树','树的性质'],'topic':'二叉树基础','answer':'二叉树每个节点最多两个子节点。满二叉树：每层全满。完全二叉树：除最后一层外全满，最后一层靠左。第 i 层最多 2^(i-1) 个节点。'},
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
        '你可以问我关于算法与数据结构的任何问题，包括：排序算法、图论（BFS/DFS/Dijkstra/Prim/Kruskal）、'
        '动态规划（背包/线性DP/区间DP/树形DP）、数据结构（链表/栈/堆/哈希/并查集/线段树/树状数组）、'
        '数论（质数/快速幂/组合计数）、字符串（KMP/Trie/AC自动机）、贪心策略、计算几何等。',
        '',
    )

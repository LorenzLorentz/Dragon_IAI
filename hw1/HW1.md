## 作业1 搜索

### 1 简答题

#### 1. 相比树搜索，图搜索作出了什么改进？

$\color{Blue}{Answer:}$

图搜索中记录节点的访问情况。如果一个节点已经访问过，在拓展时便不会把它加入 frontier 集合。

#### 2. 相比宽度优先搜索（BFS），深度优先搜索（DFS）和一致代价搜索（UCS）分别有什么优劣？

$\color{Blue}{Answer:}$

(1) DFS相比BFS的优劣：DFS的空间复杂度为 $O(bm)$，而BFS的空间复杂度为 $O(b^m)$，DFS的空间复杂度更优秀。但是DFS不完备，也不最优，不能保证搜索到一个解，也不能保证搜索到最优解。

(2) UCS相比BFS的优劣：当不同层的代价不一样的时候，BFS不能保证搜索到最优解，而UCS可以在这样的情况保证最优。但是UCS每一步都会有 $priority queue$ 的自动排序，复杂度为 $O(\log n)$，总的复杂度稍高。

#### 3. 在约束满足问题（Constraint Satisfaction Problems）中，搜索算法为什么每次要选择约束尽量多的变量（most constrained variable）和约束尽量少的值（least constrained value）

$\color{Blue}{Answer:}$

(1) 选择约束比较多的变量使得接下来这个变量的值的选项更少，搜索的空间更小；(2) 对其他节点约束比较少的值使得这个选择能够走到终点的概率更大，更不容易中道崩殂。

#### 4. 随机集束搜索（Stochastic Beam Search）为什么要引入随机性？它是否能保证找到最优解？

$\color{Blue}{Answer:}$

(1) 局部 beam search 容易陷入局部最优，收敛到一个小空间，引入随机性可以在一定程度上避免局部最优。

(2) 随机 beam search 不能保证找到最优解，因为它本质上还是一种贪心算法，只找到了局部最优的 $k$ 个解，不能保证全局最优。

#### 5. Min-Max 搜索中，若被 Alpha-Beta 剪枝的节点状态值的符号反转，根节点决策有可能发生改变吗？为什么？

$\color{Blue}{Answer:}$

Pass

### 2 $A^*$算法的性质

$\color{Blue}{Answer:}$


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

(1) 对节点 $n$ 满足 $h(n) \leq h^*(n) + C_1$，要证 $g(T) \leq h^*(S) + C_1$

有 $h(S) \leq h^*(S) + C_1$，$g(T)=h$

(2) 对节点 $n$ 满足 $h(n) \leq C_2 h^*(n)$，要证 $g(T) \leq C_2 h^*(S)$

### 3 蒙特卡洛树搜索

$\color{Blue}{Answer:}$

(1) 先手没有必胜策略，后手可以保证不输。

(3) 实验结果见`MCTS_task3.txt`文件，ai配置按照体重要求

根据实验结果可知：

| 先手   | 后手      | 先手胜率 | 先手不输率 | 后手胜率 | 后手不输率 |
|:------:|:---------:|:-------:|:---------:|:-------:|:---------:|
| Random | UCT | 63%     | 74%       | 26%     | 37%       |
| UCT | Random | 56% | 65% | 35% | 44% |
| Alphabeta | UCT | 99% | 100% | 0% | 1%|
| UCT | Alphabeta | 0% | 15% | 85% | 100% |
| UCT | UCT | 59% | 70% | 30% | 41% |

注：题干中指出应为 $3 \times 2 = 6$ 组，疑似有误，因为 MCTS vs MCTS 不需要两组。


(4) 

设定对手为Alphabeta，分别在 $C=0.1, C=5.0$ 条件下，分别先后手进行对弈，统计输出信息，实验结果见文件`MCTS_task4_C=0.1.txt`, `MCTS_task4_C=5.0.txt`, `MCTS_task_stat.txt`，统计陈旭为`stat.py`。

统计结果如下文

``` bash
--- c=0.1 ----
action 0 出现了 279 次
action 1 出现了 265 次
action 2 出现了 272 次
action 3 出现了 246 次
action 4 出现了 280 次
action 5 出现了 219 次
action 6 出现了 237 次
action 7 出现了 214 次
action 8 出现了 207 次

--- c=5.0 ----
action 0 出现了 286 次
action 1 出现了 267 次
action 2 出现了 264 次
action 3 出现了 230 次
action 4 出现了 280 次
action 5 出现了 242 次
action 6 出现了 235 次
action 7 出现了 191 次
action 8 出现了 211 次
```

可以看出，不同 $C$ 取值在井字棋游戏中不会带来显著差异，都近似为随机 (???是不是我的算法实现有问题)。

(5)

本实验非常耗时，实验结果见文件`MCTS_task5.txt`。

大量数据显示，先手胜率始终在 $30\%$ 左右，后手胜率始终在 $70\%$ 左右，与`n_rollout`与`n_search`无显著关联，表明其与搜索质量无显著关联。

同时，显然，`n_rollout`与`n_search`与搜索速度呈负相关，具体依赖情况没有具体分析。

(6)

实验结果见文件`MCTS_task6.txt`。

MCTS的落子非常不合理。

(7) (c)

分析文件待编写。
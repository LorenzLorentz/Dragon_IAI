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

(3)

```bash
> python pit.py
Player 1:Random Player  Player 2:AlphaBeta Player
P1 win: 0 (0) P2 win: 83 (83) Draw: 17 (17): 100%|████████████████████████████████████████████████████████████████████████████| 100/100 [00:00<00:00, 548.61it/s]
Player 1 (Random Player) win: 0 (0.00%)
Player 2 (AlphaBeta Player) win: 83 (83.00%)
Draw: 17 (17.00%)
Player 1 not lose: 17 (17.00%)
Player 2 not lose: 100 (100.00%)
Player 1:AlphaBeta Player  Player 2:Random Player
P1 win: 98 (98) P2 win: 0 (0) Draw: 2 (2): 100%|██████████████████████████████████████████████████████████████████████████████| 100/100 [00:00<00:00, 869.26it/s]
Player 1 (AlphaBeta Player) win: 98 (98.00%)
Player 2 (Random Player) win: 0 (0.00%)
Draw: 2 (2.00%)
Player 1 not lose: 100 (100.00%)
Player 2 not lose: 2 (2.00%)
```

```bash
> python pit.py
Player 1:Random Player  Player 2:UCT Player
P1 win: 55 (55) P2 win: 33 (33) Draw: 12 (12): 100%|███████████████████████████████████████████████████████████████████████████| 100/100 [00:05<00:00, 17.03it/s]
Player 1 (Random Player) win: 55 (55.00%)
Player 2 (UCT Player) win: 33 (33.00%)
Draw: 12 (12.00%)
Player 1 not lose: 67 (67.00%)
Player 2 not lose: 45 (45.00%)
Player 1:UCT Player  Player 2:Random Player
P1 win: 63 (63) P2 win: 27 (27) Draw: 10 (10): 100%|███████████████████████████████████████████████████████████████████████████| 100/100 [00:07<00:00, 13.85it/s]
Player 1 (UCT Player) win: 63 (63.00%)
Player 2 (Random Player) win: 27 (27.00%)
Draw: 10 (10.00%)
Player 1 not lose: 73 (73.00%)
Player 2 not lose: 37 (37.00%)
```

```bash
> python pit.py
Player 1:AlphaBeta Player  Player 2:UCT Player
P1 win: 100 (100) P2 win: 0 (0) Draw: 0 (0): 100%|█████████████████████████████████████████████████████████████████████████████| 100/100 [00:04<00:00, 21.00it/s]
Player 1 (AlphaBeta Player) win: 100 (100.00%)
Player 2 (UCT Player) win: 0 (0.00%)
Draw: 0 (0.00%)
Player 1 not lose: 100 (100.00%)
Player 2 not lose: 0 (0.00%)
Player 1:UCT Player  Player 2:AlphaBeta Player
P1 win: 0 (0) P2 win: 78 (78) Draw: 22 (22): 100%|█████████████████████████████████████████████████████████████████████████████| 100/100 [00:07<00:00, 12.84it/s]
Player 1 (UCT Player) win: 0 (0.00%)
Player 2 (AlphaBeta Player) win: 78 (78.00%)
Draw: 22 (22.00%)
Player 1 not lose: 22 (22.00%)
Player 2 not lose: 100 (100.00%)
```

(4) 

```bash
> python stat.py
--- c=0.1 ----
数字 1 出现了 76 次
数字 2 出现了 89 次
数字 3 出现了 73 次
数字 4 出现了 82 次
数字 5 出现了 80 次
数字 6 出现了 121 次
数字 7 出现了 109 次
数字 8 出现了 96 次
--- c=5.0 ----
数字 1 出现了 82 次
数字 2 出现了 77 次
数字 3 出现了 83 次
数字 4 出现了 102 次
数字 5 出现了 89 次
数字 6 出现了 90 次
数字 7 出现了 103 次
数字 8 出现了 87 次
```
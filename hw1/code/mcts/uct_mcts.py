from .node import MCTSNode, INF
from .config import MCTSConfig
from env.base_env import BaseGame
from other_algo.alpha_beta_search import go_heuristic_evaluation

import numpy as np

class UCTMCTSConfig(MCTSConfig):
    def __init__(
        self,
        n_rollout:int = 1,
        *args, **kwargs
    ):
        MCTSConfig.__init__(self, *args, **kwargs)
        self.n_rollout = n_rollout


class UCTMCTS:
    def __init__(self, init_env:BaseGame, config: UCTMCTSConfig, root:MCTSNode=None, depth:int=5):
        self.depth = depth
        self.config = config
        self.root = root
        if root is None:
            self.init_tree(init_env)
        self.root.cut_parent()
    
    def init_tree(self, init_env:BaseGame):
        # initialize the tree with the current state
        # fork the environment to avoid side effects
        env = init_env.fork()
        self.root = MCTSNode(
            action=None, env=env, reward=0,
        )
    
    def get_subtree(self, action:int):
        # return a subtree with root as the child of the current root
        # the subtree represents the state after taking action
        if self.root.has_child(action):
            new_root = self.root.get_child(action)
            return UCTMCTS(new_root.env, self.config, new_root)
        else:
            return None
    
    def uct_action_select(self, node:MCTSNode) -> int:
        # select the best action based on UCB when expanding the tree
        
        ########################
        # TODO: your code here #
        ########################
        best_action=0
        best_ucb=float('-inf')
        for action in node.children:
            ucb = (np.sum(node.child_V_total) / node.child_V_total[action] 
                   + self.config.C*np.sqrt(2 * np.log(np.sum(node.child_N_visit) / node.child_N_visit[action])))
            if ucb>best_ucb:
                best_ucb=ucb
                best_action=best_action
        return best_action
       ########################

    def backup(self, node:MCTSNode, value:float) -> None:
        # backup the value of the leaf node to the root
        # update N_visit and V_total of each node in the path
        
        ########################
        # TODO: your code here #
        ########################
        if node.parent:
            node.parent.child_N_visit[node.action]+=1
            node.parent.child_V_total[node.action]+=value
            self.backup(node.parent, value)
        ########################    
            
    
    def rollout(self, node:MCTSNode) -> float:
        # simulate the game until the end
        # return the reward of the game
        # NOTE: the reward should be convert to the perspective of the current player!
        
        ########################
        # TODO: your code here #
        ########################
        env=node.env.fork()
        total_reward=0.0
        depth=0
        while not env._ended:
            depth+=1
            action=0
            temp=0
            while True:
                temp+=1
                action=np.random.choice(np.arange(node.n_action))
                # if not env._action_mask_cache[action]==0:
                if not env._valid_action_mask[action]==0:
                    break
                if temp==node.n_action:
                    return total_reward
            observation, reward, done=env.step(action)
            total_reward+=reward

            if depth==self.depth:
                return go_heuristic_evaluation(node.env)
            
        return total_reward
        ########################
    
    def pick_leaf(self) -> MCTSNode:
        # select the leaf node to expand
        # the leaf node is the node that has not been expanded
        # create and return a new node if game is not ended
        
        ########################
        # TODO: your code here #
        ########################
        node=self.root
        while not node.done:
            if len(node.children)==node.n_action:
                action=self.uct_action_select(node)
                node=node.children[action]
            else:
                untried_actions=[action for action in np.arange(node.n_action) if node.action_mask[action] and not action in node.children]
                new_action=np.random.choice(untried_actions)
                new_env=node.env.fork()
                observation, reward, done = new_env.step(new_action)
                new_node=MCTSNode(new_action, new_env, reward, node)
                return new_node
        return node
        ########################
    
    def get_policy(self, node:MCTSNode = None) -> np.ndarray:
        # return the policy of the tree(root) after the search
        # the policy conmes from the visit count of each action 
        
        ########################
        # TODO: your code here #
        ########################
        policy=np.array(node.child_N_visit)
        return policy/np.sum(policy)
        ########################

    def search(self):
        # search the tree for n_search times
        # eachtime, pick a leaf node, rollout the game (if game is not ended) 
        #   for n_rollout times, and backup the value.
        # return the policy of the tree after the search
        for _ in range(self.config.n_search):
            leaf = self.pick_leaf()
            value = 0
            if leaf.done:
                ########################
                # TODO: your code here #
                ########################
                value=leaf.reward
                ########################
            else:
                ########################
                # TODO: your code here #
                ########################
                total = 0.0
                for _ in range(self.config.n_rollout):
                    total+=self.rollout(leaf)
                value=total/self.config.n_rollout
                ########################
            self.backup(leaf, value)

        return self.get_policy(self.root)
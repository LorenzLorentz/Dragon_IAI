from env import *
from players import *
from mcts.uct_mcts import UCTMCTSConfig
from tqdm import trange, tqdm
import numpy as np
import time
from collections import Counter

TEST=False
SEARCH_BEST_C=False
TASK3=False
TASK4=False
TASK4_MODE=0.0
TASK5=False
TASK6=True
TASK7=False

def print_devide_line(n=50):
    print("--"*n)

def pit(game:BaseGame, player1:BasePlayer, player2:BasePlayer, log_output:bool=True):
    game.reset()
    if log_output:
        print(f"start playing {type(game)}")
        print_devide_line()
    reward = 0
    
    for player in [player1, player2]:
        if player.__class__.__name__ == 'UCTPlayer':
            player.clear()
            
    while True:
        t=time.time()
        a1 = player1.play(game)
        t=time.time()-t
        
        if player1.__class__.__name__=='UCTPlayer' and TASK5:
            with open('MCTS_task5.txt', 'a') as f:
                print(f"        time:{t}, action={a1}", file=f)
        
        if player1.__class__.__name__=='UCTPlayer' and TASK4:
            with open(f'MCTS_task4_C={TASK4_MODE}.txt', 'a') as f:
                print(a1, file=f)
        
        _, reward, done = game.step(a1)
        if player2.__class__.__name__ == 'UCTPlayer':
            player2.opp_play(a1)
        if log_output:
            if TASK6:
                print(f"Player 1 ({player1}) move: {a1}", file=open("MCTS_task6.txt", "a"))
                print(game.to_string(), file=open("MCTS_task6.txt", "a"))
                # print("--"*50, file=open("MCTS_task6.txt", "a"))
            else:
                print(f"Player 1 ({player1}) move: {a1}")
                print(game.to_string())
                print_devide_line()
        if done:
            break

        t=time.time()
        a2 = player2.play(game)
        t=time.time()-t
        
        if player1.__class__.__name__=='UCTPlayer' and TASK4:
            with open(f'MCTS_task4_C={TASK4_MODE}.txt', 'a') as f:
                print(a2, file=f)

        if player2.__class__.__name__=='UCTPlayer' and TASK5:
            with open('MCTS_task5.txt', 'a') as f:
                print(f"        time:{t}, action={a2}", file=f)

        _, reward, done = game.step(a2)
        if player1.__class__.__name__ == 'UCTPlayer':
            player1.opp_play(a2)
        if log_output:
            if TASK6:
                print(f"Player 2 ({player2}) move: {a2}", file=open("MCTS_task6.txt", "a"))
                print(game.to_string(), file=open("MCTS_task6.txt", "a"))
                # print("--"*50, file=open("MCTS_task6.txt", "a"))
            else:
                print(f"Player 2 ({player2}) move: {a2}")
                print(game.to_string())
                print_devide_line()
        if done:
            reward *= -1
            break
    if log_output:
        if reward == 1:
            print(f"Player 1 ({player1}) win")
        elif reward == -1:
            print(f"Player 2 ({player2}) win")
        else:
            print("Draw")
    return reward
        
def multi_match(game:BaseGame, player1:BasePlayer, player2:BasePlayer, n_match=100):
    print(f"Player 1:{player1}  Player 2:{player2}")
    n_p1_win, n_p2_win, n_draw = 0, 0, 0
    T = trange(n_match)
    for _ in T:
        reward = pit(game, player1, player2, log_output=False)
        if reward == 1:
            n_p1_win += 1
        elif reward == -1:
            n_p2_win += 1
        else:
            n_draw += 1
        T.set_description_str(f"P1 win: {n_p1_win} ({n_p1_win}) P2 win: {n_p2_win} ({n_p2_win}) Draw: {n_draw} ({n_draw})")        
    print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)")
    print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)")
    print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)")
    print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)")
    print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)")
    return n_p1_win, n_p2_win, n_draw
        
        
def search_best_C():
    from matplotlib import pyplot as plt
    p2nl = []
    cs = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.75, 1.0, 1.5, 2.5, 5.0]
    n_match = 100
    for c in cs:
        config = UCTMCTSConfig()
        config.C = c
        config.n_rollout = 7
        config.n_search = 64
        player1 = AlphaBetaPlayer()
        player2 = UCTPlayer(config, deterministic=True)
        game = TicTacToeGame()
        p1w, p2w, drw = multi_match(game, player1, player2, n_match=n_match)
        p2nl.append((p2w+drw)/n_match)
    plt.plot(cs, p2nl)
    plt.savefig('p2nl.png')

if __name__ == '__main__':
    #####################
    # Modify code below #
    #####################
    
    # set seed to reproduce the result
    # np.random.seed(42)

    if TEST:
        game=GoGame()
        game.reset()
        print(game.to_string())

    if SEARCH_BEST_C:
        search_best_C()

    """TASK3"""
    if TASK3:
        print("---TASK3 START---")
        game = TicTacToeGame()
        n_match=100
        config = UCTMCTSConfig()
        config.C = 1.0
        config.n_rollout = 7
        config.n_search = 64
        player1 = RandomPlayer()
        player2 = AlphaBetaPlayer()
        player3 = UCTPlayer(config, deterministic=True)
        
        n_p1_win, n_p2_win, n_draw=multi_match(game, player1, player3, n_match=n_match)
        with open('MCTS_task3.txt', 'a') as f:
            print(f"-- Player 1 ({player1}) vs Player 2 ({player3}) --", file=f)
            print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)", file=f)
            print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)", file=f)
            print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)", file=f)
            print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)", file=f)
            print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)", file=f)
            print("-- end --\n", file=f)
        
        n_p1_win, n_p2_win, n_draw=multi_match(game, player3, player1, n_match=n_match)
        with open('MCTS_task3.txt', 'a') as f:
            print(f"-- Player 1 ({player3}) vs Player 2 ({player1}) --", file=f)
            print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)", file=f)
            print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)", file=f)
            print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)", file=f)
            print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)", file=f)
            print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)", file=f)
            print("-- end --\n", file=f)

        n_p1_win, n_p2_win, n_draw=multi_match(game, player2, player3, n_match=n_match)
        with open('MCTS_task3.txt', 'a') as f:
            print(f"-- Player 1 ({player2}) vs Player 2 ({player3}) --", file=f)
            print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)", file=f)
            print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)", file=f)
            print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)", file=f)
            print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)", file=f)
            print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)", file=f)
            print("-- end --\n", file=f)
        
        n_p1_win, n_p2_win, n_draw=multi_match(game, player3, player2, n_match=n_match)
        with open('MCTS_task3.txt', 'a') as f:
            print(f"-- Player 1 ({player3}) vs Player 2 ({player2}) --", file=f)
            print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)", file=f)
            print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)", file=f)
            print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)", file=f)
            print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)", file=f)
            print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)", file=f)
            print("-- end --\n", file=f)

        n_p1_win, n_p2_win, n_draw=multi_match(game, player3, player3, n_match=n_match)
        with open('MCTS_task3.txt', 'a') as f:
            print(f"-- Player 1 ({player3}) vs Player 2 ({player3}) --", file=f)
            print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)", file=f)
            print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)", file=f)
            print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)", file=f)
            print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)", file=f)
            print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)", file=f)
            print("-- end --\n", file=f)
        
        print("---TASK3   END---")

    """TASK4"""
    if TASK4:
        print("---TASK4 START---")
        game = TicTacToeGame()
        config = UCTMCTSConfig()
        config.n_rollout = 7
        config.n_search = 64
        player1 = AlphaBetaPlayer()
        print("     TEST1: C=0.1")
        TASK4_MODE=0.1
        config.C = 0.1
        player2 = UCTPlayer(config, deterministic=True)
        multi_match(game, player1, player2, n_match=100)
        multi_match(game, player2, player1, n_match=100)
        print("     TEST1 END")
        print("     TEST2: C=5.0")
        TASK4_MODE=5.0
        config.C = 5.0
        player2 = UCTPlayer(config, deterministic=True)
        multi_match(game, player1, player2, n_match=100)
        multi_match(game, player2, player1, n_match=100)
        print("     TEST2 END")
        
        print("--- c=0.1 ----", file=open("MCTS_task4_stat.txt", "a"))
        with open('MCTS_task4_C=0.1.txt', 'r') as file:
            numbers_1 = [int(line.strip()) for line in file if line.strip().isdigit()]
        freq_1 = Counter(numbers_1)
        for num, count in sorted(freq_1.items()):
            print(f"action {num} 出现了 {count} 次", file=open("MCTS_task4_stat.txt", "a"))
        print("\n", file=open("MCTS_task4_stat.txt", "a"))
        print("--- c=5.0 ----", file=open("MCTS_task4_stat.txt", "a"))
        with open('MCTS_task4_C=5.0.txt', 'r') as file:
            numbers_2 = [int(line.strip()) for line in file if line.strip().isdigit()]
        freq_2 = Counter(numbers_2)
        for num, count in sorted(freq_2.items()):
            print(f"action {num} 出现了 {count} 次", file=open("MCTS_task4_stat.txt", "a"))

        print("---TASK4   END---")


    """TASK5"""
    if TASK5:
        print("---TASK5 START---")
        cs=[1.0, 2.5]
        rollouts=[7,13]
        searchs=[64, 200]
        n_match=10
        
        game=GoGame(7)
        player1=RandomPlayer()
        config=UCTMCTSConfig()
        result=[]
        
        for c in cs:
            for rollout in rollouts:
                for search in searchs:
                    with open('MCTS_task5.txt', 'a') as f:
                        print(f"c={c}, rollout={rollout}, search={search}", file=f)
                    config.C=c
                    config.n_rollout=rollout
                    config.n_search=search
                    player2=UCTPlayer(config=config)
                    n_p1_win_1, n_p2_win_1, n_draw_1=multi_match(game, player1, player2, n_match=n_match)
                    with open('MCTS_task5.txt', 'a') as f:
                        print(f"    second, win: {n_p2_win_1/n_match}, not lose: {(n_p2_win_1+n_draw_1)/n_match}", file=f)
                    n_p1_win_2, n_p2_win_2, n_draw_2=multi_match(game, player2, player1, n_match=n_match)
                    with open('MCTS_task5.txt', 'a') as f:
                        print(f"    first, win: {n_p1_win_2/n_match}, not lose: {(n_p1_win_2+n_draw_2)/n_match}", file=f)
                    result.append(((c,rollout,search), (n_p2_win_1+n_p1_win_2)/(2*n_match)))
        
        print("---TASK5   END---")

    """TASK6"""
    if TASK6:
        print("---TASK6 START---")
        n_trail=1
        game = GoGame(7)
        config = UCTMCTSConfig()
        config.C = 2.5
        config.n_rollout = 13
        config.n_search = 200
        player2 = AlphaBetaHeuristicPlayer()
        player1 = UCTPlayer(config, deterministic=True)
        for _ in range(n_trail):
            pit(game, player1, player2, log_output=True)
            pit(game, player2, player1, log_output=True)
        print("---TASK6   END---")

    """TASK7"""
    if TASK7:
        print("---TASK7 START---")
        n_match=10
        game = GoGame()
        config = UCTMCTSConfig()
        config.C = 2.5
        config.n_rollout = 13
        config.n_search = 200
        player1 = RandomPlayer()
        player2 = AlphaBetaHeuristicPlayer()
        player3 = UCTPlayer(config, deterministic=True)
        
        n_p1_win, n_p2_win, n_draw=multi_match(game, player1, player3, n_match=n_match)
        with open('MCTS_task7.txt', 'a') as f:
            print(f"-- Player 1 ({player1}) vs Player 2 ({player3}) --", file=f)
            print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)", file=f)
            print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)", file=f)
            print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)", file=f)
            print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)", file=f)
            print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)", file=f)
            print("-- end --\n", file=f)
        
        n_p1_win, n_p2_win, n_draw=multi_match(game, player3, player1, n_match=n_match)
        with open('MCTS_task7.txt', 'a') as f:
            print(f"-- Player 1 ({player3}) vs Player 2 ({player1}) --", file=f)
            print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)", file=f)
            print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)", file=f)
            print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)", file=f)
            print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)", file=f)
            print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)", file=f)
            print("-- end --\n", file=f)

        n_p1_win, n_p2_win, n_draw=multi_match(game, player2, player3, n_match=n_match)
        with open('MCTS_task7.txt', 'a') as f:
            print(f"-- Player 1 ({player2}) vs Player 2 ({player3}) --", file=f)
            print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)", file=f)
            print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)", file=f)
            print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)", file=f)
            print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)", file=f)
            print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)", file=f)
            print("-- end --\n", file=f)
        
        n_p1_win, n_p2_win, n_draw=multi_match(game, player3, player2, n_match=n_match)
        with open('MCTS_task7.txt', 'a') as f:
            print(f"-- Player 1 ({player3}) vs Player 2 ({player2}) --", file=f)
            print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)", file=f)
            print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)", file=f)
            print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)", file=f)
            print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)", file=f)
            print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)", file=f)
            print("-- end --\n", file=f)

        n_p1_win, n_p2_win, n_draw=multi_match(game, player3, player3, n_match=n_match)
        with open('MCTS_task7.txt', 'a') as f:
            print(f"-- Player 1 ({player3}) vs Player 2 ({player3}) --", file=f)
            print(f"Player 1 ({player1}) win: {n_p1_win} ({n_p1_win/n_match*100:.2f}%)", file=f)
            print(f"Player 2 ({player2}) win: {n_p2_win} ({n_p2_win/n_match*100:.2f}%)", file=f)
            print(f"Draw: {n_draw} ({n_draw/n_match*100:.2f}%)", file=f)
            print(f"Player 1 not lose: {n_p1_win+n_draw} ({(n_p1_win+n_draw)/n_match*100:.2f}%)", file=f)
            print(f"Player 2 not lose: {n_p2_win+n_draw} ({(n_p2_win+n_draw)/n_match*100:.2f}%)", file=f)
            print("-- end --\n", file=f)
        print("---TASK7   END---")
    #####################
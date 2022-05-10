import dobbs
import time
import numpy as np
import pandas as pd
from games import PatrolGame


def play_game(m, d, num_attacker_types, items=None, item_prob=None,
              attacker_types=None, attacker_type_prob=None, actual_attacker=0):
    count = d
    lost_items = []

    while d > 0:
        game = PatrolGame(m, d, num_attacker_types, items=items, item_prob=item_prob,
                          attacker_types=attacker_types, attacker_type_prob=attacker_type_prob)
        dob = dobbs.Dobbs(game)
        dob.solve()
        # picks best attacker move based on given attacker type
        attacker_move = dob.opt_attacker_pure_strategy[actual_attacker]
        # picks best defender strategy based on best expected payoff
        defender_move = dob.game.X[np.argmax(dob.opt_defender_mixed_strategy)][0]

        if attacker_move == defender_move:
            lost_items.append(dob.game.items[defender_move])
            m -= 1
            items.pop(defender_move)
            item_prob.pop(defender_move)
        d -= 1
    success_rate = 1 - (len(lost_items) / count)
    return lost_items, success_rate


def patrol_game_visualized(m, d, num_attacker_types, items=None, item_prob=None,
                           attacker_types=None, attacker_type_prob=None, actual_attacker=0):
    count = d
    lost_items = []
    while d > 0:
        game = PatrolGame(m, d, num_attacker_types, items=items, item_prob=item_prob,
                          attacker_types=attacker_types, attacker_type_prob=attacker_type_prob)
        print('~~' * 30)
        print(f"Beginning Run {count - d}")
        dob = dobbs.Dobbs(game)
        dob.solve()
        # picks best attacker move based on given attacker type
        attacker_move = dob.opt_attacker_pure_strategy[actual_attacker]
        # picks best defender strategy based on best expected payoff
        defender_move = dob.game.X[np.argmax(dob.opt_defender_mixed_strategy)][0]
        temp0 = list(dob.game.items.values())
        temp1 = [None] * len(dob.game.items)
        temp1[defender_move] = 'def'
        temp2 = [None] * len(dob.game.items)
        temp2[attacker_move] = 'atk'
        df = pd.DataFrame(np.stack([temp1, temp2]), columns=temp0)
        print('--'*30)
        print(f'Policy decided on: {[dob.game.items[i] for i in dob.game.X[np.argmax(dob.opt_defender_mixed_strategy)]]}')
        print(df)
        print('--' * 30)
        if attacker_move != defender_move:
            print('Defender Failed, recalculating new strategy')
            lost_items.append(dob.game.items[attacker_move])
            m -= 1
            items.pop(attacker_move)
            if len(items) == 0: break
            item_prob.pop(attacker_move)
        else:
            print('Defender Succeeded')
        d -= 1

    print(f'Items lost: {lost_items}')
    success_rate = 1 - (len(lost_items) / count)
    print(f'Success Rate for Defender: {success_rate}')
    print(f'It took {round(dob.solution_time_with_overhead,5)} seconds')
    return lost_items, success_rate


if __name__ == '__main__':
    i = 0
    score = []
    start = time.time()
    while i <= 20:
        try:
            lost, success = play_game(4, 4, 3, items=["Safe", "Camera", "Computer","Phone"], item_prob=[.7, .3, .6, .1],
                                    attacker_types=['greedy', 'silly','smart','safe'], attacker_type_prob=[.6, .2, .1, .1], actual_attacker=0)
        except:
            lost, success = play_game(4, 4, 3, items=["Safe", "Camera", "Computer","Phone"], item_prob=[.7, .3, .6, .1],
                                   attacker_types=['greedy', 'silly','smart','safe'], attacker_type_prob=[.6, .2, .1, .1], actual_attacker=0)
        print(f'finished run {i}')
        score.append(success)
        i+=1
    print('time: ', time.time() - start)
    print(score)
    tot = sum(score)
    print(tot/len(score))
    # lost, success = patrol_game_visualized(4, 4, 2, items=["Safe", "Camera", "Computer", "Phone"], item_prob=[.7, .3, .6, .3],
    #                                 attacker_types=['greedy', 'silly', 'c'], attacker_type_prob=[.6, .1, .3], actual_attacker=0)

import dobbs
import time
import numpy as np
import pandas as pd
from games import PatrolGame


def play_game(m, d, num_attacker_types, items=None, item_prob=None,
              attacker_types=None, attacker_type_prob=None, actual_attacker=None):
    count = d
    lost_items = []
    if not actual_attacker or actual_attacker >= len(attacker_types):
        actual_attacker = np.random.randint(0, len(attacker_types))
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
                           attacker_types=None, attacker_type_prob=None, actual_attacker=None):
    count = d
    lost_items = []
    if not actual_attacker or actual_attacker >= len(attacker_types):
        actual_attacker = np.random.randint(0, len(attacker_types))
    while d > 0:
        game = PatrolGame(m, d, num_attacker_types, items=items, item_prob=item_prob,
                          attacker_types=attacker_types, attacker_type_prob=attacker_type_prob)
        print('~~' * 20)
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
        temp = np.stack([temp1, temp2])
        df = pd.DataFrame(temp, columns=temp0)
        print('--'*20)
        print(f'Policy decided on: {[dob.game.items[i] for i in dob.game.X[np.argmax(dob.opt_defender_mixed_strategy)]]}')
        print(df)
        print('--' * 20)
        if attacker_move != defender_move:
            print('Defender Failed, recalculating new strategy')
            lost_items.append(dob.game.items[attacker_move])
            m -= 1
            items.pop(attacker_move)
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
    while i <= 30:
        try:
            lost, success = play_game(3, 3, 4, items=["Safe", "Camera", "Computer"], item_prob=[.7, .3, .6],
                                    attacker_types=['greedy', 'silly', 'c', 'b'], attacker_type_prob=[.6, .1, .2, .1], actual_attacker=0)
        except:
            lost, success = play_game(3, 3, 4, items=["Safe", "Camera", "Computer"], item_prob=[.7, .3, .6],
                                   attacker_types=['greedy', 'silly', 'c', 'b'], attacker_type_prob=[.6, .1, .2, .1], actual_attacker=0)
        score.append(success)
        i+=1
    print(score)
    tot = sum(score)
    print(tot/len(score))
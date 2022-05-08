import dobbs
import numpy as np
from games import PatrolGame


def play_game(m, d, num_attacker_types, items=None, item_prob=None, attacker_types=None, attacker_type_prob=None, actual_attacker = None):
    count = d
    if not actual_attacker or actual_attacker >= len(attacker_types):
        actual_attacker = np.random.randint(0, len(attacker_types))
    while d > 0:
        game = PatrolGame(m, d, num_attacker_types, items=items, item_prob=item_prob,
                          attacker_types=attacker_types, attacker_type_prob=attacker_type_prob)
        print(f"Beginning Run {count - d}")
        dob = dobbs.Dobbs(game)
        dob.solve()
        # picks best attacker move based on given attacker type
        attacker_move = dob.opt_attacker_pure_strategy[actual_attacker]
        # picks best defender strategy based on best expected payoff
        defender_move = dob.game.X[np.argmax(dob.opt_defender_mixed_strategy)][0]
        print(f'Defender at the {dob.game.items[defender_move]} || Attacker at the {dob.game.items[attacker_move]}')
        d -= 1


if __name__ == '__main__':
    play_game(4, 4, 2, items=["TV", "Computer", "Vase", "Watch"], item_prob=[.7, .6, .3, .4],
                   attacker_types=['greedy', 'silly'], attacker_type_prob=[.7, .3], actual_attacker=0)
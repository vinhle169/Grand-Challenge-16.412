# Grand Challenge 16.412

Look at requirements.txt for required packages  
or do: pip install -r requirements.txt  
  
How to use files:  
##**games.py:** 
Has multiple different classes for different types of games. Has PatrolGame
(the main one looked at for Grand Challenge Assignment) and NormalFormGame 
(representing just a regular Normal Form Game).
  
PatrolGame needs to be initialized with `m` (number of "valuables" aka the targets), `d` (the length of the patrol),
`num_attacker_types` (number of types for the follower in Stackelberg game).
Use this file by calling class with at least m, d, num_attacker_types:  
`pg = PatrolGame(3,3,2)`  
can also do:  
`pg = PatrolGame(3,3,2, items = ["Phone", "Wallet", "TV"], item_prob = [.4, .6, .6], attacker_types = ["Greedy", "Risky", "Smart"], attacker_type_prob = [.6, .3, .1])`
  
Important accessible objects from this class:  
`[pg.attacker_payoffs, pg.defender_payoffs, pg.attacker_type_probability]`  
  

## **dobbs.py:**  
A class that takes in a game class from games.py as an argument and solves the problem (aka returns optimal policies.)  
Called as  
`x = PatrolGame(4, 4, 2, items=["TV", "Computer", "Vase", "Watch"], item_prob=[.7, .6, .3, .4],
                   attacker_types=['greedy', 'silly'], attacker_type_prob=[.7, .3]) `  
`dob = Dobbs(x)`  
`dob.solve()`
`dob.opt_attacker_pure_strategy`  
`dob.opt_defender_mixed_strategy`  
In order to get the exact best strategy for defender you can do this:  
    `strat = np.argmax(dob.opt_defender_mixed_strategy)`  
    `print(dob.game.X[strat])`  
  
## **play_stackelberg.py:**  
Use functions in script with same arguments as PatrolGame, to test DOBSS.  
`patrol_game_visualized` will show you the game as verbosely as possible.
`play_game` will simply just play through the game.  
Both return list of lost items and float of success rate.



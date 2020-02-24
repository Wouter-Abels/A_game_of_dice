# Loading the random integer function from the random module to roll the dice.
from random import randint

# The statics and variables for the game.
config = {'players': 2, 'target_score': 10000, 'scoring': {'1': 100,'5': 50,'111': 1000,'222': 200,'333': 300,'444': 400,'555': 500,'666': 600}, 'first_to_goal': -1, 'game_over': False}
scores = [0] * config['players']

# The title screen where the game can be started and the rules can be shown.
def menuChoice():
  print('\nA Game of Dice!\n\nOption 1: Show the rules\nOption 2: Start new games\nOption 3: Quit\n')
  choice= int(input('Please choose an option?\n'))
  while int(choice) < 1 or int(choice) > 3:
    print('\nPlease choose a valid option, enter a number between 1 and 3.')
    choice=input()
  return choice

# When option 1 is chosen from the title screen the rules of the game will be shown.
def displayRules():
  print('\nWelcome to a Game of Dice!\n\nIn this dice game the player that reaches 10,000 points first wins the game, two players take turns rolling six dice.\nThe scoring of the points is as followed:\n\tOnes are worth 100 points.\n\tFives are worth 50 points.\n\tThree of a kind are worth 100 times the die value.\n\nAt least one scoring die must be selected to continue the turn.\nWhen points are selected the player can choose between banking these points and end their turn or roll again to score more points with the risk of losing all their points of the turn and losing the turn.\n\nWhen no points are rolled, the players turn is a bust and the turn will go to the other player.\n\nHave fun playing!')

# The loop to keep the game running. When player hits target score the last round starts and when this ends loop will break.
def playGame():
  print('\nWelcome to a Game of Dice!\n')
  while not config['game_over']:
      for player in range(config['players']):
          if config['first_to_goal'] == player:
              config['game_over'] = True
              break
        
          #The start of every round when not game over.
          print('Scores:\n\t{}\n\n---- Player {}\'s turn ----'.format('\n\t'.join('Player {}: {}'.format(player, score) for player, score in enumerate(scores, 1)), player + 1))
          dice_left, turn_score, turn_over = 6, 0, False
        
          # As long as a new turn starts or there are points earned with the with the previous throw the dice will be trown. 
          while not turn_over:
              dice_left = dice_left or 6
              roll = ''.join(str(randint(1,6)) for __ in range(dice_left))
            
              # The thrown dice will be printed for the player to choose. Also, the scoring of the dice will be calculated.
              print('\n{}Player {} rolled: {}\n'.format(('[LAST TURN] ' if config['first_to_goal'] >= 0 else ''), player + 1, ', '.join(roll)))
              chose_one, roll = False, ''.join(sorted(roll))
              while True:
                  combos = [(combo,value) for combo,value in config['scoring'].items() if combo in ''.join(sorted(roll))]
                
                  # When no points are rolled the turn is over and no points will be banked. The if loop will break and the turn will shift to the next player.
                  if not combos and not chose_one:
                      print('\n---- BUST! ----\n')
                      turn_over = True
                      break 
                
                 # After a roll of the dice the dice remaining will be displayed and the player will have a choice what to do with the thrown dice. Depending on the possible points that can be selected the player can enter a number that corresponds with the combo. When R or r is entered the dice will be rolled again but only when a player has already scored points. Entering an E or e selects to end the turn and bank the score.                      
                  print('Dice remaining: {}\n{}'.format(', '.join(roll), '\n'.join('{}) {}: {} points'.format(i, ', '.join(combo), value) for i, (combo, value) in enumerate(combos, 1))))
                
                 # Input to roll again or end turn and bank score.
                  if chose_one: print('R) Roll again\nE) End turn and bank score')
                  while True:
                      choice = input('\nChoose? ')
                    
                      # When E or e is entered the score is banked and the turn for the player is over, thus the loop will break and the other player will start a new turn.
                      if chose_one and choice in 'eE':
                        scores[player], turn_over = scores[player] + turn_score, True
                        break
                    
                     # When R or r is entered the loop will be broken and the dice will be rolled again
                      if chose_one and choice in 'rR': break

                     # When a number corresponding to the point combo is chosen the loop wil be broken and the player has to make a choice again to select more points, roll again or end the turn and bank the points.
                      if combos and choice in (str(i + 1) for i in range(len(combos))):
                          chose_one, roll = True, roll.replace(combos[int(choice) - 1][0], '', 1)
                          break

                  # If the turn is over or the player choses to roll again the loop will be broken, or the scores for both the dice left and the turn core will be calculated.        
                  if turn_over or choice in 'rR': break
                  dice_left -= len(combos[int(choice) - 1][0])
                  turn_score += combos[int(choice) - 1][1]

                  # The points so far and banked will be printed next to the players number.
                  print('\nPlayer {}: {} points so far this turn, {} banked'.format(player + 1, turn_score, scores[player]))
        
          # When a player reaches the target score and is the first to do so  the game will start the final round and will display the corresponding information.
          if scores[player] >= config['target_score'] and config['first_to_goal'] == -1:
              config['first_to_goal'] = player
              print('\n---- Player {} reached the target score! Last round of a Game of Dice! ----\n'.format(player + 1))

  # Final game statistics and congratualtions to the winner.
  print('\nGAME OVER!\n\nFinal scores:\n\tplayer {}\n\nWinner: Player {}, Congratualations you won a Game of Dice!\nReady for a new game?\n\n'.format('\n\tplayer '.join('{}: {}'.format(player, score) for player, score in enumerate(scores, 1)), ', '.join(str(i + 1) for i, score in enumerate(scores) if score == max(scores))))

# The title screen program with the text for option 3: quit. 
option = menuChoice()
print(option)
while option != 3:
  if option == 1:
    displayRules()
    print()
  else:
    playGame()
    menuChoice()
  option = menuChoice()
print('\nThanks for playing, goodbye!')
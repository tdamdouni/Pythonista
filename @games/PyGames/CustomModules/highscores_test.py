print('=' * 20)
import HighScores
reload(HighScores)  # This is a best practice

high_scores = HighScores.HighScores()

high_scores.print_scores()
print('-' * 20)
for score in (-99.6, -99.5, -99, -9, -1, -0, 0, 1, 9, 99, 99.5, 99.6):
    print('Input: {} ========'.format(score))
    if high_scores.is_high_score('int', int(score)):
        print('Congratulations on your new high score!')
    #highscores.save_score('str_int', str(int(score)))  # strings now raise an exception
    if high_scores.is_high_score('float', float(score)):
        print('Congratulations on your new high score!')
    #highscores.save_score('str_float', str(float(score)))  # strings now raise an exception
    high_scores.print_scores()

lessons_learned = '''====================
For positive values:
    int(n), str(int(n)), float(n), str(float(n)) all work correctly.
For negative values:
    Only int(n) and float(n) work correctly.
Recommendation:
    Always pass an int or float as the second value to highscores.is_high_score()
Added a try / except block to reject nonnumeric scores'''
print(lessons_learned)

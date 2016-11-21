HighScores
==========

High Scores module mainly for games, Special thanks to [cclauss][1] for his contributions. 

This module contains a HighScores class that supports three main public methods:
+ `__init__([file_name])` which takes an optional name for the file used to record the high scores.
+ `is_high_score(username, score)` will return True if this is the first score or the highest score for this user.  Otherwise, False will be returned.  The `score` parameter should be numeric (int, long, float, etc.) and NOT a string.
+ `print_scores()` prints out a sorted, formatted list of all users with their high scores

[1]: https://github.com/cclauss

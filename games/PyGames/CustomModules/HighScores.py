import pickle, ui

user_name = None

class UserNameView(ui.View):
    def __init__(self, default_user_name='Name'):
        self.name = 'Enter your username:'
        self.background_color = 0.40, 0.80, 1.00
        self.label = ui.Label(frame=(12, 100, 2000, 55))
        self.label.text = 'What is your name?'
        self.label.text_color = 0.00, 0.00, 0.00
        self.label.font = ('Avenir-Black', 55)
        self.add_subview(self.label)
        self.text_field = ui.TextField(frame=(155, 175, 200, 32))
        self.text_field.text = default_user_name
        self.text_field.text_color = 0.50, 0.50, 0.50
        self.text_field.clear_button_mode = 'while_editing'
        self.add_subview(self.text_field)
        button = ui.Button(background_color='white',
                   frame=(360, 175, 75, 32),
                   image=ui.Image.named('ionicons-arrow-right-a-32'))
        button.action = self.button_tapped
        self.add_subview(button)
        self.present(style='sheet', hide_title_bar=True) # dismiss it with a two-finger swipe down gesture
        self.wait_modal()

    def button_tapped(self, sender):
        self.close()

    def will_close(self):
        global user_name
        user_name = self.text_field.text

class HighScores(object):
    def __init__(self, in_file_name = 'highscores'):
        self.file_name = in_file_name
        file_ext = '.pkl'
        if not self.file_name.endswith(file_ext):
            self.file_name += file_ext
        self.high_scores = self.__load_scores()

    def __load_scores(self):  # private function
        try:
            with open(self.file_name, 'rb') as in_file:
                return pickle.load(in_file)
        except IOError:
            return {}

    def __save_scores(self):  # private function
        with open(self.file_name, 'wb') as out_file:
            pickle.dump(self.high_scores, out_file)

    def is_high_score(self, name, score):
        try:
            curr_high_score = self.high_scores.get(name, score-1)
        except TypeError:
            raise TypeError('The score arguement must be a number.')
        is_new_high_score = score > curr_high_score
        if is_new_high_score:
            self.high_scores[name] = score
            self.__save_scores()
        return is_new_high_score

    def print_scores(self):
        score_line = '{{name:>{col_width}}} | {{score}}'.format(col_width=(80-3)//2)
        scores_sorted = sorted(zip(self.high_scores.values(),
                                   self.high_scores.keys()), reverse=True)
        for score, name in scores_sorted:
            print(score_line.format(name=name, score=score))

if __name__ == '__main__':  # this is run on run only
    # trying to do raw_input _after_ ui is not working correctly
    score = int(raw_input('Score: '))
    while not user_name:
        UserNameView()
    
    high_scores = HighScores('testing')
    if high_scores.is_high_score(user_name, score):
        print('Congratulations {} on your new high score!'.format(user_name))
    high_scores.print_scores()

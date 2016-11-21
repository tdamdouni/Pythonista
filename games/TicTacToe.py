# coding: utf-8

import console, random, ui

class TicTacToeView(ui.View):
    def __init__(self):
        self.present('sheet')
        self.image_x = ui.Image.named('ionicons-close-256')
        self.image_o = ui.Image.named('ionicons-ios7-circle-outline-256')

    def did_load(self):
        buttons = ['square{}'.format(i) for i in xrange(1,10)]
        self.squares = [self[button] for button in buttons]
        for square in self.squares:
            square.action = self.square_tapped
            square.title = ''

    def square_tapped(self, sender):
        sender.image = self.image_o if sender.image == self.image_x else self.image_x
        winner = self.winner_check()
        if winner:
            console.hud_alert('The winner is {}'.format(winner))
            ui.delay(self.clear_all_squares, 1)

        self.computer_pick()
        winner = self.winner_check()
        if winner:
            console.hud_alert('The winner is {}'.format(winner))
            ui.delay(self.clear_all_squares, 1)

    def empty_square_count(self):
        return sum([int(square.image == None) for square in self.squares])

    def computer_pick(self):
        assert self.empty_square_count(), 'Game Over: No empty squares'
        while True:
            square = random.choice(self.squares)
            if not square.image:
                square.image = self.image_o
                break

    def winner_check(self):
        tic_tac_toe = ((1, 2, 3), (4, 5, 6), (7, 8, 9),
                       (1, 4, 7), (2, 5, 8), (3, 6, 9),
                       (1, 5, 9), (3, 5, 7))
        for ttt in tic_tac_toe:
            a, b, c = [self.squares[ttt[i]-1] for i in xrange(3)]
            if a.image and a.image == b.image and a.image == c.image:
                return 'X' if a.image == self.image_x else 'O'
        return None

    def clear_all_squares(self):
        for square in self.squares:
            square.image = None

ui.load_view()

# coding: utf-8

# https://gist.github.com/offe/95d9189cc62bb9d268e7

# Kommentar 2

from scene import *

A = Action


class CreditsScene(Scene):
    def setup(self):
        SpriteNode(color='midnightblue', parent=self, size=self.size).anchor_point=(0,0)
        LabelNode('Credits', position=(self.size * (0.5, 0.9)),
            font=('Helvetica', self.size[1]/20), parent=self)
        self.back_node = SpriteNode('iow:ios7_undo_256',
            scale=self.size[1]/768.0*.6, position=self.size*(0.1, 0.9), parent=self)

    def touch_ended(self, touch):
        if touch.location in self.back_node.frame:
            self.dismiss_modal_scene()


class SettingsScene(Scene):
    def setup(self):
        SpriteNode(color='midnightblue', parent=self, size=self.size).anchor_point=(0,0)
        LabelNode('Settings', position=(self.size * (0.5, 0.9)),
            font=('Helvetica', self.size[1]/20), parent=self)
        self.back_node = SpriteNode('iow:ios7_undo_256', scale=self.size[1]/768.0*.6,
            position=self.size*(0.1, 0.9), parent=self)

    def touch_ended(self, touch):
        if touch.location in self.back_node.frame:
            self.dismiss_modal_scene()


class NewHighScoreScene(Scene):
    def __init__(self, score):
        self.score = score

    def setup(self):
        SpriteNode(color='black', parent=self, size=self.size).anchor_point=(0,0)
        LabelNode('New High Score!', position=(self.size[0]/2, self.size[1]*0.9),
                            font=('Helvetica', self.size[0]/20), parent=self)
        LabelNode(str(self.score), position=(self.size[0]/2, self.size[1]*0.4),
                            font=('Helvetica', self.size[1]/2), parent=self)

    def touch_ended(self, touch):
        self.dismiss_modal_scene()


class PlayScene(Scene):
    def __init__(self):
        self.score = 0

    def setup(self):
        SpriteNode(color='lightgrey', parent=self, size=self.size).anchor_point=(0,0)
        self.up_node = LabelNode('+1', position=(self.size * (0.25, 0.5)),
            font=('Helvetica', self.size[1]*0.3), parent=self)
        self.game_over_node = LabelNode('Game Over',
            position=(self.size * (0.75, 0.5)), font=('Helvetica', self.size[1]*0.08), parent=self)
        self.score_node = LabelNode(str(self.score), position=(self.size * (0.05, 0.95)),
                            font=('Helvetica', self.size[1]*0.08), parent=self)
        self.update_score()

    def update_score(self):
        self.score_node.text = str(self.score)

    def touch_ended(self, touch):
        if touch.location in self.up_node.frame:
            self.score += 1
            self.update_score()
        elif touch.location in self.game_over_node.frame:
            self.presenting_scene.game_score = self.score  # send score to main_menu
            self.dismiss_modal_scene()


class MainMenuScene(Scene):
    def __init__(self):
        self._game_score = self._high_score = 0

    @property
    def high_score(self):
        return self._high_score

    @high_score.setter
    def high_score(self, high_score):
        self._high_score = high_score
        self.score_node.text = 'High Score: %d' % high_score
        if high_score:
            self.present_modal_scene(NewHighScoreScene(high_score))

    @property
    def game_score(self):
        return self._game_score

    @game_score.setter
    def game_score(self, game_score):
        self._game_score = game_score
        if game_score > self.high_score:
            self.high_score = game_score

    def setup(self):
        LabelNode('The Game', position=(self.size * (0.5, 0.9)),
                            font=('Helvetica', self.size[1]*0.1), parent=self)
        self.play_node = SpriteNode('iow:play_256',
            position=self.size*(0.5, 0.5), scale=self.size[1]/768.0*1.0, parent=self)
        self.settings_node = SpriteNode('iow:ios7_gear_256',
            position=self.size*(0.3, 0.2), scale=self.size[1]/768.0*0.8, parent=self)
        self.credits_node = SpriteNode('iow:information_circled_256',
            position=self.size*(0.7, 0.2), scale=self.size[1]/768.0*0.7, parent=self)
        self.score_node = LabelNode('High Score: 0', position=(self.size*(0.5, 0.8)),
            font=('Helvetica', self.size[1]*0.08), parent=self)
        self.high_score = self._high_score

    def touch_ended(self, touch):
        if touch.location in self.play_node.frame:
            self.present_modal_scene(PlayScene())
        elif touch.location in self.settings_node.frame:
            self.present_modal_scene(SettingsScene())
        elif touch.location in self.credits_node.frame:
            self.present_modal_scene(CreditsScene())


if __name__ == '__main__':
    run(MainMenuScene())

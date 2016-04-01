# coding: utf-8

# https://gist.github.com/offe/95d9189cc62bb9d268e7

# Kommentar 1

from scene import *

A = Action

class MainMenuScene(Scene):
    def __init__(self):
        self._high_score = 0

    @property
    def high_score(self):
        return self._high_score

    @high_score.setter
    def high_score(self, high_score):
        self._high_score = high_score
        if self.score_node.children:
            self.score_node.children[0].remove_from_parent()
        LabelNode('High Score: %d' % self._high_score, position=(self.size * (0.5, 0.8)),
                            font=('Helvetica', self.size[1]*0.08), parent=self.score_node)

    def setup(self):
        SpriteNode(color='midnightblue', parent=self, size=self.size).anchor_point=(0,0)
        LabelNode('The Game', position=(self.size * (0.5, 0.9)),
                            font=('Helvetica', self.size[1]*0.1), parent=self)
        self.play_node = SpriteNode('iow:play_256',
            position=self.size*(0.5, 0.5), scale=self.size[1]/768.0*1.0, parent=self)
        self.settings_node = SpriteNode('iow:ios7_gear_256',
            position=self.size*(0.3, 0.2), scale=self.size[1]/768.0*0.8, parent=self)
        self.credits_node = SpriteNode('iow:information_circled_256',
            position=self.size*(0.7, 0.2), scale=self.size[1]/768.0*0.7, parent=self)
        self.score_node = Node(parent=self)
        self.high_score = self._high_score

    def touch_ended(self, touch):
        if touch.location in self.play_node.frame:
            self.dismiss_modal_scene()
        elif touch.location in self.settings_node.frame:
            self.present_modal_scene(SettingsScene())
        elif touch.location in self.credits_node.frame:
            self.present_modal_scene(CreditsScene())


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


class PlayScene(Scene):
    def __init__(self, main_menu):
        self.main_menu = main_menu
        self.score = 0

    def setup(self):
        self.up_node = LabelNode('+1', position=(self.size * (0.25, 0.5)),
            font=('Helvetica', self.size[1]*0.3), parent=self)
        self.game_over_node = LabelNode('Game Over',
            position=(self.size * (0.75, 0.5)), font=('Helvetica', self.size[1]*0.08), parent=self)
        self.score_node = LabelNode(str(self.score), position=(self.size * (0.05, 0.95)),
                            font=('Helvetica', self.size[1]*0.08), parent=self)
        self.update_score()
        if self.main_menu:
            self.present_modal_scene(self.main_menu)

    def update_score(self):
        self.score_node.text = str(self.score)

    def touch_ended(self, touch):
        if touch.location in self.up_node.frame:
            self.score += 1
            self.update_score()
        elif touch.location in self.game_over_node.frame:
            if self.score > self.main_menu.high_score:
                self.main_menu.high_score = self.score
                self.present_modal_scene(NewHighScoreScene(self.score))
            self.present_modal_scene(self.main_menu)


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


if __name__ == '__main__':
    run(PlayScene(MainMenuScene()))
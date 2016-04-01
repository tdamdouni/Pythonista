import unittest
import todoflow.colors as colors


class ColorsTest(unittest.TestCase):
    red = '\033[31m'
    blue = '\033[34m'
    defc = '\033[0m'

    def text(self, text):
        self.text = text
        return self

    def colored_with(self, color):
        self.text = color(self.text)
        return self

    def should_start_with(self, prefix):
        self.assertTrue(self.text.startswith(prefix))
        return self

    def should_end_with(self, suffix):
        self.assertTrue(self.text.endswith(suffix))
        return self

    def shouldnt_end_with(self, suffix):
        self.assertFalse(self.text.endswith(suffix))
        return self

    def test_constants(self):
        self.assertTrue(colors.RED)
        self.assertEqual(colors.RED, self.red)

    def test_functions(self):
        self.text('some text').colored_with(colors.red).should_start_with(
            self.red
        ).should_end_with(self.defc)

    def test_doesnt_add_unnecassary_defc(self):
        self.text('some text' + self.defc).colored_with(colors.blue).should_start_with(
            self.blue
        ).should_end_with(self.defc).shouldnt_end_with(self.defc + self.defc)


def print_colors():
    for k in colors.foreground_codes:
        print(getattr(colors, k)('this is ' + k))
    for k in colors.background_codes:
        print(getattr(colors, 'on_' + k)('this is on ' + k))
    for fk in colors.foreground_codes:
        for bk in colors.background_codes:
            print(getattr(colors, fk + '_on_' + bk)('this is ' + fk + ' on ' + bk))


if __name__ == '__main__':
    print_colors()
    unittest.main()

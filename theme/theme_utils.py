"""Utilities for working with the current theme""" 

from objc_util import *
import os
import json
import ui
import re
from PIL import ImageColor


# GLOBALS

THEME = None

# When styling uis...
# These should have background colors the same as the background
UI_BGTYPES = (
    ui.View,
    ui.Label,
    ui.ImageView,
    ui.ScrollView,
    ui.NavigationView,
    ui.TableView,
    ui.WebView
)
# These should have clear backgrounds
UI_CLEARTYPES = (
    ui.ActivityIndicator,
    ui.Slider,
    ui.DatePicker,
    ui.Switch
)


# THEME LOADING
# Some of this code is adapted from @omz's "Pythonista Theme Editor"

def _clean_json(string):
    """Remove trailing commas from JSON. This is necessary because some of the
    default themes have this in them. I guess Python's JSON parser is stricter
    than Objective-C's..."""
    # From http://stackoverflow.com/questions/23705304
    string = re.sub(",[ \t\r\n]+}", "}", string)
    string = re.sub(",[ \t\r\n]+\]", "]", string)
    return string


def get_theme():
    """Return absolute path of the JSON file for the current theme"""
    # Name of current theme
    defaults = ObjCClass("NSUserDefaults").standardUserDefaults()
    name = str(defaults.objectForKey_("ThemeName"))

    # Theme is user-created
    if name.startswith("User:"):
        home = os.getenv("CFFIXED_USER_HOME")
        user_themes_path = os.path.join(home,
                                        "Library/Application Support/Themes")
        theme_path = os.path.join(user_themes_path, name[5:] + ".json")
    # Theme is built-in
    else:
        res_path = str(ObjCClass("NSBundle").mainBundle().resourcePath())
        theme_path = os.path.join(res_path, "Themes2/%s.json" % name)
    # Read theme file
    with open(theme_path, "r") as f:
        data = f.read()
    # Return contents
    return data


def _reload_theme():
    """Reload theme. This happens whenever the script is run."""
    global THEME
    THEME = json.loads(_clean_json(get_theme()))


def load_theme():
    """Return loaded JSON of the current theme. Note that for efficiency, this
    is stored internally, and only updates when you restart your script."""
    global THEME
    if THEME is None:
        _reload_theme()
    return THEME


# Functions for getting colors from the theme

def get_theme_name():
    return load_theme()["name"]


def _get_color_scheme():
    theme = load_theme()
    colors = [
        theme["library_background"],
        theme["tab_background"],
        theme["background"],
        theme["bar_background"],
    ]
    return colors


def get_color_scheme():
    colors = _get_color_scheme()
    # Add leading # to hex values if needed, lowercase, and sort
    return sorted(
        [("" if c.startswith("#") else "#") + c.lower() for c in colors],
        reverse=theme_is_light()
    )


def get_tint():
    """Get the tint color for the current theme"""
    return load_theme()["tint"]


def theme_is_light():
    """Is the theme light colored"""
    colors = _get_color_scheme()
    colors = [ImageColor.getrgb(c) for c in colors]
    lums = [float(sum(c)) / len(c) for c in colors]
    brightness = sum(lums) / len(lums)
    return brightness > 130


def theme_is_dark():
    """Is the theme dark colored"""
    return not theme_is_light()


# UI theming functions

def _set_keyboard_darkness(v, dark=True):
    if isinstance(v, ui.TextView):
        ObjCInstance(v).setKeyboardAppearance_(dark)
    elif isinstance(v, ui.TextField):
        ObjCInstance(v).subviews()[0].setKeyboardAppearance_(dark)


def _determine_bgcolor(view, colors):
    """ Decide what background color we should assign a view when styling it.
    Returns either clear, the theme's background, or a contrast-y color. """
    # Is the view in question one of the types which should have opaque
    # backgrounds?
    if any([type(view) == t for t in UI_BGTYPES]):
        return colors[0]
    # Is the view in question one of the types which should have transparent
    # backgrounds?
    elif any([type(view) == t for t in UI_CLEARTYPES]):
        return (0, 0, 0, 0)
    # Other elements should stand out from the background
    else:
        return colors[2]


def _style_ui_component(view, respect_changes=False):
    """ Style a single UI element to match the theme. Used only internally, you
    should use style_ui instead, even on single elements. """
    ignore_changes = not respect_changes

    colors = get_color_scheme()
    bg = _determine_bgcolor(view, colors)

    # Apply styles.
    # Already-changed values won't be overriden if respect_changes is true

    # Background
    if view.background_color == (0, 0, 0, 0) or ignore_changes:
        # TextField background color does not show unless 'bordered' is off, so
        # we have to fix that ourselves
        if isinstance(view, ui.TextField):
            view.bordered = False
            view.corner_radius = 5
        view.background_color = bg

    # Tint
    if view.tint_color == (0, 0.47843137254901963, 1, 1) or ignore_changes:
        view.tint_color = get_tint()

    # Border color
    if view.border_color == (0, 0, 0, 1) or ignore_changes:
        view.border_color = colors[3]

    # Color for text on Labels/TextFields/TextViews with dark theme
    flagged_types = (ui.TextField, ui.TextView, ui.Label)
    should_change_color = isinstance(view, flagged_types) or ignore_changes
    if should_change_color and theme_is_dark():
        view.text_color = "#cccccc"

    # Color for text on DatePickers with dark theme
    if theme_is_dark() and type(view) == ui.DatePicker:
        o = ObjCInstance(view)
        color = ObjCClass("UIColor").colorWithHexString_("cccccc")
        o.setValue_forKey_(color, "textColor")


def style_ui(view, respect_changes=False):
    """ Recursively style a view and its children according to the current
    theme. When respect_changes is true, any elements with non-default styles
    are preserved; only elements with the default styles are changed. """
    _style_ui_component(view, respect_changes)
    for sv in view.subviews:
        style_ui(sv)


# Tests

def test():
    from PIL import Image
    # Print tests to console

    # Name of theme
    print("Theme:", get_theme_name())
    # Light or dark
    print("It's a {} theme".format("light" if theme_is_light() else "dark"))
    # Dominant colors
    print("Dominant colors", get_color_scheme(),
          "with a tint color of", get_tint())
    # Squares of color for the color scheme
    images = [Image.new("RGB", (100, 100), c) for c in get_color_scheme()]
    palette = Image.new("RGB", (504, 100))
    for i, im in enumerate(images):
        palette.paste(im, (i * 101, 0))
    palette.show()


def test_ui():
    v = ui.load_view()
    style_ui(v)
    v.present("sheet")


if __name__ == "__main__":
    test()
    test_ui()

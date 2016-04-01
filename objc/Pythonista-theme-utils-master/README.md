# theme-utils
This is a module called `theme_utils` that makes it easy to work with themes, as well as making it easy to style UI components with these themes. 

# The module
The module consists of two main parts, but they're in the same namespace.

1. Utilities for getting attributes of the current user theme. These include ready-made functions for accessing the most useful and common attribute of the theme, as well as lower-level functions like `load_theme` that can help with more specific use cases (like getting the colors of the code syntax). These include:
    - `load_theme`- return a Python `dict` representing the current theme
    - `get_theme_name` - return the name of the current theme
    - `get_tint` - return the tint color of the current theme
    - `get_color_scheme` - return a color scheme to go with the current theme. This consists of four colors, the editor background color, the library background color, the top bar's color, and the color of the backgrounder tabs. These are sorted by "intensity," which is dark to light for "dark themes" and light to dark for "light themes"
    - `theme_is_light` and `theme_is_dark`- is the theme a light theme, or a dark theme. Judged by averaging intensities of the 4 main colors, from `get_color_schemes`
2. Utilities for styling `ui`s to match the current theme. 
    -`style_ui(view)`, and `view` (and its children) will be styled to match the current theme. 

# Examples
***Solarized Light***:
![](http://i.imgur.com/O9pLYGa.jpg)
***Tomorrow Night***:
![](http://i.imgur.com/cq3rf63.jpg)

Running the script as-is will output some useful information about the current theme:
![](http://i.imgur.com/iQk5yQV.jpg)

# Custom themes
All of these functions work flawlessly with custom themes, built with @omz's [Pythonista Theme Editor](https://gist.github.com/omz/6c168b0c36ca3b23cacc).

***Pacific Dark***:
![](http://i.imgur.com/X3hTrC6.jpg)


This will likely be merged into `Pythonista-Tweaks` as part of the theme functionality, but that will be after there is much more control over these things.

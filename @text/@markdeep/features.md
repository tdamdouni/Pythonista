                      **Markdeep Feature Demo**
                           Morgan McGuire                  

This document shows the features of
[Markdeep](http://casual-effects.com/markdeep).  Markdeep is a text
formatting syntax that extends Markdown, and a Javascript program for
making it work in browsers. The two most powerful features are its
ability to run in any web **browser** on the client side and the
inclusion of **diagrams**.

[Click here](features.md.html?noformat) to see this document without
automatic formatting.

Markdown is free and easy to use. It doesn't need a plugin, or
Internet connection. There's nothing to install. Just start
writing in Vi, Nodepad, Emacs, Visual Studio, Atom, or another
editor! You don't have to export, compile, or otherwise process
your document.

Section Header
=======================================================================================
Text formatting: **bold**, __bold__, *italic*, _italic_,
~~strikethrough~~, [hyperlink](http://casual-effects.com), `inline
code`.

Hyperlinked explicit URL <http://casual-effects.com> and
e-mail <president@whitehouse.gov>.

Markdeep intelligently does not apply bold or italic formatting to
math expressions such as x = 3 * y - 2 * z or WORDS_WITH_INTERNAL_UNDERSCORES.
It also protects HTML `<tags>` in code blocks from disappearing.

Subsection Header
---------------------------------------------------------------------------------------
Lists and floating diagrams:
                                                   *****************************
1. Monday                                          *   A         B         C   *
2. Tuesday                                         *   *-------->o<------->o   *
  1. Morning                                       *   ^        / ^        |   *
  2. Afternoon                                     *   |       v   \       v   *
3. Wednesday                                       *   o----->o---->o<---->*   *
  - Bullets                                        *   D      E     F      G   *
  - Bullets                                        *****************************
4. Thursday
5. Friday

Ut at felis diam. Aliquam massa odio, pharetra ut neque sed, commodo
dignissim orci. Curabitur quis velit gravida, blandit diam nec,
lacinia quam. Maecenas pharetra, velit in vestibulum auctor, diam
ipsum suscipit arcu, non sodales orci nibh sit amet leo. Nulla dictum.

- Bread
- Fish
- Milk
- Cheese

> This is an indented blockquote: Ut at felis diam. Aliquam massa odio, pharetra ut neque sed, commodo
> dignissim orci. Curabitur quis velit gravida, blandit diam nec,
> lacinia quam. Maecenas pharetra, velit in vestibulum auctor, diam
> ipsum suscipit arcu, non sodales orci nibh sit amet leo. Nulla dictum

Lists can also:

* Use asterisks
* Instead of
* Minus signs

Images
------------------------------------------------------------------------------

There's no natural way to embed an image into something that is readable as a text
document. Markdeep follows markdown's somewhat reasonable syntax:

![A picture of a robot](robot.jpg)

or, just use a raw HTML `<img>` tag, which allows better format control:

<img src="robot.jpg" width="128" border="1"/>


Fenced Code Blocks
------------------------------------------------------------------------------

Fenced code blocks with syntax coloring and automatic programming
language detection:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
void insertion_sort(int data[], int length) {
    for (int i = 0; i < length; ++i) {
        for (int j = i; (j > 0) && (data[j] < data[j - 1]); --j) {
            int temp = data[j];
            data[j] = data[j - 1];
            data[j - 1] = temp;
        }
    }
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Alternative back-tick markup:

````````````````````````````````````
def insertionSort(data):
    for i in range(0, len(data)):
        j = i;
        while (j > 0) and (data[j] < data[j - 1]):
            temp = data[j]
            data[j] = data[j - 1]
            data[j] = temp
            --j
````````````````````````````````````

You can even have HTML in a code block:

````````````````````````````````````
<b>Show this</b> HTML as <i>source</i>,
<code>not code</code>.
````````````````````````````````````

...and of course, Markdeep inside Markdeep (although the syntax coloring sometimes goes crazy):

````````````````````````````````````
- Do not 
- Format
  - this as a **list**!
````````````````````````````````````


Tables
------------------------------------------------------------------------------

 Maine | Iowa | Colorado 
-------|------|----------
   1   |  4   |   10
  ME   |  IA  |   CO
 Blue  | Red  | Brown


Definition Lists
------------------------------------------------------------------------------

Apple
:   Pomaceous fruit of plants of the genus Malus in 
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.


Diagrams
--------------------------------------------------------------------------------

Diagrams can be inserted alongside, as in this      ****************************
example, or between paragraphs of text as shown     * .---------.              *
below.                                              * |  Server |<------.      *
                                                    * '----+----'       |      *
The diagram parser leaves symbols used as labels    *      |            |      *
unmodified, so characters like > and ( can appear   *      | DATA CYCLE |      *
inside of the diagram. In fact, any plain text      *      v            |      *
may appear in the diagram. In addition to labels,   *  .-------.   .----+----. *
any un-beautified text will remain in place for     * | Security|  |  File   | *
use as ASCII art. Thus, the diagram is rarely       * | Policy  +->| Manager | *
distored by the beautification process.             *  '-------'   '---------' *
                                                    ****************************

*************************************************************************************************
*.-------------------.                           ^                      .---.                   *
*|    A Box          |                           |                      |   |                   *
*|                   |                           v                      |   |                   *
*'-------------------'                                                  |   |                   *
*                       Round                                       *---(-. |                   *
*  .-----------------.  .-------.    .----------.         .-------.     | | |                   *
* |   Mixed Rounded  | |         |  / Diagonals  \        |   |   |     | | |                   *
* | & Square Corners |  '--. .--'  /              \       |---+---|     '-)-'       .--------.  *
* '--+------------+-'  .--. |     '-------+--------'      |   |   |       |        / Search /   *
*    |            |   |    | '---.        |               '-------'       |       '-+------'    *
*    |<---------->|   |    |      |       v                Interior       o         |     ^     *
*    '           <---'      '----'   .-----------.              ---.     .---       v     |     *
* .------------------.  Diag line    | .-------. +---.              \   /           .     |     *
* |   if (a > b)     +---.      .--->| |       | |    | Curved line  \ /           / \    |     *
* |   foo->bar()     |    \    /     | '-------' |<--'                +           /   \   |     *
* '------------------'     '--'      '--+--------'      .--. .--.     |  .-.     +Done?+-'      *
*    .---+-----.                        |   ^           |\ | | /|  .--+ |   |     \   /         *
*    |   |     | Join                   |   | Curved    | \| |/ | |    \    |      \ /          *
*    |   |     +---->                    '-'  Vertical  '--' '--'  '--  '--'        +  .---.    *
*    '---+-----'                                                                    |  | 3 |    *
*                                                    not:line    'quotes'        .-'   '---'    *
*                                            /            A || B   *bold*       |        ^      *
*                                       <---+---<--    A dash--is not a line    v        |      *
*                                          /           Nor/is this.            ---              *
*************************************************************************************************

Diagram Examples
================================================================================

Lines with Decorations
--------------------------------------------------------------------------------
*************************************************************************************************
*                ________                            o        *          *   .--------------.   *
*   *---+--.    |        |     o   o      |         ^          \        /   |  .----------.  |  *
*       |   |    '--*   -+-    |   |      v        /            \      /    | |  <------.  | |  *
*       |    '----->       .---(---'  --->*<---   /      .+->*<--o----'     | |          | | |  *
*   <--'  ^  ^             |   |                 |      | |  ^    \         |  '--------'  | |  *
*          \/        *-----'   o     |<----->|   '-----'  |__|     v         '------------'  |  *
*          /\                                                               *---------------'   *
*************************************************************************************************

Graph with Large Nodes
--------------------------------------------------------------------------------

*************************************************************************************************
*                                                                                               *
*   .---.       .-.        .-.       .-.                                       .-.              *
*   | A +----->| 1 +<---->| 2 |<----+ 4 +------------------.                  | 8 |             *
*   '---'       '-'        '+'       '-'                    |                  '-'              *
*                           |         ^                     |                   ^               *
*                           v         |                     v                   |               *
*                          .-.      .-+-.        .-.      .-+-.      .-.       .+.       .---.  *
*                         | 3 +---->| B |<----->| 5 +---->| C +---->| 6 +---->| 7 |<---->| D |  *
*                          '-'      '---'        '-'      '---'      '-'       '-'       '---'  *
*************************************************************************************************



Graph with Small Nodes
--------------------------------------------------------------------------------

*************************************************************************************************
*                 A      1      2     4                        8                                *
*                  *----->o<---->o<----o-----------.            o                               *
*                                ^     ^            |           ^                               *
*                                |     |            |           |                               *
*                                v     |            v           |                               *
*                                o<--->*<---->o---->*---->o---->o<---->*                        *
*                               3     B      5     C     6     7      D                         *
*************************************************************************************************


Flow Chart
--------------------------------------------------------------------------------

*************************************************************************************************
*                                      .                                                        *
*   .---------.                       / \                                                       *
*  |   START   |                     /   \        .-+-------+-.      ___________                *
*   '----+----'    .-------.    A   /     \   B   | |COMPLEX| |     /           \      .-.      *
*        |        |   END   |<-----+CHOICE +----->| |       | +--->+ PREPARATION +--->| X |     *
*        v         '-------'        \     /       | |PROCESS| |     \___________/      '-'      *
*    .---------.                     \   /        '-+---+---+-'                                 *
*   /  INPUT  /                       \ /                                                       *
*  '-----+---'                         '                                                        *
*        |                             ^                                                        *
*        v                             |                                                        *
*  .-----------.                 .-----+-----.        .-.                                       *
*  |  PROCESS  +---------------->|  PROCESS  |<------+ X |                                      *
*  '-----------'                 '-----------'        '-'                                       *
*************************************************************************************************

Line Ends
--------------------------------------------------------------------------------


*************************************************************************************************
*                                                                                               *
*   o--o    *--o     /  /   *  o  o o o o   * * * *   o o o o   * * * *      o o o o   * * * *  *
*   o--*    *--*    v  v   ^  ^   | | | |   | | | |    \ \ \ \   \ \ \ \    / / / /   / / / /   *
*   o-->    *-->   *  o   /  /    o * v '   o * v '     o * v \   o * v \  o * v /   o * v /    *
*   o---    *---                                                                                *
*                                 ^ ^ ^ ^   . . . .   ^ ^ ^ ^   \ \ \ \      ^ ^ ^ ^   / / / /  *
*   |  |   *  o  \  \   *  o      | | | |   | | | |    \ \ \ \   \ \ \ \    / / / /   / / / /   *
*   v  v   ^  ^   v  v   ^  ^     o * v '   o * v '     o * v \   o * v \  o * v /   o * v /    *
*   *  o   |  |    *  o   \  \                                                                  *
*                                                                                               *
*   <--o   <--*   <-->   <---      ---o   ---*   --->   ----      *<--   o<--   -->o   -->*     *
*                                                                                               *
*************************************************************************************************


Trees
--------------------------------------------------------------------------------

*************************************************************************************************
*                                                                                               *
*          .               .                .               .--- 1          .-- 1     / 1       *
*         / \              |                |           .---+            .-+         +          *
*        /   \         .---+---.         .--+--.        |   '--- 2      |   '-- 2   / \ 2       *
*       +     +        |       |        |       |    ---+            ---+          +            *
*      / \   / \     .-+-.   .-+-.     .+.     .+.      |   .--- 3      |   .-- 3   \ / 3       *
*     /   \ /   \    |   |   |   |    |   |   |   |     '---+            '-+         +          *
*     1   2 3   4    1   2   3   4    1   2   3   4         '--- 4          '-- 4     \ 4       *
*                                                                                               *
*************************************************************************************************


Big Shapes
--------------------------------------------------------------------------------
*************************************************************************************************
*                                                                                               *
*          .---------.   .   .-------.        .-------.   .---------.    .-----.      .----.    *
*           \       /   / \   \       \      |         |  |         |   /       \    /      \   *
*            \     /   /   \   \       \     |         |  |         |  /         \  |        |  *
*             \   /   /     \   \       \    |         |  |         |  \         /  |        |  *
*              \ /   /       \   \       \   |         |  |         |   \       /    \      /   *
*               '   '---------'   '-------'   '-------'   '---------'    '-----'      '----'    *
*                                                                                               *
*************************************************************************************************


Small Shapes
--------------------------------------------------------------------------------
*************************************************************************************************
*                                                                                      __   .   *
*  .--.     .  .-----.          .---.  .---.                    .---.     ___    ___  |  |  |)  *
* /    \   / \  \   /  .-.    .  \ /   |   |   .---. .---.     |     |   /   \  |   | '--'  '   *
* \    /  /   \  \ /  |   |  / \  '    '---'  /   /   \   \    |     |   \___/  |___|   .   __  *
*  '--'  '-----'  '    '-'  '---'            '---'     '---'    '---'                  (|  |__| *
*                                                                                       '       *
*************************************************************************************************


Overlaps and Intersections
--------------------------------------------------------------------------------

*************************************************************************************************
*                                                                                               *
*           .-.           .-.           .-.           .-.           .-.           .-.           *
*          |   |         |   |         |   |         |   |         |   |         |   |          *
*       .---------.   .--+---+--.   .--+---+--.   .--|   |--.   .--+   +--.   .------|--.       *
*      |           | |           | |   |   |   | |   |   |   | |           | |   |   |   |      *
*       '---------'   '--+---+--'   '--+---+--'   '--|   |--'   '--+   +--'   '--|------'       *
*          |   |         |   |         |   |         |   |         |   |         |   |          *
*           '-'           '-'           '-'           '-'           '-'           '-'           *
*************************************************************************************************



Big Grids
--------------------------------------------------------------------------------

*************************************************************************************************
*    .----.        .----.                                                                       *
*   /      \      /      \            .-----+-----+-----.                                       *
*  +        +----+        +----.      |     |     |     |          .-----+-----+-----+-----+    *
*   \      /      \      /      \     |     |     |     |         /     /     /     /     /     *
*    +----+   B    +----+        +    +-----+-----+-----+        +-----+-----+-----+-----+      *
*   /      \      /      \      /     |     |     |     |       /     /     /     /     /       *
*  +   A    +----+        +----+      |     |  B  |     |      +-----+-----+-----+-----+        *
*   \      /      \      /      \     +-----+-----+-----+     /     /  A  /  B  /     /         *
*    '----+        +----+        +    |     |     |     |    +-----+-----+-----+-----+          *
*          \      /      \      /     |  A  |     |     |   /     /     /     /     /           *
*           '----'        '----'      '-----+-----+-----'  '-----+-----+-----+-----+            *
*                                                                                               *
*************************************************************************************************


Small Grids
--------------------------------------------------------------------------------

*************************************************************************************************
*       ___     ___    ________    .---+---+---+---+---.     .---+---+---+---.  .---.   .---.   *
*   ___/   \___/   \  |__|__|__|   |   |   |   |   |   |    / \ / \ / \ / \ /   |   +---+   |   *
*  /   \___/   \___/  |__|__|__|   +---+---+---+---+---+   +---+---+---+---+    +---+   +---+   *
*  \___/ b \___/   \  |__|__|__|   |   |   | b |   |   |    \ / \a/ \b/ \ / \   |   +---+   |   *
*  / a \___/   \___/  |__|__|__|   +---+---+---+---+---+     +---+---+---+---+  +---+ b +---+   *
*  \___/   \___/   \  |__|__|__|   |   | a |   |   |   |    / \ / \ / \ / \ /   | a +---+   |   *
*      \___/   \___/  |__|__|__|   '---+---+---+---+---'   '---+---+---+---'    '---'   '---'   *
*                                                                                               *
*************************************************************************************************

Graphics Diagrams
-------------------------------------------------------------------------------
*************************************************************************************************
*                                                                             .                 *
*    0       3                          P *              Eye /         ^     /                  *
*     *-------*      +y                    \                +)          \   /  Reflection       *
*  1 /|    2 /|       ^                     \                \           \ v                    *
*   *-------* |       |                v0    \       v3           --------*--------             *
*   | |4    | |7      |                  *----\-----*                                           *
*   | *-----|-*       +-----> +x        /      v X   \          .-.<--------        o           *
*   |/      |/       /                 /        o     \        | / | Refraction    / \          *
*   *-------*       v                 /                \        +-'               /   \         *
*  5       6      +z              v1 *------------------* v2    |                o-----o        *
*                                                               v                               *
*************************************************************************************************


Icon Diagram
--------------------------------------------------------------------------------

*************************************************************************************************
*                                      .-.                           .--------.                 *
*                                   .-+   |                         |          |                *
*                               .--+       '--.                     |'--------'|                *
*                              |  Server Cloud |<------------------>| Database |                *
*                               '-------------'                     |          |                *
*                                   ^      ^                         '--------'                 *
*                    Internet       |      |                              ^                     *
*          .------------------------'      '-------------.                |                     *
*          |                                             |                v                     *
*          v                                             v              .------.       .------. *
*     .--------.      WiFi     .--------.  Bluetooth  .-----.          / #  # /|      / #  # /| *
*     |        |<------------->|        |<---------->|       |        +------+/| LAN +------+/| *
*     |Windows |               |  OS X  |            |  iOS  |        |      +/|<--->|      +/| *
*     +--------+               +--------+            |       |        |Ubuntu+/|     |Ubuntu+/| *
*    /// ____ \\\             /// ____ \\\           |   o   |        |      +/      |      +/  *
*   '------------'           '------------'           '-----'         '------'       '------'   *
*      Laptop 1                 Laptop 2              Tablet 1         Dedicated Server Rack    *
*************************************************************************************************

Various Syntaxes for Horizontal Rules
------------------------------------------------------------------------------------

The following are all produced by different patterns in the source:

-----

- - -

_____

_ _ _

*****

* * *

Embedded Math
========================

Markdeep automatically includes [MathJax](http://mathjax.org) if your
document contains equations and you have an Internet connection. That means
you get the **full power of LaTeX, TeX, MathML, and AsciiMath notation**.
Just put math inside single or double dollar signs. 

$$ \Lo(X, \wo) = \Le(X, \wo) + \int_\Omega \Li(X, \wi) ~ f_X(\wi, \wo) ~ | \n \cdot \wi | ~ d\wi $$

You can also use LaTeX equation syntax directly to obtain numbered
equations:

\begin{equation}
e^{i \pi} + 1 = 0
\end{equation}

\begin{equation}
\mathbf{A}^{-1}\vec{b} = \vec{x}
\end{equation}

If you don't have equations in your document, then Markdeep won't
connect to the MathJax server. Either way, it runs MathJax after 
processing the rest of the document, so there is no delay.

Markdeep is smart enough to distinguish non-math use of dollar signs,
such as $2.00 and $4.00 on the same line. It also contains some useful
extra commands by default default (well, useful if you work on
computer graphics) as shown in the examples below. Note that inline
math requires a space after the dollar sign to distinguish it from
regular text usage.

   Code            |   Symbol
-------------------|------------
 ` \n `            |  $ \n $
 ` \w `            |  $ \w $
 ` \wo `           |  $ \wo $
 ` \wi `           |  $ \wi $
 ` \wh `           |  $ \wh $
 ` \Li `           |  $ \Li $
 ` \Lo `           |  $ \Lo $
 ` \Lr `           |  $ \Lr $
 ` \Le `           |  $ \Le $
 `\O(n)`           |  $ \O(n) $
 `\mathbf{M}^\T`   |  $ \mathbf{M}^\T$
 `45\degrees`      |  $ 45\degrees$
 `x \in \Real`     |  $ x \in \Real$
 `x \in \Integer`  |  $ x \in \Integer$
 `x \in \Boolean`  |  $ x \in \Boolean$
 `x \in \Complex`  |  $ x \in \Complex$








<!-- Markdeep: --><style class="fallback">body{white-space:pre;font-family:monospace}</style><script src="markdeep.min.js"></script><script src="http://casual-effects.com/markdeep/latest/markdeep.min.js"></script>

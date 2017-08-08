# Pythonista 101: Python Wrangling

_Captured: 2015-09-29 at 00:10 from [ipad.appstorm.net](http://ipad.appstorm.net/how-to/utilities/pythonista-101-python-wrangling/)_

After the last article you should now be familiar with the Pythonista app as well as the eager community of developers which support it. While we did create a new script and learn how to import other scripts into Pythonista, we didn't actually write any Python code. And while we won't be writing any scripts from scratch this time, we will be learning how to read a Python program, as well as to modify certain aspects of it to add functionality or make it our own.

_Like this article? Stay up to date with the latest changes by subscribing to our [RSS feed](http://feeds2.feedburner.com/ipadappstorm) or by following us either on [Twitter](https://twitter.com/ipadappstorm), [Facebook](http://facebook.com/ipadappstorm), [Google+](https://plus.google.com/100501393336992877365/posts) or [App.net](https://alpha.app.net/ipadappstorm)._

## A Brief Explanation of Terminology

Just so we're all on the same page as we being writing Python code I thought I'd go through a few terms that we'll be using later.

**Variable**: a name assigned to a value. Sounds simple, but extremely powerful in practice as the value can change while the name remains the same.

**Function**: a portion of code within a larger program that performs a specific task. Functions are key to keeping code flexible and modular.

**Parameter**: a special kind of variable used when calling a function, providing input values that will be used later in the function. Parameters are a big reason functions remain usable and flexible.

**Script**: term used rather loosely, often to describe a program contained within a single file. Since all of the programs written with Pythonista are contained within a single file, they're often referred to as scripts.

**Editor**: the section of the Pythonista app where you edit code.

**Console**: the section of Pythonista where output from your scripts goes. The console is also often referred to as the Interpreter, because straight Python code can be entered into the console and run as code. The console is also used as a place to enter input to be processed by your script.

**Module**: integrated into Pythonista, modules are self-contained pieces of Python code offering additional functionality not found in the Python language itself. We'll be leveraging several modules in the examples we look at today.

## Breaking Down a Python Script

Instead of starting with that _very_ intimidating blank page, lets walk through a basic Python script so you can get a feel for the way one is structured before writing one of your own.

### Import Statements

Import statements are used to activate Python modules within a script. For consistency's sake, they're often declared on separate lines, one module per line.

![Import statements](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-Python-Wrangling1.jpg)

> _Import statements_

### Defining Variables

While some programming languages require some specific syntax when initializing a variable versus reassigning the value of the variable, Python does not. Instead, simply assign the variable a value and consider it created.

![Defining a variable](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-Python-Wrangling2.jpg)

> _Defining a variable_

### Defining Functions

With Python's emphasis on readability, the syntax used to define a function is clean and clear. The _def_ keyword is put at the beginning, followed by the name of the function. Any parameters are put inside parentheses, and default values for those parameters may be added as well. The function definition is finished with a colon, and the lines making up the function are indented.

![Defining a function](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-Python-Wrangling3.jpg)

> _Defining a function_

### Calling Functions

This one is so simple it barely needs mentioning. Take a look at the bottom of the image below. The very last line of code. That's how to call a function in Python, the function name followed by a pair of parentheses. Any parameters for the function would be passed in by placing them within the parameters.

![Calling a function](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-Python-Wrangling4.jpg)

> _Calling a function_

## Modifying a Script: Meme Generator

Ok, lets take what we just learned about how Python scripts are built and use it to modify a pre-existing script. [In our last lesson](http://ipad.appstorm.net/how-to/utilities/pythonista-101-the-scripting-community/), one of the scripts highlighted was a [Meme Generator](https://gist.github.com/omz/4034426) that used the Python Image Library (PIL) to add text to the image. We're going to look at how changing some variables and a parameter or two will let us modify the resulting image in a significant way. Then we'll leverage some of those existing variables and with some simple logic enhance this script.

### Change the Font Color

Open the Meme Generator script in your copy of Pythonista. If you don't have the script, take a look at [our last lesson](http://ipad.appstorm.net/how-to/utilities/pythonista-101-the-scripting-community/) for the instructions on how to get it. On line 32 of the Editor we see the following code:

`draw.text((10, draw_y), text, font=font, fill='white')`

The parameter _fill_ is being set to 'white'. Lets change it to 'red'.

`draw.text((10, draw_y), text, font=font, fill='red')`

Run the script by pressing the "Run" button and enter in some test text.

![130523-Python-Wrangling6](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-Python-Wrangling6.jpg)

> _The text has now changed to red._

Success! As you can see from the image below, our text is now red.

### Changing the Font

Now lets change the font that's being used here. I've always been partial to Futura, so we'll swap that out and see what it looks like. On line 21 in the Editor we see the following:

`font = ImageFont.truetype('HelveticaNeue-CondensedBlack', s)`

This line sets the font to be used as well as the size that text is going to be. The size is determined dynamically as the surrounding code block shows. The script uses the ImageFont module, which I'll discuss in greater depth in a future lesson. For now all you really need to know is that by chaining the first parameter in this function call, we can change the font that's used in our final image. Change the first parameter to be "Futura-Medium".

`font = ImageFont.truetype('Futura-Medium', s)`

Run the script and enter in some test text.

![130523-Python-Wrangling7](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-Python-Wrangling7.jpg)

> _The font has now changed to Futura._

Voila! We've successfully changed the font!

### Centering the Text

Now that we've successfully changed the font and font color, lets get a little more complicated and write some logic to center the text. This piece of code will be trickier to write. It isn't just changing a few parameters of variables. We need to write some code that determines the final width of the text, subtracts that from the width of the overall image, divides that by two and then uses the resulting value as the starting point for where to place the text. If all that sounded a little overwhelming, bear with me. We'll take it step-by-step. First we need to determine where in the script to put our new code. We're modifying where the text is rendered, so we want to find what line renders the text, and then begin writing our code above that. Fortunately the original script writer did a wonderful job commenting his script, so we know that the code that draws the text begins on line 25:

`#Draw the text multiple times in black to get the outline:`

The original writer used a variable called _x_ to store the value of the "x" coordinates. In line 26 the variable _x_ is set using the _xrange_ function and with a _for_ loop, text gets drawn with the "x" coordinates whose values go from -3 to 4.

`for x in xrange(-3, 4):`

You may think that means that the value for the "x" starts at "-3″ and then continues to "4". But we need to look at the line that actually draws the text, line 29:

`draw.text((10 + x, draw_y), text, font=font, fill='black')`

Here we see that the "x" coordinate is actually "10" plus the value of _x_. Now that we know how to set the "x" coordinate, we'll place our line that calculates the new starting "x" value. Put it above the comment found on line 25:

`x = (img.size[0] - w)/2`

Lets break this line down a little bit. We're setting a variable called _x_. What we're setting it to is the result of a basic algebraic equation. We want to take the width of the image and subtract the width of the text from that, then split the difference in half. We're getting the image width courtesy of the ImageDraw module and the _img_ variable that's passed in as a parameter to the function we're working within.

The parameter is set to the variable of _img_, and the module provides a _size_ method. Adding the _[0]_ accesses the width. For more information on the ImageDraw module and the _size_ method, you can refer to the built-in documentation. But we'll get to that more in the next article. To get the width of the text we're using the _w_ variable which is set up on line 22 as a part of the original script. Finally we're dividing the whole thing by two.

We can't forget about the _xrange_ section which creates the black outline around the text. Instead of just "-3″ and "4" we'll add _x_:

`for x in xrange(x-3, x+4):`

We also need to remove where "10" is added to _x_:

`draw.text((x, draw_y), text, font=font, fill='black')`

While you may think we're done, but we want to center the main text too, not just the outline. So drop down to line 33 and set the "x" coordinate in the _draw.text()_ function:

`draw.text((x-2, draw_y), text, font=font, fill='red')`

We added the "-2″ to center the main text within the outline. If you run the script now and add some text, you'll see it now nicely centered in you image.

![Our nicely centered text.](http://cdn.appstorm.net/ipad.appstorm.net/authors/zachlebar2/130523-Python-Wrangling5.jpg)

> _Our nicely centered text._

## Your Turn

Alright, now that you've played around with some Python code and have seen that the whole world doesn't come crashing down if things aren't just right, feel free to fiddle with some of the other scripts you find. In the next article we'll dive more into modules and the potential they open up for writing scripts of your own.

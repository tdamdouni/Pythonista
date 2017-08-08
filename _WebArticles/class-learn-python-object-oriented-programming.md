# Class: Learn Python object oriented programming

_Captured: 2017-02-18 at 15:48 from [www.raspberrypi.org](https://www.raspberrypi.org/magpi/class-python/)_

![](https://www.raspberrypi.org/magpi/wp-content/uploads/2017/02/Python-class-definitions.png)

> _In our previous Python OOP tutorial we created a dice game called Bunco in Scratch. Now we're going to recreate it in Python using class definitions to create players (like sprites in Scratch)._

The translation will help us get a good understanding of how objects work.

The game is pretty simple. Two players roll three dice, and the player with the highest score wins.

This article is based on Learn Object-Oriented Programming in issue 54 of The MagPi. Issue 53 of The MagPi has a companion piece on learning to code with a Raspberry Pi

See also:

### Creating Python procedural programs

First, let's talk about how we could make the game procedurally.

There is a module called random that we can import to create random numbers. So we'd need to import that. Then we could create a list for each player. And use the randint function to add three random numbers between one and six.

We could then use an if else block with the sum() function to add up each player's numbers. The player with the highest score wins.

Type out this bunco_procedural.py program.

123456789101112131415161718 
import randomplayer1_dice = []player2_dice = []for i in range(3):player1_dice.append(random.randint(1,6))player2_dice.append(random.randint(1,6))print("Player 1 rolled" \+ str(player1_dice))print("Player 2 rolled" \+ str(player2_dice))if sum(player1_dice) == sum(player2_dice):print("Draw")elif sum(player1_dice) > sum(player2_dice):print("Player 1 wins")else:print("Player 2 wins")

The code works, but only because this is a basic implementation of the game.

Bunco is a much more complex game in real life. It is played in six rounds, and players score 21 points if they roll all three dice that match the number of the round (three 1s in round 1, or three 2s in round 2, and so on). That's known as rolling a 'bunco'.

We're not going to create all that complexity here. But we are going to add extra types of player. Cheats! One scoundrel has loaded dice; the other rapscallion swaps out one die for a six.

We're then going to play thousands of games and see who wins.

This complexity would be extremely difficult in procedural programming. It requires us to rethink our approach to Bunco. And OOP is the answer.

### Python class definitions and objects

Instead of creating a list of variables for each player at the start, we're going to create a class called Player.

The code in bunco_oop.py represents a dice player. We then use it to create two players.

1234567891011121314151617181920212223242526272829 
from random import randintclass Player:def __init__(self):self.dice = []def roll(self):self.dice = [] # clears current dicefor i in range(3):self.dice.append(randint(1,6))def get_dice(self):return self.diceplayer1 = Player()player2 = Player()player1.roll()player2.roll()print("Player 1 rolled" \+ str(player1.get_dice()))print("Player 2 rolled" \+ str(player2.get_dice()))if sum(player1.get_dice()) == sum(player2.get_dice()):print("Draw!")elif sum(player1.get_dice()) > sum(player2.get_dice()):print("Player 1 wins!")else:print("Player 2 wins!")

One of the biggest differences between creating sprites in Scratch and objects in Python is that you create an object using a class. This code acts as a blueprint for the object.

In Scratch, you create a sprite and then duplicate it. The second sprite has the same functions as the first. It also has its own set of variables.

In Python (and other programming languages), things work somewhat differently. You don't create an object directly. Instead, you create a blueprint for the objects. This blueprint is known as the 'class'.

Don't think of a school, though. Class here means a category of similar items. It's rather like a 'Class M' planet in Star Trek: though different, these are all Earth-like planets.

Once you've created your class, you use it to create objects. These are known as 'instances' or 'object instances'. They all share similar properties. They all have the same variables and functions (called 'methods'). In Scratch, we create one sprite and then duplicate it (to get two sprites). In Python, we create one class definition. We then use this to create two object instances.

### Understanding object oriented code

As with our procedural code, we start by importing the randint module.  
Now we define our player objects. To do this, we create a class definition. It looks like this:

Inside the class definition is indented code that describes the player object.

Notice that the class name is capitalised and, unlike function definitions, there are no parentheses.

The first thing we need to add is a list to contain the dice. Normally this would be just dice = []. But if we wrote it like this:

…we'd have a problem. This code is equivalent to choosing 'For all sprites' in Scratch. Every player created using this code would share a single set of dice and get the same results. We want to use the equivalent of 'For this sprite only'.

To ensure that all our players have their own set of dice, we need to wrap the dice = [] list inside a quirky function called __init__().  
It looks like this:

The __init__() function runs when you use a class to create an object.

This is known as a 'constructor' or 'initialiser'.

Later on, when we use this Player class to create player objects, the __init__() code runs each time automatically. It creates a separate set of dice for each of our players.

The 'self' bit also needs explaining. Variables, like our dice = [] list are normally disposed of when a function ends (or is returned).

So if we just put dice = [], the list would be created by __init__(), then immediately vanish.

Python gets around this problem using the keyword 'self'. You put 'self' inside the parentheses of the __init__():

Then we use self, followed by a dot, to store the variable in this version of the object.

You then use self. in functions when you want to access or change a variable, by writing self inside the parentheses of the function. Like this:

The concept can be mind-boggling (it's passing a version of itself into itself). So focus on the practical steps rather than the esoteric theory of how it works:

  * Put a special function at the start of a class called __init__(self).
  * Put the variables you want to use inside init.
  * Create the variables with self., like self.name or self.age or self.dice = [].
  * Place self inside the parentheses of functions that need to access the variables.
  * Use self. and the name of the variable inside the function to use it.

Got that? Don't worry too much if it seems weird. That's the hardest part and it will get easier with practice.

Now we've got our dice list sorted, what about the other functions?

### Using methods in Python class definitions

Now that our class has a list for the dice, we need to roll the dice. For that, we'll create a function definition.

An object's functions are called 'methods', but they are created in the same way.

There are lots of different types of methods, and you can create whatever you like, but common ones are called 'setters' and 'getters'.

Our roll method is a 'setter'. It sets the dice list to three random numbers.

What do you think a 'getter' does? That's right. It gets the variables inside the object and returns them. We have just the one getter:

Getters and setters seem a bit odd at first. After all, you could just reach into an object and access the variables.

Well, you could, at least in Python, but this is considered a bad thing to do. One of the points of OOP is that objects contain their variables and keep them safe from other objects. So you don't just reach inside an object and access variables.

Instead, you create methods (functions) that set the variables and get them. Then you use these methods to set and get variables.

Now we've created our class definition, we can use it to create objects.

### Create objects in Python OOP

You create objects just as you would a variable. You use the assigns operator (=). We're going to create two dice players:

Note that player1 and player2 are not called 'variables'. They are called 'object instances'.

We access the object instance's methods using dot notation. That is where you use the name of the object instance, followed by a dot, then the name of the method you want to use.

We created a method, get_dice(), that returns the dice stored. We would access this method using dot notation, such as player1.get_dice().

Finally, we use the roll method to get each player object to roll its own set of dice:

The rest of our bunco_oop.py program is really very similar to bunco_procedural.py. The difference is that here we use the .get_dice() method in place of sum().

This way each player object instance returns its own (self) set of dice. The object with the highest score wins.

Next, we're going to look at creating other types of objects. Like players who can cheat!

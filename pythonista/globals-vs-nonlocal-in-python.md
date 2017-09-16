_https://forum.omz-software.com/topic/4340/share-list-dialog-simple/8_

you did mention that you were trying to understand scopes. Here're some explanations of how global and nonlocal works. It's simplified and it's still recommended to read Python documentation to fully understand it. But this should help a bit.

global

name = 'Phuket2'  # Global variable

def say_hallo():
    # You're just reading global 'name', thus no need
    # to use 'global' in this case
    print('Hallo {}'.format(name))

def update_without_global(new_name):
    # Here we're writing to 'name', so, new local variable
    # 'name' is created and global 'name' is untouched
    name = new_name
    # What can help here is analyzer warning:
    #  - local variable 'name' is assigned but never used

def update_with_global(new_name):
    # Here we're saying that we would like to modify
    # global variable 'name'
    global name
    name = new_name

say_hallo()  # Prints 'Hallo Phuket2'
update_without_global('Zrzka')
say_hallo()  # Still prints 'Hallo Phuket2' 
update_with_global('Zrzka')
say_hallo()  # Prints 'Hallo Zrzka'
But what about this?

attributes = {'name': 'Phuket2'}

def say_hallo():
    print('Hallo {}'.format(attributes['name']))

def update_without_global(new_name):
    attributes['name'] = new_name

say_hallo()  # Prints 'Hallo Phuket2'
update_without_global('Zrzka')
say_hallo()  # Prints 'Hallo Zrzka'
Ouch, what's going on one can say. I didn't use global here, but it was modified.

What is variable? It's called name in Python and every name refers to an object. This is called binding. You can read more here if you're interested (chapter 4.2.).

Basically everything is an object in Python. Really? What about primitive types for example? Python has no primitive types you know from Java or Objective C. Everything is an object in Python, even bool, int, ...

What plays big role here is mutability vs immutability and if you're mutating in place or assigning new object. Some types are immutable (bool, int, float, tuple, str, frozenset) and some are mutable (list, set, dict). Immutable objects can't be modified after you create them, mutable can.

# Immutable
x = 3
print(id(x)) # 4322496384
x += 1       # New object is created
print(id(x)) # 4322496416 != 4322496384

# Mutable
y = ['a']
print(id(y))  # 4454700936
y.append('b')
print(id(y))  # 4454700936 (equals)
y[:] = ['a', 'b', 'c']
print(id(y))  # 4454700936 (equals)
y = ['a', 'b', 'c']
print(id(y))  # 4461963720 (oops, new object b/o =)
x is of type int. This type is immutable. It looks like mutable type, but it isn't. Whenever you do x += 1, new object is created and x is rebinded to this new object. If type of your variable is immutable and you want to modify it, you have to use global.

y is of type list. This type is mutable. Whenever you do y.append('b'), it's still the same object. .append mutates it in place. Also y[:] = ['a', 'b'] mutates the list in place. It replaces all elements in the list, but it's done in place, no new object is created. So, you don't need global here as well.

But don't forget that simple assignment like y = ['a', 'b', 'c'] rebinds y variable to the new object (you're not mutating it in place) and you must use global in this case.

nonlocal

Some quote from nonlocal docs:

The nonlocal statement causes the listed identifiers to refer to previously bound variables in the nearest enclosing scope excluding globals. This is important because the default behavior for binding is to search the local namespace first. The statement allows encapsulated code to rebind variables outside of the local scope besides the global (module) scope.
Example of excluding globals:

name = 'Phuket2'

def update(new_name):
    nonlocal name
    name = new_name
    
update('Zrzka')
print(name)
It leads to SyntaxError, because no binding for nonlocal name was found. Globals are excluded.

Following example just creates local variable name. Same analyzer warning can help (assigned to, but never read).

def hallo():
    name = 'Phuket2'
    
    def update(new_name):
        # Local variable 'name', has nothing to do
        # with 'name' defined at the beginning of
        # 'hallo'
        name = new_name
        
    update('Zrzka')
    print(name)  # Prints 'Phuket2'

hallo()
And here's the correct one.

def hallo():
    name = 'Phuket2'
    
    def update(new_name):
        nonlocal name
        name = new_name
        
    update('Zrzka')
    print(name)  # Prints 'Zrzka'

hallo()
name in update refers to the name in hallo. You can rebind it. Same dance with mutable / immutable types can be reused here as well. See following example.

def hallo():
    attributes = {'name': 'Phuket2'}
    
    def update(new_name):
        attributes['name'] = new_name
        
    update('Zrzka')
    print(attributes['name'])  # Prints 'Zrzka'

hallo()
I didn't use nonlocal, but attributes were still modified. That's because I did use in place mutation. No new object, no need to rebind.

Also nonlocal search enclosing scopes (not just one scope) until it finds the right variable.

def level1():
    name = 'Phuket2'
    
    def level2():
        def level3():
            nonlocal name  # name in level1
            name = 'Zrzka'
        level3()

    level2()    
    print(name)  # Prints 'Zrzka'

level1()
And the nearest enclosing scope is used.

import console
console.clear()

def level1():
    name = 'Phuket2'
    
    def level2():
        name = 'Ole'        
        def level3():
            nonlocal name  # name in level2
            name = 'Zrzka'
        level3()

    level2()    
    print(name)  # Prints 'Phuket2'

level1()
These are contrived examples. Just to demostrate how it works. You do not want these multilevel functions where each has name and nonlocal somewhere :)

But the most important thing about nonlocal is that this lexical scoping applies to function namespaces only.

def classy():
    name = 'Phuket2'
    
    class Hallo():
        name = 'Batman'
        
        def __init__(self):
            self.name = 'Ole'
        
        def update(self, new_name):
            nonlocal name  # name in classy
            name = new_name
            
    h = Hallo()
    
    print(name)       # Prints 'Phuket2'
    print(Hallo.name) # Prints 'Batman'
    print(h.name)     # Prints 'Ole'

    h.update('Zrzka')

    print(name)       # Prints 'Zrzka'
    print(Hallo.name) # Prints 'Batman'
    print(h.name)     # Prints 'Ole'    
    
classy()
As I already wrote, this is simplified explanation with contrived examples. Anyway, hope it helps to understand what's going on.


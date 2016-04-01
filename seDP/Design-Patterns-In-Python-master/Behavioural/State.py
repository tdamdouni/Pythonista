#!/usr/bin/env python
# Written by: DGC

#==============================================================================
class Language(object):
    
    def greet(self):
        return self.greeting

#==============================================================================
class English(Language):
    
    def __init__(self):
        self.greeting = "Hello"

#==============================================================================
class French(Language):
    
    def __init__(self):
        self.greeting = "Bonjour"

#==============================================================================
class Spanish(Language):
    
    def __init__(self):
        self.greeting = "Hola"

#==============================================================================
class Multilinguist(object):

    def __init__(self, language):
        self.greetings = {
            "English": "Hello",
            "French": "Bonjour",
            "Spanish": "Hola"
            }
        self.language = language

    def greet(self):
        print(self.greetings[self.language])

#==============================================================================
if (__name__ == "__main__"):

    # talking in English
    translator = Multilinguist("English")
    translator.greet()

    # meets a Frenchman
    translator.language = "French"
    translator.greet()

    # greets a Spaniard
    translator.language = "Spanish"    
    translator.greet()

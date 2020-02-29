from __future__ import print_function
# https://forum.omz-software.com/topic/2291/share-code-for-beginners-like-me-the-python-help-function

# coding: utf-8

class SolveTheWorldsProblems(object):
    '''
    Description:
        its not possible
        
    Args:
        the meaning of life
            
    Returns:
        -optimisim 
        
    Raises:
        more questions that can be answered
    '''
    def __init__(self, meaning_of_life):
        '''
            the comment for the __init__ method
        '''
        self.meaning_of_life = meaning_of_life
        
    def result(self):
        '''
            the comment for the result method
        '''
        return ('optimism')
        
    

if __name__ == '__main__':
    stwp = SolveTheWorldsProblems(666)
    print(help(stwp))
from __future__ import print_function
# https://gist.github.com/TutorialDoctor/5834bbefb9c9d795518e

# Drop this folder in a directory and run it. It will organize all of your files into folder by first letter
# This was inspired by my mom (maybe you can relate?)
# This took much longer than I thought it would to figure this out, but I learned which modules are good for file handling.
# It took about an hour to come up with the base of the program, which organizes files by first letter or number
# I would like it to eventually recursively go into folders getting files and organizing them into folders.
# This was made using a straight ahead approach.
# For beginners, a directory is a folder.
# By the Tutorial Doctor
# Sun Dec 20 23:40:49 EST 2015
#------------------------------------------------------------------------------
import os,os.path,shutil,fnmatch


# THE CODE
#------------------------------------------------------------------------------
root_directory = os.getcwd()
directory_files = os.listdir(root_directory) # This is how you get all of the files and folders in a directory
root_size = os.path.getsize(root_directory) # Just a tip on how to get the size of a directory


def organize_files_by_letter(first_letter):
    for File in directory_files:
        # If the first letter in the file name is equal to the first_letter parameter...
        if str(File[0]).capitalize() == first_letter.capitalize():
            # Print the file (will print as a string)...
            print(File)
            # And print if it is a file or not (This step and the prior is nor really needed)
            print(os.path.isfile(File))
            print() 
            # If the file is truly a file...
            if os.path.isfile(File):
                try:
                    # Make a directory with the first letter of the file name...
                    os.makedirs(first_letter)
                except:
                    None
                # Copy that file to the directory with that letter
                shutil.copy(File,first_letter)


def organize_files_by_extension(ext):
    for File in directory_files:
        # If the extension of the file matches some text followed by ext...
        if fnmatch.fnmatch(File,'*' + ext):
            print(file)          
            # If the file is truly a file...
            if os.path.isfile(File):
                try:
                    # Make a directory with the extension name...
                    os.makedirs(ext)
                except:
                    None
                # Copy that file to the directory with that extension name
                shutil.copy(File,ext)
                

def organize_files_by_keyword(keyword):
    for File in directory_files:
        # If the name of the file contains a keyword
        if fnmatch.fnmatch(File,'*' + keyword + '*'):
            print(file)          
            # If the file is truly a file...
            if os.path.isfile(File):
                try:
                    # Make a directory with the keyword name...
                    os.makedirs(keyword)
                except:
                    None
                # Copy that file to the directory with that keyword name
                shutil.copy(File,keyword)
                
                
def organize_folders_by_letter(first_letter):
    for File in directory_files:
        if str(File[0]).capitalize() == first_letter.capitalize():
            # If the file is truly a directory...
            if os.path.isdir(File):
                try:
                    # Move the directory to the directory with the first_letter
                    shutil.move(File,first_letter)                    
                except:
                    None

                    
# Untested, but it should work
def organize_folders_by_keyword(keyword):
    for File in directory_files:
        # If the name of the file contains a keyword
        if fnmatch.fnmatch(File,'*' + keyword + '*'):
            # If the file is truly a folder/directory...
            if os.path.isdir(File):
                try:
                    # Move the directory to the directory with that keyword name
                    shutil.move(File,keyword)                    
                except:
                    None
#------------------------------------------------------------------------------

    
# IMPLEMENTATION
#------------------------------------------------------------------------------
#organize_files_by_letter("a") # This is how you use it for one letter
#organize_files_by_letter('0')
#organize_files_by_letter('o')
#organize_files_by_letter('b')
#organize_files_by_extension('txt')
#organize_folders_by_letter('a')
#organize_files_by_keyword('music')
#------------------------------------------------------------------------------


def organize(option):
    if option == 1:
        # To organize files starting with all letters or numbers you can do this:
        for letter_or_number in 'abcdefghijklmnopqrstuvwxyz0123456789':
            organize_files_by_letter(letter_or_number)
    
    if option == 2:
        for folder in 'abcdefghijklmnopqrstuvwxyz0123456789':
            organize_folders_by_letter(folder)
    
    if option == 3:
        for ext in ['jpg','png','bmp','jpeg','JPG']:
            organize_files_by_extension(ext)
    
    if option == 4:
        for keyword in ['music','art','screenshot','sound','image']:
            organize_files_by_keyword(keyword)
    
    if option == 5:
        for keyword in ['music','art','social']:
            organize_folders_by_keyword(keyword)

 
organize(4)

# EXTRA STUFF
#------------------------------------------------------------------------------
# This function helped me along the way to this solution.
# Perhaps it is useful to someone, so I will leave it
def read_files():
    for File in directory_files:
        try:
            with open(File,'r') as infile:
                print(infile.read())
        except:
            None

            
def match_files(ext):
    'Prints files with extension ext'
    for File in directory_files:
        if fnmatch.fnmatch(File,'*' + ext):
            print(File)
    # * matches everything
    # ? matches any single character
    # [seq] matches any character in seq
    # [!seq] matches any character not in seq
#------------------------------------------------------------------------------


# EXTRA STUFF IMPLEMENTATION
#------------------------------------------------------------------------------
#read_files() #If you are organizing a lot of files, you might not want to read them all.
match_files('txt')
match_files('py')
#------------------------------------------------------------------------------


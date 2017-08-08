# Tutorial: Todo-List Application

_Captured: 2015-06-17 at 23:16 from [omz-software.com](http://omz-software.com/pythonista/docs/ios/bottle/tutorial_app.html)_

This tutorial should give a brief introduction to the [Bottle](http://bottle.paws.org) WSGI Framework. The main goal is to be able, after reading through this tutorial, to create a project using Bottle. Within this document, not all abilities will be shown, but at least the main and important ones like routing, utilizing the Bottle template abilities to format output and handling GET / POST parameters.

To understand the content here, it is not necessary to have a basic knowledge of WSGI, as Bottle tries to keep WSGI away from the user anyway. You should have a fair understanding of the [Python](http://www.python.org) programming language. Furthermore, the example used in the tutorial retrieves and stores data in a SQL databse, so a basic idea about SQL helps, but is not a must to understand the concepts of Bottle. Right here, [SQLite](http://www.sqlite.org) is used. The output of Bottle sent to the browser is formatted in some examples by the help of HTML. Thus, a basic idea about the common HTML tags does help as well.

For the sake of introducing Bottle, the Python code "in between" is kept short, in order to keep the focus. Also all code within the tutorial is working fine, but you may not necessarily use it "in the wild", e.g. on a public web server. In order to do so, you may add e.g. more error handling, protect the database with a password, test and escape the input etc.

Table of Contents

At the end of this tutorial, we will have a simple, web-based ToDo list. The list contains a text (with max 100 characters) and a status (0 for closed, 1 for open) for each item. Through the web-based user interface, open items can be view and edited and new items can be added.

During development, all pages will be available on localhost only, but later on it will be shown how to adapt the application for a "real" server, including how to use with Apache's mod_wsgi.

Bottle will do the routing and format the output, with the help of templates. The items of the list will be stored inside a SQLite database. Reading and writing the database will be done by Python code.

We will end up with an application with the following pages and functionality:

>   * validating data assigned by dynamic routes with the @validate decorator
>   * catching errors

Install Bottle

Assuming that you have a fairly new installation of Python (version 2.5 or higher), you only need to install Bottle in addition to that. Bottle has no other dependencies than Python itself.

You can either manually install Bottle or use Python's easy_install: easy_install bottle

Further Software Necessities

As we use SQLite3 as a database, make sure it is installed. On Linux systems, most distributions have SQLite3 installed by default. SQLite is available for Windows and MacOS X as well and the sqlite3 module is part of the python standard library.

Create An SQL Database

First, we need to create the database we use later on. To do so, save the following script in your project directory and run it with python. You can use the interactive interpreter too:
    
    
    import sqlite3
    con = sqlite3.connect('todo.db') # Warning: This file is created in the current directory
    con.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL)")
    con.execute("INSERT INTO todo (task,status) VALUES ('Read A-byte-of-python to get a good introduction into Python',0)")
    con.execute("INSERT INTO todo (task,status) VALUES ('Visit the Python website',1)")
    con.execute("INSERT INTO todo (task,status) VALUES ('Test various editors for and check the syntax highlighting',1)")
    con.execute("INSERT INTO todo (task,status) VALUES ('Choose your favorite WSGI-Framework',0)")
    con.commit()
    

This generates a database-file todo.db with tables called todo and three columns id, task, and status. id is a unique id for each row, which is used later on to reference the rows. The column task holds the text which describes the task, it can be max 100 characters long. Finally, the column status is used to mark a task as open (value 1) or closed (value 0).

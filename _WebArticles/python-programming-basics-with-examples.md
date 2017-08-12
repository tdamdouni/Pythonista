# Python Programming Basics With Examples

_Captured: 2017-04-07 at 23:24 from [dzone.com](https://dzone.com/articles/python-programming-basics-with-examples?edition=288885&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-04-07)_

Need to build an application around your data? [Learn more](https://dzone.com/go?i=200129&u=http%3A%2F%2Fhubs.ly%2FH06Pr9h0) about dataflow programming for rapid development and greater creativity.

Python is a popular and a powerful scripting language that can do everything -- web crawling, networking tools, scientific tools, Raspberry PI programming, web development, video games, and much more. With Python programming, you can do even do system programming regardless of the platform you are using.

We will discuss basic Python programming in this post. In future posts, we will build tools and see Python programming in action.

If you find the content of this post is a little tricky, tell me so that I can start from the bottom level of Python programming in the upcoming posts.

## Manipulating Strings

Strings in Python are immutable, so they cannot be changed. Any change to a string's contents requires making a new copy.

Dealing with strings is very simple in Python.

String concatenation:

String multiplication:

Concatenate with non-strings by just converting the value:

Search for a substring:

The `find` method prints the position of the first occurrence of the `likegeeks` string if it's found. If nothing is found, it will return `-1` as a result. `find` starts from the first character -- however, you can start from the _n_th character like this:

Since we start from the 12th character, there is no word called `likegeeks` from that position, so it will return `-1`.

### Get Substrings

So, we got the index of the string we're searching for. Now, we want to print the string by index:

The first `print` line prints from the first character to the second character, while the second `print` line prints from the second character to the end. Notice the position of the colon. The count starts from zero.

You can use a negative number to start counting backward instead, like the fourth `print` line, which prints the last character in the string.

### Replace Strings

Replace a string:

If you have many occurrences and you want to replace the first occurrence only, you can specify that:

Only the first word got replaced.

### Strip Strings

You can trim whitespaces from a string:

You can strip from the right only or left only using `rstrip()` or `lstrip()` methods respectively.

### Change Character Case

Since uppercase and lowercase characters are treated differently, you can change the case of the characters if you want to compare them:

### Convert Strings to Numbers

We have the `str()`, function which casts the value to a string -- but this is not the only cast function in Python programming.

There are `int()`, `float()`, `long()`, and other cast functions that you can use. The `int()` function casts the input to the integer, while the `float()` function casts the input to float:
    
    
    print(int(str)+int(str2))

The first print line just concatenates the two numbers without summation, while the second print line adds the two values and prints the total.

### Count Strings

You can use the `min()`, `max()`, and `len()` functions to calculate the minimum character or maximum character value or the total length of characters.

### Iterate Over Strings

You can iterate over the string and manipulate every character individually like this:

Here, we've used the `len()` function, which counts the length of objects.

### Encode Strings

If you are using Python 3, all strings are stored as Unicode strings by defaul. If you are using Python 2, you may need to encode your strings like this:

## Manipulating Numbers

Numbers in python programming are defined like this: `a=15` .

You can define integers and floats the same way.

If you have a float number, you can round it like this:

### Round Numbers

You can use the `round()` function to round numbers like this:

Just specify how many numbers need to be rounded to the `round()` function.

### User-Defined Precision Numbers

You may need to work with floating numbers that are of arbitrary precision. Python provides a module called `decimal` that handles numbers of user-defined precision.

You can import the module like this:

### Generate Random Numbers

The random module in Python provides functions to generate random numbers:

The generated number is between 0.0 and 1.0.

You can generate a random number from your choices like this:

## Manipulating Dates and Times

Python provides a module called `datetime` that helps in handling dates and times.
    
    
    cur_date = datetime.datetime.now()

You can extract the value you need from the date like in the above examples.

You can get the differences between two times or two dates like this:

`timediff` is an object of type `timedelta`. H, however, you can create this kind of object yourself like this:
    
    
    time2 = datetime.timedelta(days=3)

### Format Date and Time

The `strftime()` method takes a format specification and formats the date or time based on it.

The following table specifies some of the format options that you can use:

![Image title](https://dzone.com/storage/temp/4877577-screen-shot-2017-04-05-at-110750-am.png)

### Create Date From String

You can use the `strptime()` function to create a date from string like this: `date1=datetime.datetime.strptime("2015-11-21", "%Y-%m-%d")` or like this: `date1= datetime.datetime(year=2015, month=11, day=21)`.

## Dealing With File System

Dealing with files is very easy in Python programming. Believe it or not, this is the easiest language you can use to deal with files. You can say that Python is the easiest language in doing many things.

### Copying Files

There are two functions in the `shutil` module that can be used to copy files:

If `file1.txt` is a symbolic link, this function call will create `file2.txt` as a separate file. If you want to actually create a copy of the symlink instead, you can do it like this:

### Moving Files

You can move files from one location to another using move function from the `shutil` module:

You can rename a file using the `rename` function from os module like this:

## Read and Write Text Files

You can use the built-in `open` function provided to open files, and then use the `read` or `write` methods to read from them and write to them.

First, we open the file for reading using the open function. Then, we start reading the file content using the `read` function. Finally, we put the grabbed content into the variable content.

You can specify how many bytes you want to read for the `read()` function with `fd.read(20)`.

If the file is not too large, you can read the entire contents into a list, then iterate over that list to print the output.

You can write to a file by specifying the mode to the `open` function. You have two modes of writing: the write mode and append mode.

This is the write mode where you will overwrite the old file content:

And this is the append mode:

### Creating Directories

You can create a new directory using the `mkdir` function from the `os` module like this:

This code will throw an error if the directory exists. Don't worry -- we will talk about exception handling in future posts so you can avoid such errors.

### Get Access, Modification, and Creation Time

You can use `getmtime()`, `getatime()`, and `getctime()` to get modification time, access time, and creation time respectively.

The returned time is formatted as a Unix timestamp. We can convert it to a human-readable format like this:

### Iterating Over Files

You can use the `listdir()` function from the `os` module to get the files:

Also, you can use the `glob` module to do the same thing:

You can write any extension for file globbing, like `*.doc`, to get all word documents only.

### Serializing Python Objects

This process is used to serialize a Python object to a byte stream for later reuse.

You can do that using the `pickle` module:

You can deserialize this data using the `load()` function like this:

### Compressing Files

The python standard library enables you to work with different types of compressed files like TAR, ZIP, GZIP, and BZIP2.

To work with a ZIP file, you can use the `zipfile` module:

You can create a ZIP file from your files like this:

You can extract the zip file using the `extractall()` method like this:

Also, you can append files to an existing ZIP file by using the `append` mode like this:

The same coding as above is done when dealing with GZ or BZ files. You need to use the `gzip` module or `bz2` module:

Then you can read and write in the same way.

You can deal with RAR files using the `unrar` package. First, install the package `pip install unrar`.

Then, you can use it the same way:

### Parse CSV Files

There is a very useful package called `pandas`. This package can parse CSV and Excel files, and extract data from them easily.

First, install the package `pip install pandas`.

Then, you can use it in your modules like this:

By default, `pandas` will treat the first column as the labels for each of the rows. If the row labels are in another column, you can use the parameter `index_col` to specify the column index.

If you don't have any row labels at all, you will probably want to use the parameter `index_col=False`.

To write to CSV file, you can use the `to_csv()` method: `data.to_csv('file.csv)`.

### Parse Excel Files

You can use the `read_excel()` method from the `pandas` module to parse excel files:

If you have multiple sheets that you wish to work with, you can load it like this:

It's the same way with CSV files. You can write to Excel files like this:

## Networking and Connectivity

The Python standard library includes a `socket` class that provides a way of accessing the network at a low level. It has to support many different networking protocols.

With this code, we establish a connection to a host at IP `192.168.1.5` on port `4040`.

Once a socket has been opened, you can send and receive data: `my_sock.sendall(b'Hello World')`.

Notice that I used the `b` character before the string because the data needs to be a byte string.

If have a bigger message, you should iterate over your message like this:
    
    
        sent = my_sock.send(msg[total:])

For receiving data, you need to tell the methods how many bytes to read in at a time: `data_in = my_sock.recv(2000)`.

This works because you know for sure that the message being sent is less than 2,000 bytes long.

If the message is longer, you must loop over and over until you collect all of the separate chunks.

Here, we define an empty buffer. Then, we start to write the message into the buffer.

### Reading an E-Mail From POP Mail Server

We already discussed [Linux mail server](https://likegeeks.com/linux-mail-server/) and everything about it. Now, how we can access it using Python programming?

The Python standard library contains a module named `poplib` that enables communication with a POP server.

The `getpass` module helps your code to ask in a secure way for passwords from the end user.

If the POP server you are using is secured, you need to use the `POP3_SSL` class instead.

After successful connection, you can interact with the POP server:

Don't forget to close any open connections after you finish working with the POP server: `pop_serv.quit()`.

### Reading an E-Mail From IMAP Mail Server

The `imaplib` module enables you to communicate with an IMAP email server:

If your IMAP server uses SSL, you need to use the `IMAP4_SSL` class instead.

To get a list of e-mails, you need to do a search: `data = my_imap.search(None, 'ALL')`.

Then, you can loop over the returned e-mail indices in the data variable and fetch the message using `msg = my_imap.fetch(email_id, '(RFC822)')`.

Finally, don't forget to close the connection:

### Sending an E-Mail

E-mails are sent using the SMTP protocol. The `smtplib` in Python is used to handle this.

If your SMTP server uses SSL, you need to use the `SMTP_SSL` class instead.

Once the connection is opened, you can send the message like this:

### Web Crawling

The `urllib` in Python handles communication over several different protocols.

To talk to a web server, you need to use the `urllib.request` submodule.

### Post to a Web Page

If you need to submit a web form, you know that you should send `POST` request to the web page. And that's exactly what we will do.

Note that we can use `mechanize` or `urllib2` -- there are many ways to achieve this.

### Create a Mini Server

The socket class from the Python standard library supports listening for incoming connections.

You may get a warning from your firewall, depending on the settings used on your machine.

After the socket has been created, you need to explicitly accept incoming connections:

Also, don't forget to close the connection after you've finished: `conn.close()`.

## Threading in Python Programming

Running multiple processes in parallel, which is called threading, is very useful -- especially when you need to run a process in a different thread and keep your current thread unattached to avoid freezing.

The Python standard library contains a module named `threading` that contains a thread class.

If the function takes a long time to finish, you can check to see whether it is still running by using the `is_alive()` method.

Sometimes, your threads need to access global resources safely. You can do that using locks.
    
    
    my_thread = threading.Thread(target=my_func)

## Using Raspberry Pi

With Raspberry Pi, you can create your own technology. It's a single board computer that comes at a cheap price. You can use the Python module `RPi.GPIO` to work with a Raspberry PI.

First, install the package in your Raspberry PI: `$ sudo apt-get install python-dev python-rpi.gpio`.

Now, you can use it in your scripts. You can write output on the Raspberry Pi's `GPIO` bus:

### Reading From the Raspberry Pi's GPIO

You can use the `RPi.GPIO` Python module to read data in from the `GPIO` like this:
    
    
    RPi.GPIO.setup(1, GPIO.IN)

We've actually only covered a tiny bit of Python; there is a lot to cover.

I promise you that I will do my best on the upcoming Python posts to cover Python programming language basics. Then, we can start building awesome tools.

[Check out](https://dzone.com/go?i=200130&u=http%3A%2F%2Fhubs.ly%2FH06Pr9h0) the Exaptive data application Studio. Technology agnostic. No glue code. Use what you know and rely on the community for what you don't. [Try the community version](https://dzone.com/go?i=200130&u=https%3A%2F%2Fexaptive.city%2F%23%2Flanding%3Freferrer%3DGeneral).

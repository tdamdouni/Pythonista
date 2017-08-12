# Building an API in 3 minutes with Bottle + Python

_Captured: 2015-12-14 at 01:20 from [www.adhikary.net](http://www.adhikary.net/2015/07/06/building-an-api-in-3-minutes-with-bottle-python/)_

We all had those times when we needed to build a simple API pushing out JSON, and didn't want to go into a s**t load of trouble for doing so. If you are a pythonista, bottle might be your best bet to do it quick. We are going to build a simple API with one endpoint, spitting out a list of movies.

Start off by installing bottle, globally or in a virtualenv (recommended)
    
    
    pip install bottle

Next up, open a new plain text file, I am calling it my_cool_api.py and import two methods from bottle; also importing the JSON library for exporting our objects as JSON.

Let's make a list of movies.

Now for the fun part, I will get a list of movies when I call the /movies endpoint. Let's define a method. We are declaring the endpoint as a @route decorator, and defining a function / method that does the job when this endpoint is called. This method is simply dumping the content of the list of movies as JSON.

Finally, making sure the server actually runs. This bit is quite self-explanatory.

Now, let's run the api server and point our browser to http://localhost:8080/movies.
    
    
    python my_cool_api.py

And voila! A simple API ready for action. You can use various databases, WSGI-compatible webservers along with bottle, for more checkout the official documentation of Bottle.

# Writing a Web Service Using Python Flask

_Captured: 2017-01-31 at 23:58 from [dzone.com](https://dzone.com/articles/writing-a-web-service-using-python-flask?edition=266901&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-01-31)_

Many of our customers are building useful services using our [webhook feature](https://threatstack.zendesk.com/hc/en-us/articles/206499124-Threat-Stack-Webhooks-Integration) -- but unfortunately, others are not. Often we hear that no one on their team is proficient enough to write a service that can ingest a webhook payload and do something with the data. That leaves them either hoping to get cycles from their development team (unlikely) or continuing to do without.

But what if you could write your own web services? How many routine tasks that involve taking data from system A and inputting it into system B could you automate?

Learning to code well enough can be a major skill in your tool chest and a major asset for optimizing security processes in your organization.

So in this post, I'm going to walk you through a tutorial that will get you started on the road to writing your own web services using Python Flask.

## What We're Building

I'm going to walk through the creation of a simple Python Flask app that provides a RESTful web service. Specifically, the service will provide an endpoint to:

  * Ingest a JSON formatted payload (webhook) from Threat Stack
  * Parse the payload for Threat Stack Alert IDs
  * Retrieve detailed alert data from Threat Stack
  * Archive the webhook and alert data to AWS S3

But before we jump in, here are a couple of things to keep in mind:

  * We will not be bothering with any sort of frontend display functionality, so you don't need to worry about HTML or CSS.
  * Our organization follows Flask's own [suggested organization](http://exploreflask.com/en/latest/organizing.html). We are going to skip the single module pattern and go straight to the [Packages and Blueprints models](http://exploreflask.com/en/latest/organizing.html).
  * There's a large range of Flask tutorials. On one hand, there are tutorials that explain how to build small, simple apps (where the entire app fits in a single file). On the other hand, there are tutorials that explain how to build much larger, complicated apps. **This tutorial fills a sweet spot in the middle and demonstrates a structure that is simple, but which can immediately accommodate increasingly complex requirements.**

## Project Structure

The structure of the project that we're going to build, which comes from [Explore Flask](http://exploreflask.com/en/latest/organizing.html), is shown below:

threatstack-to-s3

├── app

│ ├── __init__.py

│ ├── models

│ │ ├── __init__.py

│ │ ├── s3.py

│ │ └── threatstack.py

│ └── views

│ ├── __init__.py

│ └── s3.py

├── gunicorn.conf.py

├── requirements.osx.txt

├── requirements.txt

└── threatstack-to-s3.py

Let's start the discussion with the top-level files that are useful to us as we build the service:

  * **gunicorn.conf.py:** This is a configuration file for the Gunicorn WSGI HTTP server that will serve this app up. While the application can run and accept connections on its own, Gunicorn is more efficient at handling multiple connections and allowing the app to scale with load.
  * **requirements.txt / requirements.osx.txt:** The app's dependencies are listed in this file. It is used by the "pip" utility to install the needed Python packages. For information on installing dependencies, see the Setup section of this [README.md](https://github.com/threatstack/threatstack-to-s3/blob/master/README.md#setup).
  * **threatstack-to-s3.py:** This is the application launcher. It can be run directly using "python" if you are doing local debugging, or it can be passed as an argument to "gunicorn" as the application entry point. For information on how to launch a service, see [README.md](https://github.com/threatstack/threatstack-to-s3/blob/master/README.md#setup).

## app Package (app/ Directory)

The app package is our application package. The logic for the application is underneath this directory. [As mentioned earlier](http://blog.threatstack.com/writing-a-web-service-using-python-flask#SimpleStr), we have chosen to break the app into a collection of smaller modules rather than use a single, monolithic module file.

The following four usable modules defined in this package are:

These are described below.

**Note: **[app.views](https://github.com/threatstack/threatstack-to-s3/blob/phase_1_s3_achiving/app/views/__init__.py) and [app.models](https://github.com/threatstack/threatstack-to-s3/blob/phase_1_s3_achiving/app/models/__init__.py) do not provide anything. See that their __init__.py files are empty.

### app Module

The **app module** has the job of creating the Flask application. It exports a single function, **_create_app()_**, that will create a Flask application object and configure it. Currently it initializes application blueprints that correspond to our application views. Eventually, **_create_app()_**will do other things such as initialize logging, but we've skipped that now for clarity and simplicity.

#### **_app/__init__.py_**

This module is used by **_threatstack-to-s3.py_** to start the application. See that it imports **_create_app()_**and then uses it to create a Flask application instance.

#### **_ threatstack-to-s3.py_**

## views and Flask Blueprints

Before discussing the remaining three modules, we'll talk about what views and Flask blueprints are before diving into the app.views.s3 module.

  * **views:** Views are what the application consumer sees. There's no frontend to this application, but there is a public API endpoint. It's easiest to think of a view as what can and should be exposed to the person or thing (e.g., the consumer) who is using this application. It is always a best practice to keep views as simple as possible. If an endpoint's job is to take data in and copy it to S3, we make it perform that function, but we hide the details of how that was done in the application models. Our views should mostly represent the actions a consumer wants to see happen, while the details (which consumers shouldn't care about) live in the application models (described later).
  * **Flask Blueprints:** that we are going to use a Packages and Blueprints layout instead of single module application. Blueprints contain a portion of our API endpoint structure. This let's us logically group related portions of our API. In our case, each view module is its own blueprint.

**Learn more:**

### app.views.s3 Module

The threatstack-to-s3 service takes Threat Stack webhook HTTP requests in and stores a copy of the alert data in S3. This is where we store the set of API endpoints that allow someone to do this. If you look back at [app/__init__.py](https://github.com/threatstack/threatstack-to-s3/blob/phase_1_s3_achiving/app/__init__.py#L8), you will see that we have rooted the set of endpoints at **/api/v1/s3**.

#### **_From app/__init__.py:_**

I used this path for a few reasons:

  * **api:** To note that this is an API and you should not expect a front end. Maybe one day I'll add a frontend. Probably not, but I find this useful mentally and as a sign to others.
  * **v1:** This is version 1 of the API. If I need to make breaking changes to accommodate new requirements, I can add a v2 so that two APIs exist as I migrate all consumers over to the new version.
  * **s3:** This is the service we're connecting to and manipulating. You have some freedom here to name this portion of the path whatever you want, but I like to keep it descriptive. If the service was relaying data to HipChat, for example, you could name this portion of the path **_hipchat_**.

In **_app.views.s3_**, we are providing a single endpoint for now,**_/alert_**, which represents the object we're manipulating, that responds only to the HTTP POST request method.

**Remember:** When you are building APIs, url paths should represent nouns, and HTTP request methods should represent verbs.

#### **_app/views/s3.py_**

Now, let's walk through some key parts of the module. If you are familiar enough with Python, you can skip the next few lines on imports. But if you're wondering why I rename what I import, then follow along.

I'm a fan of typing brevity and consistency. I could have done this the following way to import the model modules:

But that would mean I'd be using functions like:

I could have done this as well:

That, however, would break when I create the s3 Blueprint object a few lines later because I'd overwrite the s3 model module.

For these reasons, it is just easier to import the model modules and rename them slightly.

Now let's walk through the app endpoint and function associated with it.

The first line is called a decorator. We're adding a route to the s3 Blueprint called **_/alert_**, which expands to **_/api/v1/s3/alert_**, that when an HTTP POST request is made to it, will cause **_put_alert()_**to be called.

The body of the function is pretty simple:

  * Get the request's JSON data.
  * Iterate over the array in the alerts key.
  * For each alert: 
    * Retrieve the alert detail from Threat Stack.
    * Store the alert info in the request in S3.
    * Store the alert detail in S3.

Once that's done, we return a simple JSON doc back, indicating the success or failure of the transaction. (**Note:** There's no error handling in place, so of course we've hardcoded the success response and HTTP status code. We'll change that when error handling is added at a later date.)

At this point, we have satisfied our request and done what the consumer asked for. Notice that there is no code demonstrating how we fulfilled the request. What did we have to do to get the alert's detail? What actions did we perform to store the alert? How are the alerts stored and named in S3? The consumer doesn't really care about those details. That's a good way to think about organizing your code in your own service: What the consumer needs to know about should live in your view. The details the consumer doesn't need to know should live in your model, which we are about to cover.

Before discussing the remaining modules, we'll talk about models, which are how we talk to the services we're using such as Threat Stack and S3.

## models

Models describe "things," and these "things" are what we want to perform actions on. Typically when you search for help on Flask models, blogs and documentation like to use databases in their examples. While what we're doing right now isn't far off, we're just storing data in an object store instead of a database. It's not the only sort of thing we might do in the future with the data received from Threat Stack.

Additionally, I've chosen to skip an object oriented approach and have used a procedural style. In more advanced Python, you would model an alert object and provide a means of manipulating it. But this introduces more complexity than is needed for the given task of storing data in S3 and also makes the code more complicated for demonstrating a simple task. I've chosen brevity and clarity over technical correctness for this.

### app.models.threatstack Module

The app.models.threatstack module, as you can guess, handles communication with Threat Stack.

Just a quick run through of a few spots of note:

We don't want to keep the Threat Stack API in our code. That's just good clean code/security living. We're going to get the API key from our environment for now because it's a quick and simple solution. At some point, we should centralize all configuration in a single file instead of hiding it here so the code and setup are a little cleaner. That's a job for another time, and for now the setup is documented in [README.md](https://github.com/threatstack/threatstack-to-s3/blob/master/README.md#setup).

The **_get_alert_by_id()_**function takes an alert ID, queries the Threat Stack platform for the alert data, and returns that data. We're using the Python [requests module](http://docs.python-requests.org/en/master/) to make an HTTP GET request to the Threat Stack API endpoint that returns alert info for the given alert.

The Threat Stack API documentation is located at:

### app.models.s3 Module

The **app.models.s3** module handles connectivity to AWS S3.

Let's walk through the interesting parts:

Again, there's no config file for this app, but we need to set an S3 bucket name and optional prefix. We should fix this eventually . . . But the setup is documented in the [README.md](https://github.com/threatstack/threatstack-to-s3/blob/master/README.md#setup), which is good enough for now.

The functions _**put_webhook_data()**_ and _**put_alert_data()**_ have a lot of duplicate code. I haven't refactored them because it's easier to see the logic before refactoring. If you look closely, you'll realize that the only difference between them is how the alert_key is defined. Let's focus on **_put_webhook_data()_** then.

This function takes in a single argument named alert. Looking back at **_app/views/s3.py_**, _**alert**_ is just the JSON data that was sent to the endpoint. Webhook data is stored in S3 by date and time. The alert 587c0159a907346eccb84004 occurring at 2017-01-17 13:51 is stored in S3 as webhooks/2017/01/17/13/51/587c0159a907346eccb84004.

We start by getting the alert time. Threat Stack has sent the alert time in milliseconds since the Unix epoch, and that needs to be converted into seconds, which is how Python handles time. We take that time and parse it into a string that will be the directory path. We then join the top-level directory where we store webhook data, the time-based path, and finally the alert ID to form the path to the webhook data in S3.

[Boto 3](https://boto3.readthedocs.io/en/latest/) is the primary module in Python for working with AWS resources. We initialize a **_boto3_** client object so we can talk to S3 and put the object there. **_s3_client.put_object()_**is fairly straight forward with its **_Bucket_** and **_Key_** arguments, which are the name of the S3 bucket and the path to the S3 object we want to store.The **_Body_** argument is our alert converted back to a string.

## Wrapping Up...

What we have now is a functional Python Flask web service that can take a Threat Stack webhook request, get the alert's detail, and archive it in S3. It's a great start, but there's still more to be done for this to be production ready. Immediately you might be asking, "What happens if something goes wrong?" There's no exception handling to deal with issues such as communication failures with Threat Stack or S3. That was intentionally omitted to keep the code clear. There's also no authorization key checking. This means that anyone can send data to it. (And since we don't do any error checking or exception handling, they can crash the service.) There's also no TLS encryption handling. That's something we'd leave up to Nginx or Apache, which would be the webserver fronting this application. All these and more are issues to be tackled before putting this web service into production. But for now this is a start that should help you become more comfortable as you start building your own services.

**Notes:**

The GitHub repository for this service is located at:

Since the application goes through revisions, you can find the version used in this blog post at:

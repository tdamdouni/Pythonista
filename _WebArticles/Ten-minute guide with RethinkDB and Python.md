# Ten-minute guide with RethinkDB and Python

_Captured: 2015-06-13 at 10:26 from [rethinkdb.com](http://rethinkdb.com/docs/guide/python/)_

From version 1.14, the Python driver for RethinkDB supports Python 2 and 3. Version 1.13 and older support Python 2 only.

![](http://rethinkdb.com/assets/images/docs/api_illustrations/10-minute-guide-python.png)

# Import the driver

First, start a Python shell:
    
    
    $ python
    

Then, import the RethinkDB driver:
    
    
    import rethinkdb as r
    

You can now access RethinkDB commands through the `r` module.

# Open a connection

When you first start RethinkDB, the server opens a port for the client drivers (`28015` by default). Let's open a connection:
    
    
    r.connect( "localhost", 28015).repl()
    

The `repl` command is a convenience method that sets a default connection in your shell so you don't have to pass it to the `run` command to run your queries.

**Note:** the `repl` command is useful to experiment in the shell, but you should pass the connection to the `run` command explicitly in real applications. See [an example project](//github.com/rethinkdb/rethinkdb-example-flask-backbone-todo) for more details.

# Create a new table

By default, RethinkDB creates a database `test`. Let's create a table `authors` within this database:
    
    
    r.db("test").table_create("authors").run()
    

The result will be:
    
    
    {
        "config_changes": [
            <table configuration data>
        ],
        "tables_created": 1
    }
    

(The `config_changes` field contains metadata about the newly created table; for more details, read about the [table_create](http://rethinkdb.com/api/python/table_create/) command.) There are a couple of things you should note about this query:

  * First, we select the database `test` with the `db` command.
  * Then, we add the `table_create` command to create the actual table.
  * Lastly, we call `run()` in order to send the query to the server.

All ReQL queries follow this general structure. Now that we've created a table, let's insert some data!

# Insert data

Let's insert three new documents into the `authors` table:
    
    
    r.table("authors").insert([
        { "name": "William Adama", "tv_show": "Battlestar Galactica",
          "posts": [
            {"title": "Decommissioning speech", "content": "The Cylon War is long over..."},
            {"title": "We are at war", "content": "Moments ago, this ship received..."},
            {"title": "The new Earth", "content": "The discoveries of the past few days..."}
          ]
        },
        { "name": "Laura Roslin", "tv_show": "Battlestar Galactica",
          "posts": [
            {"title": "The oath of office", "content": "I, Laura Roslin, ..."},
            {"title": "They look like us", "content": "The Cylons have the ability..."}
          ]
        },
        { "name": "Jean-Luc Picard", "tv_show": "Star Trek TNG",
          "posts": [
            {"title": "Civil rights", "content": "There are some words I've known since..."}
          ]
        }
    ]).run()
    

We should get back an object that looks like this:
    
    
    {"unchanged":0,"skipped":0,"replaced":0,"inserted":3,"generated_keys":["7644aaf2-9928-4231-aa68-4e65e31bf219","064058b6-cea9-4117-b92d-c911027a725a","543ad9c8-1744-4001-bb5e-450b2565d02c"],"errors":0,"deleted":0}

The server should return an object with zero errors and three inserted documents. We didn't specify any primary keys (by default, each table uses the `id` attribute for primary keys), so RethinkDB generated them for us. The generated keys are returned via the `generated_keys` attribute.

There are a couple of things to note about this query:

  * Each connection sets a default database to use during its lifetime (if you don't specify one in `connect`, the default database is set to `test`). This way we can omit the `db('test')` command in our query. We won't specify the database explicitly from now on, but if you want to prepend your queries with the `db` command, it won't hurt.
  * The `insert` command accepts a single document or an array of documents if you want to batch inserts. We use an array in this query instead of running three separate `insert` commands for each document.

# Retrieve documents

Now that we inserted some data, let's see how we can query the database!

## All documents in a table

To retrieve all documents from the table `authors`, we can simply run the query `r.table('authors')`:
    
    
    cursor = r.table("authors").run()
    for document in cursor:
        print(document)
    

The query returns the three previously inserted documents, along with the generated `id` values.

Since the table might contain a large number of documents, the database returns a cursor object. As you iterate through the cursor, the server will send documents to the client in batches as they are requested. The cursor is an iterable Python object so you can go through all of the results with a simple `for` loop.

## Filter documents based on a condition

Let's try to retrieve the document where the `name` attribute is set to `William Adama`. We can use a condition to filter the documents by chaining a `filter` command to the end of the query:
    
    
    cursor = r.table("authors").filter(r.row["name"] == "William Adama").run()
    for document in cursor:
        print(document)
    

This query returns a cursor with one document--the record for William Adama. The `filter` command evaluates the provided condition for every row in the table, and returns only the relevant rows. Here's the new commands we used to construct the condition above:

  * `r.row` refers to currently visited document.
  * `r.row['name']` refers to the value of the field `name` of the visited document.
  * The `==` operator is overloaded by the RethinkDB driver to execute on the server. It returns `True` if two values are equal (in this case, the field `name` and the string `William Adama`).

Let's use `filter` again to retrieve all authors who have more than two posts:
    
    
    cursor = r.table("authors").filter(r.row["posts"].count() > 2).run()
    for document in cursor:
        print(document)
    

In this case, we're using a predicate that returns `True` only if the length of the array in the field `posts` is greater than two. This predicate contains two commands we haven't seen before:

  * The `count` command returns the size of the array.
  * The `>` operator is overloaded by the RethinkDB driver to execute on the server. It returns `True` if a value is greater than a certain value (in this case, if the number of posts is greater than two).

## Retrieve documents by primary key

We can also efficiently retrieve documents by their primary key using the `get` command. We can use one of the ids generated in the previous example:
    
    
    r.db('test').table('authors').get('7644aaf2-9928-4231-aa68-4e65e31bf219').run()
    

Since primary keys are unique, the `get` command returns a single document. This way we can retrieve the document directly without iterating through a cursor.

Learn more about how RethinkDB can efficiently retrieve documents with [secondary indexes](http://rethinkdb.com/docs/secondary-indexes/javascript/).

# Realtime feeds

Feel free to skip this section if you don't want to learn about realtime feeds yet. You can always go back and start a feed later.

RethinkDB inverts the traditional database architecture by exposing an exciting new access model - instead of polling for changes, the developer can tell RethinkDB to continuously push updated query results to applications in realtime.

To start a feed, open a new terminal and open a new RethinkDB connection. Then, run the following query:
    
    
    cursor = r.table("authors").changes().run()
    for document in cursor:
        print(document)
    

Now switch back to your first terminal. We'll be updating and deleting some documents in the next two sections. As we run these commands, the feed will push notifications to your program. The code above will print the following messages in the second terminal:
    
    
    {"new_val":{"id":"1d854219-85c6-4e6c-8259-dbda0ab386d4","name":"Laura Roslin","posts":[...],"tv_show":"Battlestar Galactica","type":"fictional"},"old_val":{"id":"1d854219-85c6-4e6c-8259-dbda0ab386d4","name":"Laura Roslin","posts":[...],"tv_show":"Battlestar Galactica"}}

RethinkDB will notify your program of all changes in the `authors` table and will include the old value and the new value of each modified document. See the [changefeeds](http://rethinkdb.com/docs/changefeeds) documentation entry for more details on how to use realtime feeds in RethinkDB.

# Update documents

Let's update all documents in the `authors` table and add a `type` field to note that every author so far is fictional:
    
    
    r.table("authors").update({"type": "fictional"}).run()
    

Since we changed three documents, the result should look like this:
    
    
    {
        "unchanged": 0,
        "skipped": 0,
        "replaced": 3,
        "inserted": 0,
        "errors": 0,
        "deleted":0
    }
    

Note that we first selected every author in the table, and then chained the `update` command to the end of the query. We could also update a subset of documents by filtering the table first. Let's update William Adama's record to note that he has the rank of Admiral:
    
    
    r.table("authors").
        filter(r.row['name'] == "William Adama").
        update({"rank": "Admiral"}).run()
    

Since we only updated one document, we get back this object:
    
    
    {
        "unchanged": 0,
        "skipped": 0,
        "replaced": 1,
        "inserted": 0,
        "errors": 0,
        "deleted": 0
    }
    

The `update` command allows changing existing fields in the document, as well as values inside of arrays. Let's suppose Star Trek archaeologists unearthed a new speech by Jean-Luc Picard that we'd like to add to his posts:
    
    
    r.table('authors').filter(r.row["name"] == "Jean-Luc Picard").
        update({"posts": r.row["posts"].append({
            "title": "Shakespeare",
            "content": "What a piece of work is man..."})
        }).run()
    

After processing this query, RethinkDB will add an additional post to Jean-Luc Picard's document.

Browse the [API reference](http://rethinkdb.com/api/python/) for many more array operations available in RethinkDB.

# Delete documents

Suppose we'd like to trim down our database and delete every document with less than three posts (sorry Laura and Jean-Luc):
    
    
    r.table("authors").
        filter( r.row["posts"].count() < 3 ).
        delete().run()
    

Since we have two authors with less than two posts, the result is:
    
    
    {
        "unchanged": 0,
        "skipped": 0,
        "replaced": 0,
        "inserted": 0,
        "errors": 0,
        "deleted": 2
    }
    

# Learn more

**Want to keep learning?** Dive into the documentation:

  * Read the [introduction to RQL](http://rethinkdb.com/docs/introduction-to-reql/) to learn about the ReQL concepts in more depth.
  * Learn how to use [table joins](http://rethinkdb.com/docs/table-joins/) in RethinkDB.
  * Jump into the [cookbook](http://rethinkdb.com/docs/cookbook/javascript/) and browse through dozens of examples of common RethinkDB queries.

# The Future of Asynchronous IO in Python

_Captured: 2015-06-12 at 22:43 from [medium.com](https://medium.com/p/ce200536d847)_

_Disclaimer: I'm an engineer with 10+ years of backend development for web, most of the career spent on writing Python code. So most of this text may be not relevant for other areas of software development. Likewise it's not relevant to people using JVM or CLR, they just solve issues in different way._

Developing web applications today does look very different from what we have been doing 10 years ago. Now we build everything as number of microservices. It drastically changes architecture of our application.

> If you are still building monolithic web app in 2014, you need to fix it,  
or you'll be fired soon.

While design of our applications changed a lot. Our tools don't. I'm going to describe how I would like to write microservices in the future. But first let's look what we have.

### Global Interpreter Lock

The infamous Python GIL, which pythonistas speak a lot is there for other scripting languages too (Ruby, Perl, Node.js, to name a few). It's conventional source of holy-wars about bad language interpreter design, but it was never a problem for web applications. We have always relied on many processes sharing only a database.

With microservices global interpreter lock is even less the problem. In most cases single microservice is even smaller than typical web application a decade ago. Being smaller, it also serves bigger number of requests per second, mostly because it's highly specialized and well tuned for the kind of queries it have.

What starts becoming an issue when building microservices is time needed to wait for reply of other service. That's where comes into play…

### Asynchronous I/O

> "Asynchronous I/O, or non-blocking I/O is a form of input/output processing that permits other processing to continue before the transmission has finished."  
-- Wikipedia

What's any asynchronous library does is basically turning the kind of code flow on the left to the flow on the right:

![](https://d262ilb51hltx0.cloudfront.net/max/1069/1*XZlkILfsMj8nOnnXj5bnqw.png)

> _Synchronous (left) vs asynchronous (right) request processing_

The support of asynchronous I/O in Python is pretty much good. There are tons of libraries which do the work (Twisted, Tornado, Gevent, Eventlet, Asyncio to name a few). Each library supports numerous of protocols. You can use MySQL, Mongo, PostgreSQL, Redis, Memcache, ElasticSearch,… well, pretty much every DB, and many other services. Some exotic protocols, like SSH or Beanstalk are supported only in several libraries. But even that's not usually a problem, as writing another protocol or port it from one I/O framework to another is not that hard.

Of course every I/O library support both client-side and server-side HTTP. Presumably it is the reason why HTTP is the most common protocol used for messaging between microservices. But most of the frameworks support various other protocols too (msgpack-rpc, thrift, zeromq, ice, to name a few).

There are many frameworks, which differ merely in convenience of using various protocols and other kinds of concurrency abstractions. While support of various protocols is being more and more prevalent. Nothing has really changed since Twisted was published in 2002. Yeah, a lot of convenience added when python has grown _yield_ and when stackless and _greenlets_appeared, but that's really just a little bit convenience. The real change was back then in 2002.

But there are something that most Python frameworks weak at. When you can handle many client requests in single process, potentially you can pipeline them into a single upstream connection. I.e. if you have three GET requests in frontend, you might send three requests to the MySQL, not waiting for the answer. And reply to the client as fast as they come back. Just like displayed in the picture above, but using single DB connection. Most python frameworks now, require pulling a connection from the pool at the start of request, and release it back at the end of request, effectively having a connection number equal to number of simultaneous requests.

Thousands of connections to a database is still a problem for many of them. Even classic sharding doesn't help, as you need same number of connections per each shard. Many users adopt a special microservice that does nothing but pipelining (pgbalancer as an example). And that's not only a problem for the DB. There are many microservices that suffer from the same problem.

Fortunately architecture of asyncio allows to make pipelining easy to write, so more and more asyncio protocols adopt this technique. Unfortunately the databases for which connections are expensive (namely MySQL and PostgreSQL), have C library which doesn't really allow that, and nobody cares enough to write nicer one.

### Publish-Subscribe as a Resque

Today, many engineering teams build a microservices architecture around single big pub-sub bus. I.e. they run RabbitMQ or one of many it's competitors and just publish everything as a message. They believe it simplifies their architecture:

  1. Single bus, no need to think of it any more
  2. Can publish messages without waiting for reply. Effectively getting asynchronous I/O without any async library whatsoever

While there are engineers that think it's an answer, I don't believe in that in generic case.

> I don't believe that limiting my design decisions to the use of particular broker with particular message dispatching algorithm would solve all my networking problems

### Zeromq and Nanomsg Way

Another thing that is charming for microservice architecture is Zeromq. If you are not familiar with it you should learn it as soon as possible. Zeromq have the MQ (message queue) suffix merely by coincidence, as there is no central message queue which is the case for RabbitMQ, Kafka, and others. It's a small library that provides _sockets on steroids_. I.e. something that looks mostly like a normal socket, but does automatic message delimitation (splits TCP stream into frames), reconnection, load-balancing between peers, etc.

In Zeromq world there are basically three ways your service communicates with the world:

  1. Publish-subscribe, which works mostly as pubsub in other apps
  2. Request-reply, which basically how RPC works everywhere
  3. Push-pull which is request without reply, or pub-sub which delivers message to a single respondent (based on round-robin)

The Nanomsg is going a step further, as it supports all of the above, and adds more _communication patterns _(in terms of nanomsg):

  1. Surveyor-respondent, which allows to send requests to the multiple peers and receive requests from all
  2. Bus, which allows sending a message to every peer

Even more: the promise of nanomsg is that communication patterns will be _pluggable_, i.e. more communication patterns will be invented and added to the library in future.

> I believe that more communication patterns should emerge in the near future. And using Pub-sub or HTTP for everything is doomed

What's also useful for scripting languages that both nanomsg and zeromq do: they are handling I/O in a separate thread. So while you are doing some stuff in python code holding GIL, your zeromq thread keeps your connections running, flushing message buffers, accepting and establishing connections, etc.

### The Real World of Microservices

While cool hackers are building nice things like zeromq, or nanomsg or publish-subscribe buses, _real engineers _continue to build things the old way.

I don't know a single database that uses zeromq for database access. There are very little number open-source services that use zeromq. Basically all modern databases are divided into two camps:

  1. Invent their own protocol
  2. Use HTTP

The database example is just most prominent one. As another example Docker uses HTTP over unix sockets for communication. And it just shamelessly breaks protocol semantics when it needs full-duplex streams instead request-reply.

#### The HTTP Protocol

I have to say just a few words about HTTP.

_Some HTTP support_ is ubiquitous, but it's also vaguely inefficient in Python. Not only it can't be handled in separate thread like in zeromq, and not just HTTP parsing is slow. Often keep-alive connections are not supported well.

Also HTTP is complex. If you think it isn't, you're wrong. Just to give you a little example. You may write code like below:
    
    
    def simple_app(environ, start_response):  
        status = '304 Not Modified'  
        headers = [('Content-Length', '5')]  
        start_response(status, headers)  
        return [b'hello']

What happens here is that server returns a page with word "hello" in the body of response (tested with wsgiref). But what spec says:

> The 304 response MUST NOT contain a message-body, and thus is always terminated by the first empty line after the header fields

What this means is that the "hello" line will be treated by client as a first line of the response on the **next** request. Which in some setups leads to poisoning cache and security vulnerabilities. How many programmers that use HTTP are aware of this fact? There are many more subtle details.

> The HTTP must not be used for internal messaging as it's easy, but not simple, quite the contrary it's complicated protocol with 5 RFCs describing only basics. And misunderstanding smallest part of spec may lead to a security vulnerability

Frankly, most microservices use subset of HTTP which for example only recognize response code 200 (and all others as failure) don't use special headers and similar, and may never run into issues. Still this is not real HTTP (but proxies, i.e. HAProxy often used for load-balancing, expect real HTTP), and one should be very fluent in HTTP spec to find out the safe subset of it.

#### So What's Wrong With Zeromq

First it's not very versatile piece of software:

  1. It's hard to hack on (it's C++ with complex Actors model)
  2. It doesn't embed well into some programs (e.g. it doesn't play well with fork)
  3. It doesn't integrate well into failover and service discovery
  4. It still doesn't handle well non-idempotent requests, and stateful routing.

While nanomsg better at (1) still far from perfect. The (2) can't be solved with current design. The (3) solves nanoconfig library for nanomsg, which received even less attention comparing to nanomsg itself. The (4) might eventually be solved in nanomsg, but it's not close yet.

The second big reason is that engineers just not get used to it's way of thinking (e.g. redis protocol uses pub-sub and req-rep over same connection, mongo does push-pull and req-rep over same connection, zeromq just doesn't allow that). This is something nanomsg specifically tries to fix in engineers mind, and this is a long jorney.

Don't take me wrong. Zeromq is good. And nanomsg learned from the mistakes a lot, and will be my first choice for messaging between services when become production ready. But nanomsg itself doesn't solve all networking problems for python.

#### But What's Wrong With Microservices?

Okay. The easy part is that most of the time you can't build even a tiny service with only zeromq. But if your DB speaks HTTP you can build service with a HTTP at both sides as a client and as a service. That _feels _easy (but remember HTTP is complicated).

Another thing that is broken is I/O model. When you have a single-threaded code, you can't reliably heartbeat your connections while you don't use them. Even if you have asynchronous loop, it can stall for long time doing some computation.

So sometimes you are trying to send request to a connection, but it have already been closed. And there is a widely adopted hack, to read from connection, checking if it's still alive, because it's often hard to recover after trying to send request:
    
    
    if s.read() == b'':  
      self.reconnect()  
    s.write(request)  
    response = s.read()

But it all means that connection is starting to establish only when you do request, instead of being already ready as the case when using zeromq or nanomsg.

It's also hard to do service discovery this way. You have three easy choices:

  1. Check service name (e.g. resolve DNS) before each request
  2. Resolve service name on next connection request
  3. Never update service (i.e. until restart of a process)

And most users just use (3)rd choice. Sometimes (2) works out of the box, but it works only in cases when failover takes place when machine is not reachable. And (1) is quite ineffecient, so almost never done.

### I/O Kernel Design

![](https://d262ilb51hltx0.cloudfront.net/max/600/1*wkZfpRYC9-c3Qiz7QZZFXQ.png)

So I propose to redesign all IO subsystem. I.e. write a library in C (or any other GIL-less language), that handle IO independent of main application thread. It should contact with main python thread using some kind of messaging. But it must not send Python objects, to never hold GIL in I/O thread.

The I/O kernel must speak many application protocols and for each protocol it should be able to (a) process hanshake and (b) delimit stream into messages so that it transfer only fully received messages to main thread. Better if it can devise connection details, such as master/slave relations for automatic failover.

The I/O thread should be able to resolve names, handle connection attempts, be able to subscribe on DNS name changes and do other high-level stuff.

Note this might be useful not only for Python, but also for any scripting language that has GIL. In fact in will work nice even with GIL-less languages, just may have less need for it.

### Previous Work

The idea is partially exists in many products:

  1. Already mentioned zeromq and nanomsg handle I/O in different thread(s)
  2. Kazoo, which is pythonic implementation zookeeper protocol, uses a separate (pythonic) thread for reconnecting and pinging connections
  3. Twisted offloads blocking computations to thread pool (although, we need reverse thing, still this is work offloading)

Probably there are more examples. Still I've seen no attempts to build some unified kernel for I/O in separate thread. If you know some, please let me know.

Also the pattern has similarities with recently emerging Ambassador pattern. Ambassador is a process which sits on every machine, and does service discovery, but proxies all connections through itself. I.e. every service connects to some port at localhost where Ambassador listens and forwards connection to some real service(s). Similarly I/O Kernel must do service discovery and communication with service on behalf of main thread (still protocol probably should be very different from the one ambassador using).

### So What's The Point

> So is the point just to get few milliseconds out of performance?

Yes. This one too. In fact small millisecond-level delays add up pretty quickly when using multiple services to handle single frontend request. Also this technique saves from non-linear raise of latency when CPU usage approaches 100%.

> Or the point is keeping persistent connections? They work nice in traditional asynchronous I/O, if you're careful enough to yield CPU often

Right. You're already pretty good if you using Async I/O at all, as a lot of people still don't see the need. But how many async libraries do service discovery in sensible way? (My answer: None of them).

> But it's possible to do service discovery in asynchronous I/O too

Sure. But nobody does yet. I think this should be taken as an opportunity to fix this one too.

Also there are the following tasks that my imaginary I/O kernel should do:

#### Health Checks and Statistics

Sending statistics at regular intervals is hard for CPU intensive tasks. This should be fixed. The main thread should just increment counters in some memory region, completely independently of the I/O thread.

Also we get accurate timestamps of request-response timers. In typical case they are very skewed by the amount of work python main loop have to do.

With combination of correct service discovery, we should be able to notify that some required service is unavailable at this node, even before real user tried to execute a request on this worker.

#### Debugging

Imagine you can ask Python process to get state at any time. First we always have list of requests that currently in progress. Also we can attach some marker points, like with statistics. And finally we can use a technique similar to one used in _faulthandler _to find out what the stack of main thread.

The key point is that there is a thread that can answer debugging requests, even when main thread does something CPU intensive, or just hangs for some reason.

#### Pipelining

Requests must be pipelined as much as possible. I.e. no matter which frontend request requires database request, we send all of them through single database connection.

This allows not only keep number of DB connections low, but also allows us to gather statistics about which replica is slower.

#### Name Discovery

We must not only resolve DNS names (or whatever name resolution we choose), but also get updates when that name changes, for example by setting watch in zookeeper.

This process must be done transparently to the application, and connection must already be established, when application starts request.

#### Unification

Having I/O kernel in place. Various I/O frameworks in python just support all the protocols supported by kernel. Every new protocol should be done there. This allows frameworks to compete on convenience and efficiency rather than on protocol support.

#### Throttling

Even in Java and Go, where you can freely use threads there is often need for throttling number client connections. The described design allows to control number of requests in single place in the application, no matter which library is the real executor of the network request.

### Design Notes

Following are random thoughts about design of I/O kernel in no particular order. Some of them may be left out in the final design.

  1. The I/O kernel must be single threaded. As it's almost impossible to overload I/O thread in C with python code. This makes design choices much easier (e.g. comparing to that of nanomsg or zeromq)
  2. All I/O should be done in I/O thread with minimal interlocking. As it's often cheaper to wake up another thread than to execute couple of python bytecodes (and this leads to simpler design)
  3. Copying data from python objects is not expensive comparing to holding GIL. However, if it's possible should probably allocate non-pythonic buffer and serialize directly into it.
  4. Every protocol supported must at least be delimited into frames in C code. So that partial packets do not reach python code. Other parsing might be done in main thread directly in python objects.
  5. Service discovery must be pluggable. With most obvious choices implemented first (e.g. polling on a DNS name).
  6. Service discovery should be easily integrated into any protocol. In fact it must be easier to use service discovery than to omit it for protocol implementer.

### Wrapping Up

Well building such a tool is not a matter of a weekend. It's hard work, and definitely long journey.

Still now is a good time to start rethinking how we handle networking in Python. The recent tools like stable libuv and may be a rust language simplifies the building I/O kernel a lot. It may even be wise to prototype the code in go-python, which should be easy to do but not going to be long term solution.

The described solution looks like clean and simple to use. Hopefully, In the future it would allow us to build nice, high-performant services in Python, that play nice with dynamic network configuration. And not to suffer from templation of rewriting everything in other language on every apparent performance issue.

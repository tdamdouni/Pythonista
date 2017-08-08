# Goodbye Shell, Hello Python!

_Captured: 2017-05-23 at 03:45 from [dzone.com](https://dzone.com/articles/goodbye-shell-hello-python?edition=299094&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-05-22)_

Need to build an application around your data? [Learn more](https://dzone.com/go?i=200129&u=http%3A%2F%2Fhubs.ly%2FH06Pr9h0) about dataflow programming for rapid development and greater creativity.

As an Ops/DevOps professional, I have many years of experience writing Shell scripts. You're probably in a similar situation, right? I deeply treasure my achievements with Shell. Yes, I still do, even now. But I have to make a decision to (finally!) drop Shell and embrace Python.

Why is that? Check out this blog post and discuss with me.

It's really hard to reject the temptation of Shell. Shell is a very old and widely used language, but it's far from modern programming languages. Poor error handling, weird syntax, no package mechanism to reuse the code -- the list goes on and on…

  1. **Unix PIPE philosophy makes Shell the default glue language**. It integrates all kinds of (relatively) small tools, solving a bigger problem. So, if you check any popular online tutorials now, you will probably see Shell scripts somewhere.
  2. With Shell, it's super easy to **get your hands dirty and make progress**. Each Shell command you have issued in the terminal is a reward. It makes you feel that you're making constant progress. Hard to say no, isn't?
  3. **There's no extra wrapper layer**. Let's say you need to trigger some [ElasticSearch actions](http://www.dennyzhang.com/query_elasticsearch/) by programming. You can either call the ElasticSearch management REST API directly by Shell or use the ElasticSearch Python SDK. If you choose Python and the script is not working, then what? It could be some bugs in Python SDK or the way you use Python SDK. No doubt people are in favor of Shell scripting sometimes.

Regardless of all benefits, my DevOps fellows, we have to look ahead and move on.

I will choose Python as the default for all unattended scripts that will run automatically. There is still some room for Shell, for example, to quickly wrap up some commands and execute them manually from the terminal.

First of all, it doesn't necessarily need to be Python. It could be any modern programming languages you're comfortable with like Ruby, Golang, etc.

  1. **Reuse code and modules across projects**. With years' accumulation, I come up with a shell common library ([GitHub](https://github.com/DennyZhang/devops_public/tree/tag_v4/common_library)). With this library, I can easily and quickly accomplish lots of DevOps tasks -- for example, [enforce pre-checks before deployment](http://www.dennyzhang.com/enforce_precheck/), run deployment and maintenance via [Jenkins](http://www.dennyzhang.com/demo_jenkins/), etc. However, distributing the Shell scripts and upgrading them is quite a burden. With Python, I can easily pack up the logic as a pip package.
  2. **It's super hard to make decent and reliable Shell scripts**. Think you're a Shell ninja? Run [Shellcheck](http://www.dennyzhang.com/wp-admin/post.php?post=3657&action=edit) against your scripts. With the absence of error handling, your scripts can easily give you false positives. Consequently, it may incur serious damage or make troubleshooting difficult.
  3. **Easy requirements may not be easily supported**. For example, when you run the scripts, you want to see the output in both terminal and log files. With some research, you may finalize with the solution of the [tee command](http://www.dennyzhang.com/shell_tee/). However, you will have to deal with weird bash issues like [this one](http://www.dennyzhang.com/bash_errcode_exit/).

Now, my Python journey starts. What about yours?

Note: I will keep open source my DevOps Python scripts in [GitHub](https://github.com/DennyZhang/devops_public/tree/tag_v5/python).

[Check out](https://dzone.com/go?i=200130&u=http%3A%2F%2Fhubs.ly%2FH06Pr9h0) the Exaptive data application Studio. Technology agnostic. No glue code. Use what you know and rely on the community for what you don't. [Try the community version](https://dzone.com/go?i=200130&u=https%3A%2F%2Fexaptive.city%2F%23%2Flanding%3Freferrer%3DGeneral).

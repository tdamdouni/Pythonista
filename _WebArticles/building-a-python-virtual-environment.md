# Building a Python Virtual Environment

_Captured: 2017-06-09 at 22:50 from [dzone.com](https://dzone.com/articles/building-a-python-virtual-environment?edition=304154&utm_source=Daily%20Digest&utm_medium=email&utm_campaign=dd%202017-06-09)_

The DevOps Zone is brought to you in partnership with Sonatype Nexus. The [Nexus Suite](https://dzone.com/go?i=146021&u=https%3A%2F%2Fwww.sonatype.com%2Fnexus-lifecycle%3Futm_source%3DDZONE%2520-%2520Nexus%2520Lifecycle%2520-%2520September%25202016%26utm_medium%3DDZONE%2520-%2520Nexus%2520Lifecycle%2520-%2520September%25202016%26utm_campaign%3DDZONE%2520-%2520Nexus%2520Lifecycle%2520-%2520September%25202016) helps scale your DevOps delivery with continuous component intelligence integrated into development tools, including Eclipse, IntelliJ, Jenkins, Bamboo, SonarQube and more. [Schedule a demo today](https://dzone.com/go?i=146021&u=https%3A%2F%2Fwww.sonatype.com%2Fnexus-lifecycle%3Futm_source%3DDZONE%2520-%2520Nexus%2520Lifecycle%2520-%2520September%25202016%26utm_medium%3DDZONE%2520-%2520Nexus%2520Lifecycle%2520-%2520September%25202016%26utm_campaign%3DDZONE%2520-%2520Nexus%2520Lifecycle%2520-%2520September%25202016).

When embarking on a DevOps journey, getting a consistent development environment is key. In this post, I show how to setup a virtual environment and install the correct libraries necessary for a project.

## Virtual Environments: VirtualEnv

A Virtual Environment is a tool to keep the dependencies required by different projects in separate places, by creating [virtual Python environments](https://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) for them.

The tool in python is called `virtualenv` .

To work with isolated environments, you need to follow these steps:

  * **Initial Setup**
    * Install the `virtualenv` tool.
    * Initialize your environment.
    * Install dependencies.
    * Create the **requirements.txt** to remember the dependencies.
    * Check-in code and the requirements.txt file to code repository.
  * **Developer Installs**
    * Get the latest code.
    * Install virtual environment.
    * Install dependencies.
    * Start working on code.

Let's look into the steps in detail.

## Initial Setup

Before commencing the project, one of the developers can follow these steps to help get the team going. The first step is to install the `virtualenv` tool.

The next step is to initialize virtual environment on the project folder.

This step will install python, pip and basic libraries within the project folder, _myproject_. After version 1.7 of virtualenv, it will use the option **-no-site-packages** by default. It means that virtualenv will NOT install the libraries available globally. This will help ensure that the project package will contain the bare minimum libraries and the libraries installed for the specific project.

After this, you will need to activate the virtual environment to start working on the project.

Once you do this, your prompt will change to show that you are now working in a virtual environment. It should look something like this:

Now, go ahead and install the libraries that may be required for the project. If all the dependencies can be named at this stage, it will simply make it easier to replicate the environment. The dependency list can always be updated, as I'll show later.

Once done with the installations, create a list of the libraries and their versions.

This file _requirements.txt_ will hold the necessary dependencies for your project. In one of my projects, it looks like this:
    
    
    appdirs==1.4.3 asn1crypto==0.22.0 cffi==1.10.0 cryptography==1.8.1 enum34==1.1.6 idna==2.5 ipaddress==1.0.18 jsontree==0.4.3 ndg-httpsclient==0.4.2 packaging==16.8 pyasn1==0.2.3 pycparser==2.17 pyOpenSSL==17.0.0 pyparsing==2.2.0 requests==2.14.2 six==1.10.0 urllib3==1.21.1

This file will need to be checked in to your project code. At any time, if any other developer installs a new library, it will have to be added to this requirements.txt file. That way, once other developers pull the update from the source code repository, they will be made aware of the new dependencies.

## Developer Install

For each developer, the project setup is now straight-forward. They will need to install `virtualenv` .

Then, create a folder and activate virtual environment.

After this, they'll need to check-out the code from the code repository. Assuming it is a Git repo, this will just be a `git clone` command.

Now navigate to this sub-folder:

Install the dependencies:

That's it! Your developer machine is now all set for coding.

[This page](https://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/ for anything virtualenv) is an excellent reference for virtualenv.

I hope this post has been useful to you.

The DevOps Zone is brought to you in partnership with Sonatype Nexus. Use the [Nexus Suite](https://dzone.com/go?i=146022&u=https%3A%2F%2Fwww.sonatype.com%2Fget-nexus-sonatype%3Futm_source%3DDZONE%2520-%2520Get%2520Nexus%2520-%2520September%25202016%26utm_medium%3DDZONE%2520-%2520Get%2520Nexus%2520-%2520September%25202016%26utm_campaign%3DDZONE%2520-%2520Get%2520Nexus%2520-%2520September%25202016) to automate your software supply chain and ensure you're using the highest quality open source components at every step of the development lifecycle. [Get Nexus today](https://dzone.com/go?i=146022&u=https%3A%2F%2Fwww.sonatype.com%2Fget-nexus-sonatype%3Futm_source%3DDZONE%2520-%2520Get%2520Nexus%2520-%2520September%25202016%26utm_medium%3DDZONE%2520-%2520Get%2520Nexus%2520-%2520September%25202016%26utm_campaign%3DDZONE%2520-%2520Get%2520Nexus%2520-%2520September%25202016).

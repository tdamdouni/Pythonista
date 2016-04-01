#!/usr/bin/env python
# Written by: DGC

# http://sourcemaking.com/design_patterns/proxy
# give 4 good reasons for a proxy to be made.

# A virtual proxy is a placeholder for "expensive to create" objects. The real
# object is only created when a client first requests/accesses the object.
#
# A remote proxy provides a local representative for an object that resides in
# a different address space. This is what the "stub" code in RPC and CORBA 
# provides.

# A protective proxy controls access to a sensitive master object. The 
# "surrogate" object checks that the caller has the access permissions required
# prior to forwarding the request.

# A smart proxy interposes additional actions when an object is accessed. 
# Typical uses include: 
#   o Counting the number of references to the real object so that it can be 
#     freed automatically when there are no more references (aka smart pointer)
#   o Loading a persistent object into memory when it's first referenced,
#   o Checking that the real object is locked before it is accessed to ensure
#     that no other object can change it.


#==============================================================================
class SharedData(object):

    def __init__(self):
        self.resource = "A resource"

#==============================================================================
class AsyncProxy(object):

    def __init__(self, data):
        """ 
        Takes some data which should now only be accessed through this class, 
        otherwise you could get 
        """
        self.data = data


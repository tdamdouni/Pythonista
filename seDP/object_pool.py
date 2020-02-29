from __future__ import print_function
# https://forum.omz-software.com/topic/2307/copy-deepcopy-or-copy-copy-with-classes-using-ui-view

# https://gist.github.com/pazdera/1124839

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Example of `object pool' design pattern
# Copyright (C) 2011 Radek Pazdera

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


class Resource:

    """ Some resource, that clients need to use.
    
    The resources usualy have a very complex and expensive
    construction process, which is definitely not a case
    of this Resource class in my example.
    """

    __value = 0

    def reset(self):
        """ Put resource back into default setting. """
        self.__value = 0

    def setValue(self, number):
        self.__value = number

    def getValue(self):
        return self.__value


class ObjectPool:
    
    """ Resource manager.

    Handles checking out and returning resources from clients.
    It's a singleton class.
    """

    __instance = None
    __resources = list()

    def __init__(self):
        if ObjectPool.__instance != None:
            raise NotImplemented("This is a singleton class.")

    @staticmethod
    def getInstance():
        if ObjectPool.__instance == None:
            ObjectPool.__instance = ObjectPool()

        return ObjectPool.__instance

    def getResource(self):
        if len(self.__resources) > 0:
            print("Using existing resource.")
            return self.__resources.pop(0)
        else:
            print("Creating new resource.")
            return Resource()

    def returnResource(self, resource):
        resource.reset()
        self.__resources.append(resource)

def main():
    pool = ObjectPool.getInstance()

    # These will be created
    one = pool.getResource()
    two = pool.getResource()

    one.setValue(10)
    two.setValue(20)

    print("%s = %d" % (one, one.getValue()))
    print("%s = %d" % (two, two.getValue()))

    pool.returnResource(one)
    pool.returnResource(two)

    one = None
    two = None

    # These resources will be reused
    one = pool.getResource()
    two = pool.getResource()
    print("%s = %d" % (one, one.getValue()))
    print("%s = %d" % (two, two.getValue()))


if __name__ == "__main__":
    main()
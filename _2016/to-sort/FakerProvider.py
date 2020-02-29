# coding: utf-8

# https://forum.omz-software.com/topic/2514/share-code-markdownview/2

from __future__ import print_function
from faker import Faker
fake = Faker()

# first, import a similar Provider or use the default one
from faker.providers import BaseProvider

# create new provider class
class MyProvider(BaseProvider):
    def foo(self):
        return 'bar'
    
    def orange(self):
        return [fake.first_name(), fake.first_name()]

# then add new provider to faker instance
fake.add_provider(MyProvider)

# now you can use:
print(fake.foo())
print(fake.orange())
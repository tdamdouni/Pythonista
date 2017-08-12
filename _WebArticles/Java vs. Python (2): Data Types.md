# Java vs. Python (2): Data Types

_Captured: 2015-11-22 at 13:44 from [www.programcreek.com](http://www.programcreek.com/2012/09/java-vs-python-data-types/)_

If you know Java and want to quickly get a sense of how to use Python from the very beginning, the following summary can provide you a quick review of data types. You may also find the previous [comparison of Java and Python](http://www.programcreek.com/2012/04/java-vs-python-why-python-can-be-more-productive/) useful.

By comparing data types between Java and Python, you can get the difference and start using Python quickly. Comparision also can also help developers understand the common concepts shared by different programming languages.

Apparently, Java has more data types/structures than Python, so I will list the most similar concept from Java for the corresponding Python data types.

** 1\. Strings **

Java
Python
    
    
    //string
    String city = "New York";
    String state = "California";//has to be " not '
     
    String lines = "multi-line " +
    		"string";
    
    
    # Strings
    city = "New York"
    state = 'California'
     
    # multi-line string
    lines = """multi-line
    string"""
    moreLines = '''multi-line
    string'''

In python, string can reside in a pair of single quotes as well as a pair of double quotes. It supports multiplication: "x"*3 is "xxx".

**2\. Numbers **

Java
Python
    
    
    //integer numbers
    int num = 100;
     
    //floating point numbers
    float f = 1.01f; 
    //float f = 1.01;//wrong!
     
    double d = 1.01;
    
    
    # integer numbers
    num = 100
    num = int("100")
     
    # floating point numbers
    f = 1.01
    f = float("1.01")
     
    # null
    spcial = None

In Java, when you type something like 1.01, its interpreted as a double.  
Double is a 64-bit precision IEEE 754 floating point, while float is a 32-bit precision IEEE 754 floating point.  
As a float is less precise than a double, the conversion cannot be performed implicitly.

**3\. Null **

Java
Python
    
    
    //null
    Object special = null;
    
    
    # null
    spcial = None

**4\. Lists **

Java
Python
    
    
    //arraylist is closest with list in python
    ArrayList<Integer> aList = new ArrayList<Integer>();
     
    //add
    aList.add(1);
    aList.add(3);
    aList.add(2);
    aList.add(4);
     
    //index
    int n = aList.get(0);
     
    //get sub list
    List<Integer> subList = aList.subList(0, 2);
    //1, 3
    
    
    aList = []
    aList = [1, 'mike', 'john']
     
    #append
    aList.append(2)
     
    # extend
    aList.extend(["new","list"])
     
    print aList
    #[1, 'mike', 'john', 2, 'new', 'list']
     
    aList = [0,1,2,3,4,5,6]
    # size
    print len(aList)
    #7
     
    print aList[2]
    #2
     
    print aList[0:3]
    #[0, 1, 2]
     
    print aList[2:]
    #[2, 3, 4, 5, 6]
     
    print aList[-2]
    #5
     
    #lists are mutable
    aList[0] = 10
    print aList
    #[10, 1, 2, 3, 4, 5, 6]

**5\. Tuples**

Java
Python

No tuples in Java. 
    
    
    aTuple = ()
    aTuple = (5) # cause error
    aTuple = (5,)
     
    print aTuple
    print aTuple[0]
    #5

In Python, tuples are similar with lists, and the difference between them is that tuple is immutable. That means methods that change lists' value can not be used on tuples.

To assign a single element tuple, it has to be: aTuple = (5,). If comma is removed, it will be wrong.

**6\. Sets **

Java
Python
    
    
    //hashset
    HashSet<String> aSet = new HashSet<String>();
    aSet.add("aaaa");
    aSet.add("bbbb");
    aSet.add("cccc");
    aSet.add("dddd");
     
    //iterate over set
    Iterator<String> iterator = aSet.iterator();
    while (iterator.hasNext()) {
    	System.out.print(iterator.next() + " ");
    }
     
    HashSet<String> bSet = new HashSet<String>();
    bSet.add("eeee");
    bSet.add("ffff");
    bSet.add("gggg");
    bSet.add("dddd");
     
    //check if bSet is a subset of aSet
    boolean b = aSet.containsAll(bSet);
     
    //union - transform aSet 
    //into the union of aSet and bSet
    aSet.addAll(bSet);
     
    //intersection - transforms aSet 
    //into the intersection of aSet and bSet
    aSet.retainAll(bSet); 
     
    //difference - transforms aSet 
    //into the (asymmetric) set difference
    // of aSet and bSet. 
    aSet.removeAll(bSet);
    
    
    aSet = set()
    aSet = set("one") # a set containing three letters
    #set(['e', 'o', 'n'])
     
    aSet = set(['one', 'two', 'three'])
    #set(['three', 'two', 'one'])
    #a set containing three words
     
    #iterate over set
    for v in aSet:
        print v
     
    bSet = set(['three','four', 'five'])
     
    #union 
    cSet = aSet | bSet
    #set(['four', 'one', 'five', 'three', 'two'])
     
    #intersection
    dSet = aSet & bSet
     
    #find elements in aSet not bSet
    eSet = aSet.difference(bSet)
     
    #add element
    bSet.add("six")
    #set(['four', 'six', 'five', 'three'])

**7\. Dictionaries **

Dictionaries in Python is like Maps in Java.

Java
Python
    
    
    HashMap<String, String> phoneBook = 
                            new HashMap<String, String>();
    phoneBook.put("Mike", "555-1111");
    phoneBook.put("Lucy", "555-2222");
    phoneBook.put("Jack", "555-3333");
     
    //iterate over HashMap
    Map<String, String> map = new HashMap<String, String>();
    for (Map.Entry<String, String> entry : map.entrySet()) {
        System.out.println("Key = " + entry.getKey() +
          ", Value = " + entry.getValue());
    }
     
    //get key value
    phoneBook.get("Mike");
     
    //get all key
    Set keys = phoneBook.keySet();
     
    //get number of elements
    phoneBook.size();
     
    //delete all elements
    phoneBook.clear();
     
    //delete an element
    phoneBook.remove("Lucy");
    
    
    #create an empty dictionary
    phoneBook = {}
    phoneBook = {"Mike":"555-1111", 
                 "Lucy":"555-2222", 
                 "Jack":"555-3333"}
     
    #iterate over dictionary
    for key in phoneBook:
        print(key, phoneBook[key])
     
    #add an element
    phoneBook["Mary"] = "555-6666"
     
    #delete an element
    del phoneBook["Mike"]
     
    #get number of elements
    count = len(phoneBook)
     
    #can have different types
    phoneBook["Susan"] = (1,2,3,4)
     
    #return all keys
    print phoneBook.keys()
     
    #delete all the elements
    phoneBook.clear()

More about Java Collections:

Category >> [Basics](http://www.programcreek.com/category/java-2/basics/) >> [Python](http://www.programcreek.com/category/programming-languages/python/) >> [Versus](http://www.programcreek.com/category/versus/)

If you want to post syntax highlighted code and let me or someone else review it, please put the code inside <pre><code> and </code></pre> tags.   
For example:
    
    
    <pre><code> 
    String foo = "bar";
    </code></pre>
    

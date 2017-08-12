# How to Create JSON in Python Flask

_Captured: 2016-06-25 at 23:54 from [codehandbook.org](http://codehandbook.org/how-to-create-json-in-python-flask/)_

This post is in reply to a user comment on the [Working with JSON data in Python Flask](http://codehandbook.org/working-with-json-data-in-python-flask/) post where one of the readers asked how to create the following _JSON_ data :
    
    
    {
        "Employees": [{
            "firstName": "Roy",
            "lastName": "Augustine"
        }, {
            "firstName": "Roy",
            "lastName": "Augustine"
        }]
    }
    
    

Start by creating a simple python flask app with a method to return _employee_ JSON data.
    
    
    @app.route("/getEmployeeList")
    def getEmployeeList():
        
        try:
    
           # Code will be here
    
        except Exception ,e:
            print str(e)
    
        return "Employee"
    
    

I'll be importing _json_ and _jsonify _python app.
    
    
    from flask import Flask,jsonify,json
    
    

The basic logic for creating the above _JSON_ data is creating a dictionary and appending it to a list. Once the list is complete we'll convert the list to _JSON_ data. Here is the complete _getEmployeeList_ python method :
    
    
    @app.route("/getEmployeeList")
    def getEmployeeList():
        
        try:
    
            # Initialize a employee list
            employeeList = []
    
            # create a instances for filling up employee list
            for i in range(0,2):
            empDict = {
            'firstName': 'Roy',
            'lastName': 'Augustine'}
                employeeList.append(empDict)
        
            # convert to json data
            jsonStr = json.dumps(employeeList)
    
        except Exception ,e:
            print str(e)
    
        return jsonify(Employees=jsonStr)
    
    

Save the changes and try to run the above code. <http://localhost:5000/getEmployeeList> should return the required JSON data:
    
    
    {
        "Employees": [{
            "firstName": "Roy",
            "lastName": "Augustine"
        }, {
            "firstName": "Roy",
            "lastName": "Augustine"
        }]
    }
    
    

## Wrapping It Up

In this short tutorial, we saw how to create _JSON_ data in Python Flask. I would also recommend reading [working with JSON data in Python Flask](http://codehandbook.org/working-with-json-data-in-python-flask/).

Also read : [Other Python Programming Tutorials on CodeHandbook](http://codehandbook.org/category/python-programming-language/).

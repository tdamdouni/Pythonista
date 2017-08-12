import csv
import os

def write_to_csv(filename, data_dict):
    
    fexists = os.path.exists(filename) # We set a var to see if the file exists 
    
    fieldnames = list(my_data_dict.keys()) # get a list of the keys to use as the header
    with open(filename, 'a') as csvfile:
            #fieldnames = ['Day', 'Month','Year']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # only write the header one time to the file
            if not fexists:
                writer.writeheader()
                
            writer.writerow(data_dict)
            #svfile1.close()  # you dont need this.  Look up Context Managers

if __name__ == '__main__':
    filename = 'my_csv.csv'
    
    # you would collect your data and put it in a dict.
    my_data_dict = dict(
        Day = 1,
        Month = 12,
        Year = 2017,
        Amm = 2.5   
    )
    
    write_to_csv(filename , my_data_dict)
    
    # just print the file to the console, make sure its what we wanted
    with open(filename) as f:
        for line in f:
            print(line, end='') 

import sqlite3
import dataset
from datetime import date

db = dataset.connect('sqlite:///checkbook.my.db')
today = date.today().strftime('%Y-%m-%d')

deposits = db['deposits']
withdrawals = db['withdrawals']
known_expenses = db['knownExpenses']

def get_vals():
    def get_bal(database):
        bal = 0
        for items in database:
            bal += items['amount']
        return(bal)

    deposit_bal = get_bal(deposits)
    withdrawals_bal = get_bal(withdrawals)
    balance = deposit_bal - withdrawals_bal
    return (round(balance,2))

def transaction(table, tName, tAmount):
    table.insert(dict(name= tName, amount=tAmount, date=str(today)))

def get_mandatory(expenses):
    if date.today().day in [15, 25]:
        day_val = date.today().day
    else:
        day_val = int(input('What Payday are you looking for?'))

    mandatory_expenses = expenses.find(date = day_val)
    mandatory_val = 0
    for a in mandatory_expenses:
        mandatory_val += (a['amount'])
    return(mandatory_val)

def main():

    print('${}'.format(get_vals()))
    Name = input('Name: ')
    Amount = input('Amount: $')
    if  Amount[0] == '(':
        transaction(deposits,Name,Amount[1:-1])
    else:
        transaction(withdrawals,Name,Amount)
    if input('continue?') == 'y': main()

option =  input('Selecet an Option: ')

if option  == 'bal':
    print('${}'.format(round(get_vals(),2)))
elif option == 'payday':
    print('mandatory expenses: ${}'.format(get_vals() - get_mandatory(known_expenses)))
else: 
    main()
fin_balance = '$' + str(get_vals())
with open('balance.txt', 'w') as file:
    file.write(fin_balance)

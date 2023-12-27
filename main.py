import sqlite3
import random


bank = sqlite3.connect('bank.db')
sql = bank.cursor()
sql = bank.execute('CREATE TABLE IF NOT EXISTS bank_system'
                   '(clientID INTEGER, clientN TEXT, phon_num INTEGER, '
                   'balance REAL, contribution REAL, con_period INTEGER);')


def period_c(a, b, c):
    percent = a / 100
    period = percent * b
    con = c + period
    return con


def minus(a, b):
    balance = a - b
    return balance


def plus(a, b):
    balance = a + b
    return balance


while True:
    action = input('Enter the command: ')
    if action.lower() == 'register':
        id = random.randrange(1, 999999, 6)
        cname = input('Enter your name: ')
        phon_num = input('Enter your phon num: ')
        balance = 0.00
        contribution = 0.00
        period = 0
        sql.execute('INSERT INTO bank_system(clientID, clientN, phon_num, balance, contribution ,con_period)'
                    f'VALUES ({id},"{cname}",{phon_num},{balance},{contribution},{period})')
        bank.commit()

    elif action.lower() == 'money':
        cname = input('In which account you wanna add: ')
        balance = float(input('Enter the count of money you wanna add: '))
        sql.execute(f'UPDATE bank_system SET balance = {balance} WHERE clientN = "{cname}"')
        bank.commit()
    elif action.lower() == 'cash':
        cname = input('In which account you wanna add: ')
        sql.execute(f'SELECT balance FROM bank_system WHERE clientN = "{cname}"')
        result = sql.fetchone()
        if result is None:
            print(f"Client '{cname}' not found.")
            continue
        balance = result[0]
        cash = float(input('How much money you wanna cash: '))
        if cash > balance:
            print('In your balance not enough money!')
            continue
        c_balance = minus(balance, cash)
        sql.execute(f'UPDATE bank_system SET balance = {c_balance} WHERE clientN = "{cname}"')
        bank.commit()
    elif action.lower() == 'contribute':
        cname = input('In which account you wanna add: ')
        sql.execute(f'SELECT balance, contribution FROM bank_system WHERE clientN = "{cname}"')
        result = sql.fetchone()

        if result is None:
            print(f"Client '{cname}' not found.")
            continue

        balance = result[0]
        contribution = result[1]

        period = int(input('Choose the period which you wanna take, we have period for 12:12%, 24:24%, 36:36% : '))

        if period in [12, 24, 36]:
            sum = float(input('Enter the sum of money you wanna contribute: '))
            if sum > balance:
                print('Your balance not enough!')
            else:
                new_contribution = period_c(sum, period, contribution)
                new_balance = minus(balance, sum)

                # Update the database with the new values
                sql.execute(f'UPDATE bank_system SET balance = {new_balance} WHERE clientN = "{cname}"')
                sql.execute(f'UPDATE bank_system SET contribution = {new_contribution+sum} WHERE clientN = "{cname}"')
                sql.execute(f'UPDATE bank_system SET con_period = {period} WHERE clientN = "{cname}"')

                bank.commit()
        else:
            print('Invalid period choice')
    elif action.lower() == 'balance':
        cname = input('Enter your name: ')
        sql.execute('SELECT balance FROM bank_system WHERE clientN = ?', (cname,))

        result = sql.fetchone()

        if result:
            balance = result[0]
            print(f"Your current balance is: {balance} $")
        else:
            print(f"Client '{cname}' not found.")

    elif action.lower() == 'profile':
        cname = input('Enter your name: ')
        phon_num = input('Enter your phone number: ')
        sql.execute(f'SELECT * FROM bank_system WHERE clientN = "{cname}" AND phon_num = "{phon_num}"')
        result = sql.fetchone()

        if result:
            client_id, full_name, phone_number, balance, contribution, con_period = result
            print(
                f"Client ID: {client_id}\nName: {full_name}\nPhone Number: {phone_number}\nBalance: {balance} $\n"
                f"Contribution: {contribution} $\nContribution Period: {con_period} months")
        else:
            print(f"Client '{cname}' with phone number '{phon_num}' not found.")










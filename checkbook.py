"""
Keith Stateson
Project 1: checkbook
Checkbook is a command line checkbook application that allows users to track their finances.
"""

import csv
import os
import time
import random

# variables
play_game = True

# global variables - global is generally used for static variables that don't change
cols = ['timestamp', 'transaction', 'balance', 'description']


def clear():
    os.system('clear')


def get_checkbook_status(get_choice):
    """
    Determine if the customer has an account; if not, create an account for the customer.
    :return: status of account as accessed or created
    """
    if os.path.exists('checkbook.csv'):
        if get_choice == 1:
            get_status = ''
        else:
            get_status = '\nTransaction complete!\n'
    else:
        with open('checkbook.csv', 'w') as f_gcs:
            transaction = dict(timestamp=time.ctime(), transaction='new account', balance=0,
                               description='opened new checkbook account')
            writer = csv.DictWriter(f_gcs, fieldnames=cols)
            writer.writeheader()
            writer.writerow(transaction)
        get_status = '\nCreating your new galaxy-wide checkbook account!\nWelcome to SuperNova Bank!!!\n'
    return print(get_status)


def get_checkbook_balance():
    """
    Get customer checkbook balance.
    :return: current balance
    """
    current_total = 0
    with open('checkbook.csv', 'r') as f_gcb:
        content = csv.DictReader(f_gcb, fieldnames=cols)  # output is a list [balance, 0]
        lines = [line for line in content][1:]
        for line in lines:
            current_total += float(line['balance'])
    return current_total


def get_valid_input_debit_or_credit(get_deb_cred_choice):
    """
    Prevent invalid input for debits and credits.
    :return: valid input
    """
    if get_deb_cred_choice == 2:
        choice_value = 'debit'
    else:
        choice_value = 'credit'
    while True:
        user_str = input(f'How much is the {choice_value}: ').lower()
        if '.' in user_str:
            user_str = user_str.replace('.', ' ')
            user_str = user_str.split()
            whole_number_str = str(user_str[0])
            fractional_number_str = str(user_str[1])
            if whole_number_str.isdigit() and fractional_number_str.isdigit():
                valid_float_str = whole_number_str + '.' + fractional_number_str
                valid_float = float(valid_float_str)
                break
        elif user_str.isdigit() and user_str != '0':
            valid_float = float(user_str)
            break

        # alternate method using try and except to obtain valid float entry
        # try:
        #     valid_debit_or_credit = float(input(f'How much is the {choice_value}: '))
        #     if valid_debit_or_credit > 0:
        #         break
        # except ValueError:
        #     print("Invalid entry. Please enter a valid number.")

    return valid_float


def add_transaction(get_choice, get_deb_or_cred):
    """
    Add debit or credit transaction to checkbook.
    :return: no value is returned
    """
    with open('checkbook.csv', 'a') as f_trans:
        if get_choice == 3:
            transaction_type = 'credit'
        elif get_choice == 2:
            transaction_type = 'debit'
        user_description = get_user_description()
        transaction = {'timestamp': time.ctime(), 'transaction': transaction_type,
                       'balance': get_deb_or_cred, 'description': user_description}
        writer_transaction = csv.DictWriter(f_trans, fieldnames=cols)
        writer_transaction.writerow(transaction)


def get_user_description():
    """
    This function is called by "add_transaction" function.
    Get user comment for a debit or credit transaction.
    :return: user description of the transaction
    """
    while True:
        description_choice = input("Enter a description for your transaction (up to 30 characters and cannot begin "
                                   "with a number), or press 's' to skip: ").lower()
        if description_choice == 's':
            description_choice = ''
            break
        elif not description_choice.isdigit() and len(description_choice) <= 30:
            break
    return description_choice


def get_transaction_history():
    print("Galaxy Wide Transaction History\n".center(36, ' '))
    with open('checkbook.csv', 'r') as f_history:
        reader = csv.DictReader(f_history)
        next(reader)  # next pull the header and then moves onward to the next row
        lines = [line for line in reader]

        for line in lines:  # get the max length of any tender to expand the output column
            max_length = 0
            biggie = len(line['balance'])
            if biggie > max_length:
                max_length = biggie
            max_length += 3  # accounts for two decimal places and period
        print(f"#    Timestamp                    Type       Balance, USD            Description")
        for index, line in enumerate(lines):
            print(f"{index: <4} {line['timestamp']:<28} {line['transaction']:<10}"
                  f" ${float(line['balance']):>17,.2f} {' ':<4} {line['description']}")
        print('\n')


def get_search(get_search_choice):
    with open('checkbook.csv', 'r') as f_history:
        reader = csv.DictReader(f_history)
        next(reader)
        lines = [line for line in reader]

        if get_search_choice == 5:
            user_search = input("Enter keyword to search descriptions in debit and credit entries: ")
            print('\n')

            for line in lines:
                if user_search in line['description']:
                    print(line)
        else:
            day_of_week = {'1': 'Sun', '2': 'Mon', '3': 'Tue', '4': 'Wed', '5': 'Thu', '6': 'Fri', '7': 'Sat'}
            day_input = input("Enter day of the week to search timestamp in debit and credit entries.\nSunday = 1, Mon = 2, Tue = 3, Wed = 4, Thu = 5, Fri = 6, Sat = 7: ")
            user_search = day_of_week[day_input]
            for line in lines:
                if user_search in line['timestamp']:
                    print(line)
        print('\n')


def get_stats_summary():
    with open('checkbook.csv', 'r') as f_history:
        reader = csv.DictReader(f_history)
        next(reader)
        lines = [line for line in reader]

        max_credit = 0
        for line in lines:
            if float(line['balance']) > max_credit:
                max_credit = float(line['balance'])
        print(f"Maximum withdrawal amount, galaxy wide: ${max_credit:,.2f}")

        min_credit = float('+inf')
        for line in lines:
            if float(line['balance']) < min_credit and float(line['balance']) > 0:
                min_credit = float(line['balance'])
        print(f"Minimum withdrawal amount, galaxy wide: ${min_credit:,.2f}")

        max_debit = 0
        for line in lines:
            if float(line['balance']) < max_debit:
                max_debit = float(line['balance'])
        print(f"Maximum galactic withdrawal: ${max_debit:,.2f}")

        min_debit = float('-inf')
        for line in lines:
            if float(line['balance']) > min_debit and float(line['balance']) < 0:
                min_debit = float(line['balance'])
        print(f"Minimum galactic withdrawal: ${min_debit:,.2f}")

        total_credits = 0
        each_credit = 0
        for line in lines:
            if line['transaction'] == 'credit':
                each_credit = float(line['balance'])
            total_credits += each_credit  # Output of sum is not correct, don't know why
        print(f"Total Milky Way deposits: ${total_credits:,.2f}")

        total_debits = 0
        each_debit = 0
        for line in lines:
            if line['transaction'] == 'debit':
                each_debit = float(line['balance'])
            total_debits += each_debit  # Output of sum is not correct, don't know why
        print(f"Total Milky Way withdrawals: ${total_debits:,.2f}\n")

def get_random_number():
    random_number_int = random.randint(1, 3)
    if random_number_int == 1:
        print("You been scammed - Yo money, MY MONEY! - Ponzi principle!\n")
    elif random_number_int == 2:
        print("SuperNova went nova! Sorry, yo money gone!\n")
    elif random_number_int == 3:
        print("Martian dollars ain't worth dung.\n")

clear()
print("\n~~~ Welcome to SuperNova's Intergalactic Terminal Checkbook! ~~~".center(64, '~'))
print("\x1B[3mWhere money grows so fast it explodes!\x1B[3m".center(72, ' '))
print("Currency is in USD, Universal Star Dollars\n".center(64, ' '))

while play_game:
    print("What would you like to do?\n")
    print("1 - view current balance")
    print("2 - record a debit (withdraw)")
    print("3 - record a credit (deposit)")
    print("4 - view intergalactic transaction history")
    print("5 - search transaction descriptions")
    print("6 - search transaction timestamps (time travel not included)")
    print("7 - summary of checkbook statistics")
    print("8 - quote of the day")
    print("9 - exit\n")

    while True:
        choice_str = input('Enter your choice: ').lower()
        if choice_str.isdigit() and (0 < int(choice_str) < 10):
            choice = int(choice_str)
            break

    if choice == 9:  # end game
        clear()
        print('Thank you using SuperNova, have a starbrite day!')
        play_game = False

    elif choice == 1:  # check balance
        clear()
        get_checkbook_status(get_choice=choice)    # determine if customer has an account
        current_balance = get_checkbook_balance()
        print(f'Your current galactic balance is ${current_balance:,.2f}\n')

    elif choice == 2:  # debit transaction
        clear()
        debit = -1 * get_valid_input_debit_or_credit(get_deb_cred_choice=choice)  # validation of debit
        get_checkbook_status(get_choice=choice)
        add_transaction(get_choice=choice, get_deb_or_cred=debit)  # add debit to checkbook

    elif choice == 3:  # credit transaction
        clear()
        credit = get_valid_input_debit_or_credit(get_deb_cred_choice=choice)  # validation of credit
        get_checkbook_status(get_choice=choice)
        add_transaction(get_choice=choice, get_deb_or_cred=credit)  # add credit to checkbook

    elif choice == 4:  # view transaction history
        clear()
        get_transaction_history()

    elif choice == 5:  # search description history
        clear()
        get_search(get_search_choice=choice)

    elif choice == 6:  # search transaction timestamps
        clear()
        get_search(get_search_choice=choice)

    elif choice == 7:  # view summary of checkbook statistics
        clear()
        get_stats_summary()

    elif choice == 8:
        clear()
        get_random_number()

    else:
        print("$omething smells fi$hy - Yo money is gaw-gaw-gone!!! Sorry, SuperNova went Nova!")

import csv
import datetime
import ipaddress

# erstellt von Paul-Robert Dulca
##########################################################
# Task 1
##########################################################
def find_customers_by_ip(ip_address, date=None):
    # check if date is valid
    if date is not None:
        try:
            check_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            print(f'Invalid date: {date}')
            return []
    else:
        check_date = None

    # check if IP-Address is valid
    try:
        addressIP = ipaddress.ip_address(ip_address)
    except ValueError:
        print(f'Invalid IP address: {ip_address}')
        return []

    # initializing the lists of IDs
    assignmentID = []
    customersID = []
    rangesID = []

    with open('ip-ranges.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            range1 = ipaddress.ip_address(row[1])
            range2 = ipaddress.ip_address(row[2])
            # checking if the ip address is in the range of the current start and end ip
            if range1 <= addressIP <= range2:
                rangesID.append(row[0])
        csvfile.close()

    with open('ip-assignments.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            # depending on the date, the program is checking with both rangeID and date
            if check_date is not None:
                start_date = datetime.datetime.strptime(row[2], '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(row[3], '%Y-%m-%d').date()
                if start_date <= check_date <= end_date and row[1] in rangesID:
                    assignmentID.append(row[0])
            elif row[1] in rangesID and check_date is None:
                assignmentID.append(row[0])
        csvfile.close()

    with open('customer2ipassignment.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        # customerIDs are saved and returned
        for row in reader:
            for id in assignmentID:
                if id in row:
                    customersID.append(row[0])
        csvfile.close()

    return customersID


##########################################################
# Task 2
##########################################################
# makes sure that all companies found are being saved for later, to print them with the coresponding range
customerNameId = []


def find_ip_by_customer(customer, date=None):
    # check the date if it is valid or not
    if date is not None:
        try:
            check_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            print(f'Invalid date: {date}')
            return []
    else:
        check_date = None

    # initializing the lists of IDs
    customerID = []
    assignmentID = []
    rangesID = []
    rangeIP = []
    # check if the users input is the ID or name of the company
    # here it checks the input string for either characters or spaces
    if all((c.isalpha() or c.isspace()) for c in customer):
        with open('customer.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)
            for row in reader:
                if any(customer.lower() in value.lower().strip() for value in row):
                    nameID = row[0]
                    name = row[1]
                    # name and id of the found companies are saved in a global variable
                    customerNameId.append((nameID, name))
                    customerID.append(row[0])
            csvfile.close()
    else:
        # firt the customer is being saved in the global variable
        with open('customer.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            next(reader)
            for row in reader:
                if customer in row:
                    nameID = row[0]
                    name = row[1]
                    customerNameId.append((nameID, name))
        # then the uid is being saved in the customerID list, which is being used for the next step
        customerID.append((customer))

    # from here on the program makes sure that the customer id is being passed on, so that we know,
    # which range belongs where
    with open('customer2ipassignment.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            for id in customerID:
                if id in row:
                    assignmentID.append((row[0], row[1]))
        csvfile.close()

    with open('ip-assignments.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            for id in assignmentID:
                # depending on the date, the program is checking with both rangeID and date
                if check_date is not None:
                    # the dates from the csv are being converted, so that the program can use them
                    start_date = datetime.datetime.strptime(row[2], '%Y-%m-%d').date()
                    end_date = datetime.datetime.strptime(row[3], '%Y-%m-%d').date()
                    if start_date <= check_date <= end_date and id[1] in row:
                        rangesID.append((id[0], row[1]))
                elif id[1] in row and check_date is None:
                    rangesID.append((id[0], row[1]))
        csvfile.close()

    with open('ip-ranges.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            for rangesIP in rangesID:
                if rangesIP[1] in row:
                    range1 = row[1]
                    range2 = row[2]
                    rangeIP.append((rangesIP[0], range1, range2))
        csvfile.close()

    return rangeIP


##########################################################
# Input for the program
##########################################################

print('To close the programm type 0')

while 1:
    # check how the user wants to search
    search = input('\nDo you want to search an Customer(1) or IP range for a customer(2): ')
    # check wether the programm should be closed or not
    if int(search) == 0:
        break
    # check for the input if it is correct
    if search.isdigit():
        # case of the user searches for a customer with a specific ip-address
        if int(search) == 1:
            ip_string = input('Enter an IP-Address: ')
            date_string = input('Enter a date (YYYY-MM-DD): ')

            customer = []
            # checking if date is empty or not
            if date_string == "":
                customer = find_customers_by_ip(ip_string)
            else:
                customer = find_customers_by_ip(ip_string, date_string)
        # case if user searches for n IP range with the name or UID of a customer
        elif int(search) == 2:
            ip_string = input('Enter a customer or customer ID: ')
            date_string = input('Enter a date (YYYY-MM-DD): ')

            customer = []
            # checking if date is empty or not
            if date_string == "":
                customer = find_ip_by_customer(ip_string)
            else:
                customer = find_ip_by_customer(ip_string, date_string)
        else:
            print('Invalid input.')
            continue
    else:
        print('Invalid input.')
        continue

    # checking the search of the function
    if len(customer) > 0:
        # checking wich method was used for the search
        if int(search) == 1:
            print(f'\nCustomers assigned to IP address {ip_string}:')
            with open('customer.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                next(reader)
                for row in reader:
                    for name in customer:
                        if name in row:
                            print(row[1])
        elif int(search) == 2:
            print(f'\nIP address ranges assigned to the customer {ip_string}:')
            # for i in range(len(customer)):
            for n in customer:
                for i in customerNameId:
                    if n[0] == i[0]:
                        print('Customer ID: '+i[0]+'; Name:'+i[1]+'; IP address range: '+n[1]+'-'+n[2]+';')
    else:
        print('No customers found.')

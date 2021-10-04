#!/usr/bin/env python3
# Download the helper library from https://www.twilio.com/docs/python/install
import csv, sys 
from twilio.rest import Client

def send_sms(path):
    MESSAGE_FILE = 'carla_colete.txt'     # File containing text message
    CSV_FILE = 'participants.csv'    # File containing participant numbers
    SMS_LENGTH = 160                 # Max length of one SMS message
    MSG_COST = 0.04                  # Cost per message
    
    # Twilio: Find these values at https://twilio.com/user/account
    account_sid = "AC7673de4db6607faff5ca555001b4c2bc"
    auth_token = "c3c43bf569f66a6a0273a287db28e0df"
    from_num = "3197010252578”    # 'From' number in Twilio
    
    # Now put your SMS in a file called message.txt, and it will be read from there.
    with open(MESSAGE_FILE, 'r') as content_file:
        sms = content_file.read()
    
    # Check we read a message OK
    if len(sms.strip()) == 0:
        print("SMS message not specified- please make a {}' file containing it. \r\nExiting!".format(MESSAGE_FILE))
        sys.exit(1)
    else:
        print("> SMS message to send: \n\n{}".format(sms))
    
    # How many segments is this message going to use?
    segments = int(len(sms.encode('utf-8')) / SMS_LENGTH) +1
    
    # Open the people CSV and get all the numbers out of it
    ml_files = list(filter(lambda c: c.endswith('.csv'), os.listdir(path)))
    numbers = []
    
    for ml in ml_files:
        cf = path + ml
        lines = [line for line in file]
        with tqdm(total=len(lines)) as progress:
            for ndx, phone in csv.reader(lines):
                print(phone)
                try:
                    z = phonenumbers.parse(phone)
                    valid_number = phonenumbers.is_valid_number(z)
                    if valid_number:
                        line_type = phonenumberutil.number_type(z)
                        if line_type == 0:
                            numbers.append(phone)
                        print(line_type)
                except NumberParseException as e:
                    print(str(e))

    # Calculate how much it's going to cost:
    messages = len(numbers)
    cost = MSG_COST * segments * messages
    
    print("> {} messages of {} segments each will be sent, at a cost of ${} ".format(messages, segments, cost))
    
    # Check you really want to send them
    confirm = input("Send these messages? [Y/n] ")
    if confirm[0].lower() == 'y':
        # Set up Twilio client
        client = Client(account_sid, auth_token)
    
        # Send the messages
        for num in numbers:
            # Send the sms text to the number from the CSV file:
            print("Sending to " + num)
            message = client.messages.create(to=num, from_=from_num, body=sms)
    
    print("Exiting!")

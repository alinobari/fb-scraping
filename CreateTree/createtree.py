import requests
import os
from datetime import datetime, timedelta
from time import strptime
import pickle

from lxml import html
from bs4 import BeautifulSoup

class bcolors:
    WHITE = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CYAN = '\033[34m'

class Message(object):
    #name of the user sending the message
    name = ''

    #message content
    message = ''

    #date the message was sent
    year = 0
    month = 0
    day = 0
    hour = 0
    minute = 0

    """__init__() constructs the class object"""
    def __init__(self, name, message, year, month, day, hour, minute):
        self.name = name
        self.message = message
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute

messageList = []

OUTPUT_DIR = ".../collected data/html/Raw/"
OUTPUT_FILE_NAME = "test_fb_pretty_div.html" #MUST FILL IN


def createtree():
    """create the tree structure from the saved html file"""
    html_file = open('../collected data/html/Raw/test_fb.html', 'r').read() #MUST FILL IN

    soup_file = BeautifulSoup(html_file, "lxml")

    #organize the file -> outputs str
    #soup_file_pretty = soup_file.prettify()

    #extract main class
    extract_message_main_class = soup_file.findAll('div', {'class': '__i_'})

    soup_main_div = BeautifulSoup(str(extract_message_main_class), "lxml")

    #User message block
    extract_message_user_class = soup_main_div.findAll('div', {'class': '_1t_p'})

    ###--- ---MESSAGE BLOCK HAS BEEN EXTRACTED--- ---###

    test = extract_message_user_class

    #print the messages
    print_messages(extract_message_user_class)

    #pickle the file to be used by another appliciation
    messages_pickle = open('pickle-messages.obj', 'wb') #MUST FILL IN
    pickle.dump(messageList, messages_pickle)

    return

def date_format_fix(date):
    m_minute = 0
    m_hour = 0
    m_day = 0
    m_month = 0
    m_year = 0

    now = datetime.now()

    weekday = datetime.today().weekday()

    #removes commas
    if ',' in date:
        date = date.replace(',', '')

    date_split = date.split()

    #remove space behind am/pm
    count = 0
    for text in date_split:
        if (text == 'am'):
            date_split[count-1] = date_split[count-1] + date_split[count]
            date_split.pop()
        elif (text == 'pm'):
            date_split[count-1] = date_split[count-1] + date_split[count]
            date_split.pop()
        count += 1

    #if single value
    if (len(date_split) == 1):
        #time fix
        new_time = time_format_change(date_split[0])

        m_minute = new_time[1]
        m_hour = new_time[0]
        m_day = now.day
        m_month = now.month
        m_year = now.year
    
    elif (len(date_split) == 2):
        #day of the week fix
        if (date_split[0] == 'Monday'):
            #day is 0
            Monday = 0
            if (weekday == Monday):
                print(bcolors.FAIL + "ERROR- day of the week")
                days_to_subtract = 1
            else:
                days_to_subtract = ((weekday - Monday)%7)

            new_day = now - timedelta(days=days_to_subtract)
        elif (date_split[0] == 'Tuesday'):
            #day is 1
            Tuesday = 1
            if (weekday == Tuesday):
                print(bcolors.FAIL + "ERROR- day of the week")
                days_to_subtract = 1
            else:
                days_to_subtract = ((weekday - Tuesday)%7)

            new_day = now - timedelta(days=days_to_subtract)
        elif (date_split[0] == 'Wednesday'):
            #day is 2
            Wednesday = 2
            if (weekday == Wednesday):
                print(bcolors.FAIL + "ERROR- day of the week")
                days_to_subtract = 1
            else:
                days_to_subtract = ((weekday - Wednesday)%7)

            new_day = now - timedelta(days=days_to_subtract)            
        elif (date_split[0] == 'Thursday'):
            #day is 3
            Thursday = 3
            if (weekday == Thursday):
                print(bcolors.FAIL + "ERROR- day of the week")
                days_to_subtract = 1
            else:
                days_to_subtract = ((weekday - Thursday)%7)

            new_day = now - timedelta(days=days_to_subtract)           
        elif (date_split[0] == 'Friday'):
            #day is 4
            Friday = 4
            if (weekday == Friday):
                print(bcolors.FAIL + "ERROR- day of the week")
                days_to_subtract = 1
            else:
                days_to_subtract = ((weekday - Friday)%7)

            new_day = now - timedelta(days=days_to_subtract)
        elif (date_split[0] == 'Saturday'):
            #day is 5
            Saturday = 5
            if (weekday == Saturday):
                print(bcolors.FAIL + "ERROR- day of the week")
                days_to_subtract = 1
            else:
                days_to_subtract = ((weekday - Saturday)%7)

            new_day = now - timedelta(days=days_to_subtract)
        elif (date_split[0] == 'Sunday'):
            #day is 6
            Sunday = 6
            if (weekday == Sunday):
                print(bcolors.FAIL + "ERROR- day of the week")
                days_to_subtract = 1
            else:
                days_to_subtract = ((weekday - Sunday)%7)

            new_day = now - timedelta(days=days_to_subtract)

        new_time = time_format_change(date_split[1])
        #take out old time
        #date_split.pop()
        #inset new hour
        #date_split.append(new_time[0])
        #insert new minute
        #date_split.append(new_time[1])

        m_minute = new_time[1]
        m_hour = new_time[0]
        m_day = new_day.day
        m_month = new_day.month
        m_year = new_day.year


    elif (len(date_split) == 3):
        #day month time
        #if beginning character starts with a number
        if(date_split[0].isdigit()):
            m_month = strptime(date_split[1], '%B').tm_mon
            m_day = date_split[0]
        else:
            if 'st' in date_split[1]:
                date_split[1] = date_split[1].strip('st')
            if 'rd' in date_split[1]:
                date_split[1] = date_split[1].strip('rd')
            if 'nd' in date_split[1]:
                date_split[1] = date_split[1].strip('nd')
            if 'th' in date_split[1]:
                date_split[1] = date_split[1].strip('th')

            m_month = strptime(date_split[0], '%B').tm_mon
            m_day = date_split[1]

        new_time = time_format_change(date_split[2])
        #take out old time
        #date_split.pop()
        #inset new hour
        #date_split.append(new_time[0])
        #insert new minute
        #date_split.append(new_time[1])

        m_minute = new_time[1]
        m_hour = new_time[0]
        m_year = now.year
            

    elif (len(date_split) == 4):
        #day month year time
        if(date_split[0].isdigit()):
            m_month = strptime(date_split[1], '%B').tm_mon
            m_day = date_split[0]
        else:
            if 'st' in date_split[1]:
                date_split[1] = date_split[1].strip('st')
            if 'rd' in date_split[1]:
                date_split[1] = date_split[1].strip('rd')
            if 'nd' in date_split[1]:
                date_split[1] = date_split[1].strip('nd')
            if 'th' in date_split[1]:
                date_split[1] = date_split[1].strip('th')

            m_month = strptime(date_split[0], '%B').tm_mon
            m_day = date_split[1]

        new_time = time_format_change(date_split[3])

        m_minute = new_time[1]
        m_hour = new_time[0]
        m_year = date_split[2]

    #print("Input: " + date + '\n')

    #print("Minute: " + str(m_minute))
    #print("Hour: " + str(m_hour))
    #print("Day: " + str(m_day))
    #print("Month: " + str(m_month))
    #print("Year: " + str(m_year) + '\n\n')

    fixed_date = [m_year, m_month, m_day, m_hour, m_minute]

    return fixed_date

def time_format_change(time):
    """ 12 hour to 24 hour format"""
    if 'am' in time:
        date_strip = time.strip("am")
        date_split_two = date_strip.split(':')
        return date_split_two
        #only hour, minute
    elif 'pm' in time:
        date_strip = time.strip("pm")
        date_split_two = date_strip.split(':')
        date_split_two[0] = str(12 + int(date_split_two[0]))
        return date_split_two
        #only hour, minute
    else:
        date_split_two = time.split(':')
        return date_split_two
        #only hour, minute

def print_messages(extract_message_user_class):
    
    #counter for messages
    sent_message_count = 1

    for div_count in range (0, len(extract_message_user_class)):
        
        message_block = BeautifulSoup(str(extract_message_user_class[div_count]), 'lxml')

        #get name of message sender
        message_block_name = message_block.select('h5._ih3')[0].text.strip()

        #length of message_block.select('span._58nk') will determine how many messages have been sent 
        number_of_messages = len(message_block.select('span._58nk'))

        #if there is only one message
        if (number_of_messages == 1):
            #message counter
            #print(bcolors.FAIL + str(sent_message_count))
            sent_message_count += 1
        
            message_block_message = message_block.select('span._58nk')[0].text.strip()
            #move two divs up from the message and select the date
            message_block_date = message_block.find_all('span', {'class': '_58nk'})[0].parent.parent.get('data-tooltip-content')
            message_block_date = date_format_fix(message_block_date)

            #print (bcolors.WHITE + "Name: " + message_block_name)
            #print (bcolors.WARNING + "Message: " + str(message_block_message))
            #print (bcolors.CYAN + "Date: " + str(message_block_date) + '\n')

            messageList.append(Message(message_block_name, message_block_message, message_block_date[0], message_block_date[1], 
                message_block_date[2], message_block_date[3], message_block_date[4]))
        
        #user sent more than one message        
        else:
            for message_count in range (0, number_of_messages):
                #message counter
                #print(bcolors.FAIL + str(sent_message_count))
                sent_message_count += 1

                #move two divs up from the message and select the date
                message_block_date = message_block.find_all('span', {'class': '_58nk'})[0].parent.parent.get('data-tooltip-content')
                message_block_date = date_format_fix(message_block_date)
                message_block_message = message_block.select('span._58nk')[message_count].text.strip()

                #print (bcolors.WHITE + "Name: " + message_block_name)
                #print (bcolors.WARNING + "Message: " + message_block_message)
                #print (bcolors.CYAN + "Date: " + str(message_block_date) + '\n')
            
                messageList.append(Message(message_block_name, message_block_message, message_block_date[0], message_block_date[1], 
                    message_block_date[2], message_block_date[3], message_block_date[4]))
    
    return

def pretty(input_to_pretty):
    """prettify an input"""

    input_to_pretty_bf = BeautifulSoup(str(input_to_pretty), 'lxml')

    soup_file_pretty = input_to_pretty_bf.prettify()

    #output file to textfile
    output = open(os.path.join(OUTPUT_DIR, 'pretty_div_individual.html'), 'w')
    output.write(soup_file_pretty)
    output.close()

    return

def pretty_file():
    """prettify a file"""
    input_file = open('./test_fb_pretty_div.html', 'r').read() #MUST FILL IN

    soup_file = BeautifulSoup(input_file, "lxml")
    
    #organize the file -> outputs str
    soup_file_pretty = soup_file.prettify()

    #output file to textfile
    output = open(os.path.join(OUTPUT_DIR, 'pretty_div.html'), 'w')
    output.write(soup_file_pretty)
    output.close()

    return

def date_conversion_test():
    date0 = '17:50'
    date1 = '11:30 am'
    date1_1 = '2:30pm'
    date2 = 'Thursday 17:12'
    date2_1 = 'Saturday 17:12'
    date3 = 'Thursday 1:28pm'
    date4 = 'August 15, 2015 9:53 pm'
    date5 = '6 January 14:00'
    date5_1 = 'January 31st, 1:41 pm'
    date6 = '31 December 2017 16:02'

    date_format_fix(date0)
    date_format_fix(date1)
    date_format_fix(date1_1)
    date_format_fix(date2)
    date_format_fix(date2_1)
    date_format_fix(date3)
    date_format_fix(date4)
    date_format_fix(date5)
    date_format_fix(date5_1)
    date_format_fix(date6)

#main
createtree()
#pretty()
exit()
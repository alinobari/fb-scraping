import pickle
import os
import sys
from datetime import datetime,timedelta
import calendar
#for work counting
import collections
import re

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

dir_path = os.path.dirname(os.path.realpath(__file__))
INPUT_FILE_NAME = dir_path + '/../collected data/message-class/pickle-messages-Alyssa.obj'

OUTPUT_FILE_DIR = './data/'

def input_class():
    """function to input the created object file"""
    global messageList

    pickled_messages = open(INPUT_FILE_NAME, 'rb')
    messageList = pickle.load(pickled_messages)

    #print(messageList[0].name)

    return

def message_word_count():
    """number of words sent by each user"""

    name_1 = ''
    name_2 = ''

    count_1 = 0
    count_2 = 0

    name_1 = messageList[0].name

    flag = 0

    for count in range (0, len(messageList)):
        if (name_1 == messageList[count].name):
            message = messageList[count].message
            count_1 = count_1 + len(message.split())
        else:
            if (flag == 0):
                name_2 = messageList[count].name
                flag = 1
            message = messageList[count].message
            count_2 = count_2 + len(message.split())

    print("Words sent")
    print(name_1 + "'s word count: " + str(count_1))
    print(name_2 + "'s word count: " + str(count_2) + '\n')

    create_csv_file('message_word_count', 'name', 'count', [name_1, name_2], [str(count_1), str(count_2)])
            
    return

def character_count():
    """number of characters sent by each user"""

    name_1 = ''
    name_2 = ''

    count_1 = 0
    count_2 = 0

    name_1 = messageList[0].name

    flag = 0

    for count in range (0, len(messageList)):
        if (name_1 == messageList[count].name):
            count_1 = count_1 + len(messageList[count].message)
        else:
            if (flag == 0):
                name_2 = messageList[count].name
                flag = 1
            count_2 = count_2 + len(messageList[count].message)

    print("Characters sent")
    print(name_1 + "'s character count: " + str(count_1))
    print(name_2 + "'s character count: " + str(count_2) + '\n')
            
    return   

def message_sent_count():
    """number of messages sent"""

    name_1 = ''
    name_2 = ''

    count_1 = 0
    count_2 = 0

    name_1 = messageList[0].name

    flag = 0

    for count in range (0, len(messageList)):
        if (name_1 == messageList[count].name):
            count_1 += 1
        else:
            if (flag == 0):
                name_2 = messageList[count].name
                flag = 1
            count_2 += 1

    print("Messages sent")
    print(name_1 + "'s messages sent: " + str(count_1))
    print(name_2 + "'s messages sent: " + str(count_2) + '\n')

    create_csv_file('message_sent_count', 'name', 'count', [name_1, name_2], [str(count_1), str(count_2)])

def monthly_message():
    """number of messages sent every month"""

    #array to hold 
    message_count_array = []
    #storing the date messages were sent
    date_array = []

    #value to hold message amount per month
    message_count = 0

    #set the current month
    current_date = datetime(int(messageList[0].year), int(messageList[0].month), 1)

    counter = 0

    for count in range(0, len(messageList)):

        #check if month has changed
        if (current_date.month == messageList[count].month):
            counter +=1
            message_count += 1
        else:
            message_count_array.append(message_count)
            date = str(current_date.year) + '/' + str(current_date.month)
            date_array.append(date)

            #check if the next month has any messages
            next_month = current_date.month + 1
            while(True):
                if(next_month == 13):
                    next_month = 1
                    #increment the year
                    current_date = datetime((current_date.year+1), current_date.month, 1)

                if(next_month != messageList[count].month):
                    message_count_array.append(0)
                    date = str(current_date.year) + '/' + str(current_date.month)
                    date_array.append(date)
                else:
                    #the new month conatains a message
                    current_date = datetime(current_date.year, int(messageList[count].month), 1)  
                    break

                next_month += 1

            #reset the amount of messages for the next month
            counter += 1
            message_count = 1
    
    message_count_array.append(message_count)
    date = str(current_date.year) + '/' + str(current_date.month)
    date_array.append(date)

    #print(message_count_array)
    #print(date_array)
    #print(len(messageList))

    create_csv_file("month", "date", "messagecount", date_array, message_count_array)

    return

def weekly_message():
    """number of messages sent every week"""
    """week starts on the first day user sends a message"""

    #array to hold 
    message_count_array = []
    #storing the date messages were sent
    date_array = []

    #value to hold message amount per month
    message_count = 0

    #set the current day
    current_date = datetime(int(messageList[0].year), int(messageList[0].month), int(messageList[0].day))

    for count in range(0, len(messageList)):
        
        #check if the date is less than a week in advance
        if(datetime(int(messageList[count].year), int(messageList[count].month), int(messageList[count].day)) < 
            (current_date + timedelta(days=7))):
            #less than a week
            message_count += 1
        else:
            #append the message count to the array
            message_count_array.append(message_count)

            #record the date that the message is appended at
            date = str(current_date.year) + '/' + str(current_date.month) + '/' + str(current_date.day)
            date_array.append(date)

            #go to the next week
            current_date = current_date + timedelta(days=7)

            #count up from current weeks to see weeks in between
            while(True):
                #value to itterate the weeks
                days = 7
    
                if(datetime(int(messageList[count].year), int(messageList[count].month), int(messageList[count].day)) < 
                    (current_date + timedelta(days=7+days))):
                    #the next message is within the next week
                    break
                else:
                    #the next message is not within the next coming weeks
                    current_date = current_date + timedelta(days=7)
                    message_count_array.append(0)

                    date = str(current_date.year) + '/' + str(current_date.month) + '/' + str(current_date.day)
                    date_array.append(date)

            #reset the amount of messages for the next month
            message_count = 1

    message_count_array.append(message_count)
    date = str(current_date.year) + '/' + str(current_date.month) + '/' + str(current_date.day)
    date_array.append(date)  

    #print(message_count_array)
    #print(date_array)
    #print(len(messageList))

    create_csv_file("week", "date", "messagecount", date_array, message_count_array)

    return

def first_last_date():
    """first and last day messages were sent and by what user"""

    name_first = ''
    name_last = ''

    date_first = ''
    date_last = ''

    length = len(messageList) - 1

    name_first = messageList[0].name
    date_first = str(messageList[0].year) + '/' + str(messageList[0].month) + '/' + str(messageList[0].day)

    name_last = messageList[length].name
    date_last = str(messageList[length].year) + '/' + str(messageList[length].month) + '/' + str(messageList[length].day)

    print("Messages sent first and last date")
    print(name_first + "'s messages sent: " + str(date_first))
    print(name_last + "'s messages sent: " + str(date_last) + '\n')

    create_csv_file('message_sent_first_last_date', 'name', 'date', [name_first, name_last], [str(date_first), str(date_last)])

def create_csv_file(func_type, col_one_name, col_two_name, col_one_array, col_two_array):
    """function for creating the csv file"""

    #write the data in csv file
    file_name = OUTPUT_FILE_DIR + func_type + '_csvfile.csv'

    with open (file_name, 'w') as file:
        file.write(col_one_name + "," + col_two_name)

        for count in range(0, len(col_one_array)):
            file.write('\n' + str(col_one_array[count]) + "," + str(col_two_array[count]))

    return

def longest_word_sent():
    """find longest word written by a user"""
        
    name_1 = ''
    name_2 = ''

    word_1 = ''
    word_2 = ''

    name_1 = messageList[0].name

    #flag to only set name_2 once
    flag = 0

    for count in range (0, len(messageList)):
        if (name_1 == messageList[count].name):
            messages = messageList[count].message.split()
            longest_word = max(messages, key=len)

            #check to see if new word is larger
            if(len(word_1) < len(longest_word)):
                #print (bcolors.FAIL + "word1:" + bcolors.WHITE + word_1 + bcolors.FAIL + " ---- longer_word:" + bcolors.WHITE + longest_word)
                word_1 = longest_word
            else:
                pass
        else:
            if (flag == 0):
                name_2 = messageList[count].name
                flag = 1
            messages = messageList[count].message.split()
            longest_word = max(messages, key=len)

            #check to see if new word is larger
            if(len(word_2) < len(longest_word)):
                word_2 = longest_word
            else:
                pass


    print("\nLongest word sent")
    #print(name_1 + "'s longest word: " + word_1)
    #print(name_2 + "'s longest word: " + word_2 + '\n')

    create_csv_file('longest_word_sent', 'name', 'word', [name_1, name_2], [word_1, word_2])
            
    return

def average_word_length():
    """find the average word length used by a user"""
        
    name_1 = ''
    name_2 = ''

    sum_1 = 0
    sum_2 = 0

    name_1 = messageList[0].name

    #flag to only set name_2 once
    flag = 0

    for count in range (0, len(messageList)):
        if (name_1 == messageList[count].name):
            message = messageList[count].message.split()

            average = sum(len(word) for word in message) / len(message)

            sum_1 = sum_1 + average

        else:
            if (flag == 0):
                name_2 = messageList[count].name
                flag = 1
            message = messageList[count].message.split()

            average = sum(len(word) for word in message) / len(message)

            sum_2 = sum_2 + average

    sum_1 = sum_1 / len(messageList)
    sum_2 = sum_2 / len(messageList)

    print("\nAverage word length")
    print(name_1 + "'s average word length: " + str(sum_1))
    print(name_2 + "'s average word length: " + str(sum_2) + '\n')

    create_csv_file('average_word_length', 'name', 'length', [name_1, name_2], [str(sum_1), str(sum_2)])
            
    return

def hourly_messages():
    """show during what time of day users sent messages"""

    name_1 = ''
    name_2 = ''

    #create an array for each user
    array_1 = [0]*24
    array_2 = [0]*24

    name_1 = messageList[0].name

    #flag to only set name_2 once
    flag = 0  

    for count in range (0, len(messageList)):
        if (name_1 == messageList[count].name):
            array_1[int(messageList[count].hour)-1] += 1

        else:
            if (flag == 0):
                name_2 = messageList[count].name
                flag = 1          

            array_2[int(messageList[count].hour)-1] += 1

    print("\nHourly messages")
    #print(name_1 + "'s hourly messages:")
    #print(array_1)
    #print(name_2 + "'s hourly messages:")
    #print(array_2)
    #print("")

    array_hour = []
    for i in range(24): array_hour.append(i)

    create_csv_file('hourly_messages_user1', 'hour', 'count', array_hour, array_1)            
    create_csv_file('hourly_messages_user2', 'hour', 'count', array_hour, array_2) 

def word_usage():
    """get the most common words used by a user"""

    #most_common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'i\'m', 'im' \
    #                    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', \
    #                    'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', \
    #                    'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', \
    #                    'come', 'its', 'it\'s', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', \
    #                    'new', 'want', 'because', 'any', 'these', 'give', 'most', 'us', \
    #                    'is', 'this', 'did', 'have', 'was', 'got', 'thats', 'that\'s', 'are', 'you\'re']

    name_1 = ''
    name_2 = ''

    #arrays used to hold in the words
    array_1 = []
    array_2 = []

    name_1 = messageList[0].name

    #flag to only set name_2 once
    flag = 0 

    for count in range (0, len(messageList)):
        if (name_1 == messageList[count].name):

            message = messageList[count].message
            #remove numbers and special characters
            message = re.sub('[^ a-zA-Z]', '', message)
            message = message.lower().split()

            #for word in most_common_words:
            #   message = [string for string in message if string != word] 

            array_1 = array_1 + message

        else:
            if (flag == 0):
                name_2 = messageList[count].name
                flag = 1
            message = messageList[count].message
            #remove numbers and special characters
            message = re.sub('[^ a-zA-Z]', '', message)
            message = message.lower().split()

            #for word in most_common_words:
            #   message = [string for string in message if string != word] 

            array_2 = array_2 + message

    words_1 = collections.Counter(array_1)
    common_1 = words_1.most_common(10)
    least_common_1 = words_1.most_common()


    words_2 = collections.Counter(array_2)
    common_2 = words_2.most_common(10)
    least_common_2 = words_2.most_common()

    print("\nTop 10 most common words")
    print(name_1 + "'s 10 most common words:")
    #print(common_1)
    for percent in common_1: print('(' + percent[0] + ', ' + str(percent[1]) + ', ' + bcolors.FAIL + str( round((int(percent[1])/int(len(array_1)))*100,3) ) + '%' + bcolors.WHITE + '), ', end='')
    print("\nLeast 10 most common words:")
    for val in range(1,11): print('(' + least_common_1[len(least_common_1)-val][0] + ', ' + str(least_common_1[len(least_common_1)-val][1]) + ', ' + bcolors.FAIL + \
        str( round((int(least_common_1[len(least_common_1)-val][1])/int(len(array_1)))*100,3) ) + '%' + bcolors.WHITE + '), ', end='')
    print('\n')

    print(name_2 + "'s 10 most common words:")
    for percent in common_2: print('(' + percent[0] + ', ' + str(percent[1]) + ', ' + bcolors.FAIL + str( round((int(percent[1])/int(len(array_2)))*100,3) ) + '%' + bcolors.WHITE + '), ', end='')
    print("\nLeast 10 most common words:")
    for val in range(1,11): print('(' + least_common_2[len(least_common_2)-val][0] + ', ' + str(least_common_2[len(least_common_2)-val][1]) + ', ' + bcolors.FAIL + \
        str( round((int(least_common_2[len(least_common_2)-val][1])/int(len(array_2)))*100,3) ) + '%' + bcolors.WHITE + '), ', end='')
    print('\n')

    #create_csv_file('hourly_messages_user1', 'hour', 'count', array_hour, array_1)            
    #create_csv_file('hourly_messages_user2', 'hour', 'count', array_hour, array_2) 

#main
input_class()

#first_last_date() -> graphed
#message_word_count()
#character_count()
#message_sent_count() -> graphed

#monthly_message() -> graphed
#weekly_message() -> graphed

#longest_word_sent()
#average_word_length()
#hourly_messages()
word_usage()

#TODO

#word_usage_circle_chart()
    #|-> Most common word

#Synopsis

exit()
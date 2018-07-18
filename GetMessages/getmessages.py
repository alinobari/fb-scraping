#remove the print parens error
from __future__ import print_function
import sys
import json
import time
import selenium
import requests
import warnings
import getpass
import traceback

import re
import os
import operator
from datetime import datetime
from collections import Counter
from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from splinter import Browser
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
    from urllib import request, parse
from selenium.webdriver.chrome.options import Options

#not used on mac
from pyvirtualdisplay import Display

#for timer
from timeit import default_timer as timer

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

BASE_URL = "https://facebook.com"
BASE_URL_BASIC = "https://mbasic.facebook.com"
LOGIN_URL = "https://login.facebook.com/login.php?login_attempt=1"
BASE_MESSAGE_URL = BASE_URL + "/messages/"
BASE_MESSAGE_URL_BASIC = BASE_URL_BASIC + "/messages/"
LOGIN_URL = "https://www.facebook.com/login.php?login_attempt=1"

URL_TO_GET_USER = "" #MUST FILL IN
URL_TO_GET = "https://www.messenger.com/t/" + URL_TO_GET_USER

#screenshot file
OUTPUT_SCREENSHOT_NAME = "" #MUST FILL IN

#Output file name
OUTPUT_FILE_NAME = '' #MUST FILL IN 

#create display
display = Display(visible=0, size=(1280, 1380))
display.start()

# Create firefox browser instance
BROWSER = webdriver.Firefox(executable_path='../binaries/geckodriver')

#chrome used on mac
#options = Options()
#options.add_argument('headless')
#options.add_argument('window-size=1280x1380')
#BROWSER = webdriver.Chrome(chrome_options=options)
BROWSER.implicitly_wait(10)

#location to save the html file 
OUTPUT_DIR = "./"

def login_with_messenger_scroll():
    """using the method of scrolling to get to the top"""

    #get the conversation thread defined by the user
    BROWSER.get(URL_TO_GET)

    time.sleep(1)

    USERNAME_INPUT = BROWSER.find_element_by_name('email')
    PASSWORD_INPUT = BROWSER.find_element_by_name('pass')

    USERNAME = input("Username: ")
    PASSWORD = getpass.getpass('Password: ')
    
    USERNAME_INPUT.send_keys(USERNAME)
    PASSWORD_INPUT.send_keys(PASSWORD)

    ENTER = BROWSER.find_element_by_name("login")
    ENTER.click()

    print(bcolors.OKBLUE + "url: " + BROWSER.current_url)
    send_message_to_slack(bcolors.OKBLUE + "url: " + BROWSER.current_url)

    #get class to scroll
    CLASS_ELEMENT = BROWSER.find_elements_by_class_name('uiScrollableAreaWrap')

    #messages are on the last div, so must select last position
    CLASS_ELEMENT_SIZE = len(CLASS_ELEMENT) - 1

    MESSAGE_CLASS = BROWSER.find_element_by_class_name("__i_")

    print(MESSAGE_CLASS.get_attribute("scrollHeight"))

    #create text file
    output = open(os.path.join(OUTPUT_DIR, OUTPUT_FILE_NAME), 'w')
    output.close()

    new_height = 0

    old_height = 0

    count = 0

    break_count = 0

    scroll = 0

    start_timer = timer()

    PAGE_SOURCE = None

    while(True):    

        #scroll the message element
        try:
            if (scroll == 0):
                """scroll to the top"""
                BROWSER.execute_script('arguments[0].scrollTop = 0', CLASS_ELEMENT[CLASS_ELEMENT_SIZE])
                scroll = 1              

            if(new_height < int(MESSAGE_CLASS.get_attribute("scrollHeight"))):
                """extract data after having scrolled to the top"""
                
                #find lap time
                LAP = timer() - start_timer

                #compare heights to see if messages have started from the bottom
                new_height = int(MESSAGE_CLASS.get_attribute("scrollHeight"))
                if(old_height >= new_height):
                    print(bcolors.FAIL + 'Size is smaller/equal: ' + 'New Height: ' + str(new_height) + ' Old Height: ' +  str(old_height))
                    break

                print(bcolors.OKGREEN + "  Size of OLD height: " + str(old_height)) 
                print(bcolors.OKGREEN + "  Size of NEW height: " + str(new_height))
                time.sleep(1)
                SOURCE_PAGE_SIZE = str(len(BROWSER.page_source))
                print(bcolors.CYAN + "   Size of source page: " + SOURCE_PAGE_SIZE)
                send_message_to_slack("   Size of source page: " + SOURCE_PAGE_SIZE)
                
                #output the data
                PAGE_SOURCE = BROWSER.page_source

                #print file size
                print(bcolors.OKGREEN + "   Size of variable: " + str(len(PAGE_SOURCE)))

                #print the lap
                print(bcolors.WARNING + str(LAP) + " " + MESSAGE_CLASS.get_attribute("scrollHeight"))
                send_message_to_slack(str(LAP) + " " + MESSAGE_CLASS.get_attribute("scrollHeight"))

                #update height
                old_height = new_height 

                #set flags
                scroll = 0 
                count = 0
            else:
                #if new height is less set the counter
                count += 1

            if(count == 400):
                print(bcolors.FAIL + "Hit counter time")
                send_message_to_slack("Hit the counter time")
                break
            
            break_count = 0
        
        except Exception:
            print(bcolors.FAIL + "While Loop Exception")
            traceback.print_exc()
            send_message_to_slack("While Loop Exception")
            break_count += 1
            if(break_count == 3):
                break
            time.sleep(2)
            pass 

    end_timer = timer()
    time_elapsed = end_timer - start_timer

    #output the data to a file
    output = open(os.path.join(OUTPUT_DIR, OUTPUT_FILE_NAME), 'w')
    output.write(PAGE_SOURCE)
    output.close()

    #get screenshot from the conversation
    BROWSER.get_screenshot_as_file("./" + OUTPUT_SCREENSHOT_NAME)

    print("Time elapsed: " + str(time_elapsed))
    send_message_to_slack("Time elapsed: " + str(time_elapsed))

    print(bcolors.WHITE + "End")
    send_message_to_slack("End")

    BROWSER.quit()
    
    #not used on mac
    display.stop()

    return

def login_with_messenger_search():
    """using the method of searching to get to the top"""

    #get the conversation thread defined by the user
    BROWSER.get(URL_TO_GET) #MUST FILL IN

    time.sleep(1)

    USERNAME_INPUT = BROWSER.find_element_by_name('email')
    PASSWORD_INPUT = BROWSER.find_element_by_name('pass')

    USERNAME = input("Username: ")
    PASSWORD = getpass.getpass('Password: ')
    
    USERNAME_INPUT.send_keys(USERNAME)
    PASSWORD_INPUT.send_keys(PASSWORD)

    ENTER = BROWSER.find_element_by_name("login")
    ENTER.click()
    
    print("url: " + BROWSER.current_url)

    lastheight = BROWSER.execute_script("return document.body.scrollHeight")
    print("Height: " + str(lastheight))

    #click search button
    SEARCH_PANEL = BROWSER.find_elements_by_class_name('_3szn')
    SEARCH_PANEL[0].click()

    #wait for search button to appear
    time.sleep(1)

    #enter search message
    SEARCH_FIELD = BROWSER.find_elements_by_class_name('_58al')    
    SEARCH_FIELD[1].send_keys('This is a test message')

    #hit search
    SEARCH_BUTTON = BROWSER.find_element_by_class_name('__h6')
    SEARCH_BUTTON.click()

    #message view size
    MESSAGE_CLASS = BROWSER.find_element_by_class_name("__i_")

    print(MESSAGE_CLASS.get_attribute("scrollHeight"))

    start_timer = timer()

    time.sleep(1)

    #top bar with users name
    TOP_BAR = BROWSER.find_elements_by_class_name('_llj')

    #load more button
    LOAD_MORE = BROWSER.find_elements_by_class_name('_41jf')

    time.sleep(2)
    while(True):
        try:
            LOAD_MORE[0].click()
            time.sleep(1)
            BROWSER.execute_script('arguments[0].scrollIntoView();', TOP_BAR[0])
            time.sleep(1)
        except:
            print("out")
            break

    end_timer = timer()
    time_elapsed = end_timer - start_timer

    print("time elapsed: " + str(time_elapsed))

    #OUTPUT = open(os.path.join(OUTPUT_DIR, "test_fb_" + '.html'), 'w')
    #OUTPUT.write(BROWSER.page_source)
    #OUTPUT.close()

    BROWSER.quit()

    return

def send_message_to_slack(text):
    """function to send messages to slack"""
    import json
 
    post = {"text": "{0}".format(text)}
 
    try:
        json_data = json.dumps(post)
        req = request.Request("", #MUST FILL IN
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'}) 
        resp = request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))

#call to main
login_with_messenger_scroll()
exit()

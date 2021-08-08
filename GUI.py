from StonkRedditAPI import StonkRedditAPI
from news import newsScraper
from DataTracker import Manager
from collections import Counter
import PySimpleGUI as sg

from datetime import datetime, timedelta
import time

root = 'TrackedInfo'


def addSubTicks(headNum, *counters):
    final = Counter()
    for i in counters:
        final += i.org_freq
    return final.most_common(headNum)


def runSingle():
    print("Running...")

    #Reddit Scrapers
    AMC = StonkRedditAPI('r/amcstock', 'new', 'all', 100, 3)
    WSBN = StonkRedditAPI('r/Wallstreetbetsnew', 'new', 'all', 100, 3)
    WSBE = StonkRedditAPI('r/WallStreetbetsELITE', 'new', 'all', 100, 3)

    #Article Scraper
    yf = newsScraper('https://finance.yahoo.com/', 'news', 10, "yahoo", True)
    cnbc = newsScraper('https://www.cnbc.com/economy/', '2021', 10, 'cnbc', True)

    manager = Manager(root)
    sup_list = [AMC.final, WSBN.final,WSBE.final, yf.word_count, cnbc.word_count]
    manager.storeDataSet(sup_list)

    final_counters = addSubTicks(10, AMC, WSBN, WSBE)
    print('\n\n\n\nFinal:',final_counters)
    return final_counters


def runInBack():
    hour = input("Enter hours to be ran : ")
    frequency = input("Enter frequency for each run in minutes : ")
    target_time = datetime.now() + timedelta(hours=int(hour))

    print("\nStarting Process\n")

    while int(hour) >0:
        cur = datetime.now()
        time_delta = target_time - cur

        print("Instance : " + cur.strftime("%H:%M:%S"))

        runSingle()

        print("Completed Instance")
        print("Waiting...")

        time.sleep(int(frequency)*60)




'''
def look():
    simp = input("Enter symbol : ")
    simp = simp.upper()

    manager = Manager(root)

    printMenu()



def changeSettings():
    print("Settings")


#commands in dict for ease
commands = {
    'a':runSingle,
    'b':runInBack,
    'c':look,
    'd':changeSettings
}
def processCMD(inp):
    commands[inp]()


def printMenu():

    #whitelist all the command keys
    accepted = []
    for keys in commands:
        accepted.append(keys)

    print("a. Run single instance")
    print("b. Run instances in background")
    print("c. Look at data")
    print("d. Settings")
    print("e. Quit ")

    inp = input("Enter choice \n")
    if inp in accepted:
        processCMD(inp)
    else:
        print("Input not accepted\n\n\n\n\n\n\n\n")
        printMenu()'''


def GUI():

    layout = [  [sg.Text('StonkBot')],
                [sg.Output(size=(120,15))],
                [sg.Button('Run Once'), sg.Button('Exit')] ]

    window = sg.Window('StonkBot Output', layout)

    while True:             # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            window.Close()
            break

        elif event == 'Run Once':
            runSingle()

        elif event == 'Run In Back':
            runInBack()

GUI()



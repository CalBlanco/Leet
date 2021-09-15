from StonkRedditAPI import StonkRedditAPI
from news import newsScraper
from DataTracker import Manager



from datetime import datetime, timedelta
import time



root = '20210621_TripCollection'



def runSingle():
    print("Running...")

    #Reddit Scrapers
    WSB = StonkRedditAPI('r/wallstreetbets', 'new', 'all', 100)
    WSBN = StonkRedditAPI('r/Wallstreetbetsnew', 'new', 'all', 100)
    WSBE = StonkRedditAPI('r/WallStreetbetsELITE', 'new', 'all', 100)

    #Article Scraper
    yf = newsScraper('https://finance.yahoo.com/', 'news', 10, "yahoo", True)
    cnbc = newsScraper('https://www.cnbc.com/economy/', '2021', 10, 'cnbc', True)

    manager = Manager(root)

    sup_list = [WSB.word_count,WSBN.word_count,WSBE.word_count,yf.word_count,cnbc.word_count]
    manager.storeDataSet(sup_list)




def runInBack():
    hour = input("Enter hours to be ran : ")
    frequency = input("Enter frequency for each run in minutes : ")
    target_time = datetime.now() + timedelta(hours=int(hour))

    print("\nStarting Process\n")

    ran = 0
    total_instances = int(int(hour)*60 / int(frequency))

    while ran < total_instances:
        cur = datetime.now()
        time_delta = target_time - cur

        print("Instance : " + cur.strftime("%H:%M:%S"))
        print("Run : " + str(ran) + " remaining : " + str(total_instances-ran))

        ran+=1


        runSingle()

        print("Completed Instance")
        print("Waiting...")
        print("Run : " + str(ran) + " remaining : " + str(total_instances - ran))

        time.sleep(int(frequency)*60)












def look():
    simp = input("Enter symbol : ")
    simp = simp.upper()

    manager = Manager(root)
    manager.readData(simp)

    printMenu()



def changeSettings():
    print("Settings")


def exit():
    print("Exiting")


#commands in dict for ease
commands = {
    'a':runSingle,
    'b':runInBack,
    'c':look,
    'd':changeSettings,
    'e':exit
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
        printMenu()







printMenu()
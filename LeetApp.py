#ins imports
from StonkRedditAPI import StonkRedditAPI
from news import newsScraper
from DataTracker import Manager
from datetime import datetime, timedelta
import time




#GUI import
import wx

class MenuPanel(wx.Panel):
    def __init__(self, parent):
        super.__init__(parent)

        ins = InstanceCreator("20210621_TripCollection")

        #sizer controls size dynamically, VERTICAL tells wx to stack items vertically
        main_sizer = wx.BoxSizeR(wx.VERTICAL)

        #button creation
        rSButton = wx.Button(self,label="Run Single")
        rIBButton = wx.Button(self,label="Run In Background")
        lButton = wx.Button(self,label="Look at Data")
        sButton = wx.Button(self,label="Settings")
        


        main_sizer.Add(rSButton,0,wx.ALL | wx.CENTER,5)
        main_sizer.Add(rIBButton,0,wx.ALL | wx.CENTER,5)
        main_sizer.Add(lButton,0,wx.ALL | wx.CENTER,5)
        main_sizer.Add(sButton,0,wx.ALL | wx.CENTER,5)

        self.SetSizer(main_sizer)


class MenuFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Leet Reader")
        self.panel = MenuPanel(self)
        self.Show()

class InstanceCreator:
    def __init__(self, root):
        self.root_path = root

    def runSingle(self):
        print("Running...")

        # Reddit Scrapers
        WSB = StonkRedditAPI('r/wallstreetbets', 'new', 'all', 100)
        WSBN = StonkRedditAPI('r/Wallstreetbetsnew', 'new', 'all', 100)
        WSBE = StonkRedditAPI('r/WallStreetbetsELITE', 'new', 'all', 100)

        # Article Scraper
        yf = newsScraper('https://finance.yahoo.com/', 'news', 10, "yahoo", True)
        cnbc = newsScraper('https://www.cnbc.com/economy/', '2021', 10, 'cnbc', True)

        manager = Manager(self.root_path)

        sup_list = [WSB.word_count, WSBN.word_count, WSBE.word_count, yf.word_count, cnbc.word_count]
        manager.storeDataSet(sup_list)

    def runInBack(self):
        hour = input("Enter hours to be ran : ")
        frequency = input("Enter frequency for each run in minutes : ")
        target_time = datetime.now() + timedelta(hours=int(hour))

        print("\nStarting Process\n")

        ran = 0
        total_instances = int(int(hour) * 60 / int(frequency))

        while ran < total_instances:
            cur = datetime.now()
            time_delta = target_time - cur

            print("Instance : " + cur.strftime("%H:%M:%S"))
            print("Run : " + str(ran) + " remaining : " + str(total_instances - ran))

            ran += 1

            self.runSingle()

            print("Completed Instance")
            print("Waiting...")
            print("Run : " + str(ran) + " remaining : " + str(total_instances - ran))

            time.sleep(int(frequency) * 60)


    def look(self):
        simp = input("Enter symbol : ")
        simp = simp.upper()

        manager = Manager(self.root_path)
        manager.readData(simp)





    def changeSettings(self):
        print("Settings")


    def exit(self):
        print("Exiting")


if __name__ == '__main__':
    app = wx.App(False)
    frame = MenuFrame
    app.MainLoop()
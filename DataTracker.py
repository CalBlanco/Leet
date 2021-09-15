from datetime import datetime
from collections import Counter




''' This class manages the storing and reading of data '''

class Manager:
    #constructor : takes the root directory
    def __init__(self, root):
        self.root = root

    #main method for storing data
    def storeDict(self, inDict):
        print("Storing Dictionary...")
        #get time
        current_time = datetime.now()
        current_time = current_time.strftime('%Y_%m_%d_%H_%M')
        print("Current Time : " + current_time)

        #create a file for each symbol and then append the data
        for key in inDict:
            filename = self.root + "/" + key + ".txt"
            with open(filename, 'a') as outFile:
                outFile.write(current_time + ":" + str(inDict[key]) + "\n")

        print("Dict stored")

    #merge a list of word counts
    def storeDataSet(self,listOfDicts):
        print('STORING DATA')
        a = Counter()
        print("Merging Counters")
        for item in listOfDicts:
            a += Counter(item)

        self.storeDict(a)
        print("DATA STORED")

    #look at data
    def readData(self, symbol):
        out_data = []


        with open(self.root + "/" + symbol + ".txt", "r") as inFile:
            lines = inFile.readlines()

        for line in lines:
            date = line[0:line.find(":")]
            count = line[line.find(":") + 1:len(line) - 1]
            data_point = (date, int(count))
            out_data.append(data_point)

            print(data_point)

        return out_data




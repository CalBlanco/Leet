import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from collections import Counter


'''
    Class graph takes in data and a name for the graph files
    
    it is really just a lot of matplotlib stuff and not crazy important long term
    just nice for data visual, this is also where the ratio is calculated but I think I will do that somewhere else
    
    Ignore this class for now, worked temporarily on old data not set up for new change
'''

class Graph:
    def __init__(self,data,name):
        x_ax = []
        count = []
        change = []
        self.data = data
        for item in data:
            x_ax.append(item[0])
            count.append(item[1])
            change.append(item[2])
        #color map
        my_cmap = plt.get_cmap("RdYlGn")
        #rescales values to fit within cmap
        rescale = lambda count: (count - np.min(count)) / (np.max(count) - np.min(count))


        #fix count
        fixed_count = []
        for item in count:
            if item > 100:
                fixed_count.append(0)
            else:
                fixed_count.append(np.log(item+1))



        fig, count_chart = plt.subplots(figsize=( (len(x_ax) / 2),max(fixed_count) + 10))
        count_chart.bar(x_ax, fixed_count)
        count_chart.set_xlabel('Symbols')
        count_chart.set_ylabel('Word Count')
        count_chart.set_title('Counts per Symbol')
        fig_fname = name + "count.png"
        fig.savefig(fig_fname)

        fig2, change_chart = plt.subplots(figsize=( (len(x_ax) / 2),max(change) + 10))
        change_chart.bar(x_ax, change, color=my_cmap(rescale(change)))
        change_chart.set_xlabel('Symbols')
        change_chart.set_ylabel('% Change')
        change_chart.set_title('% Change per Symbol')
        fig2_fname = name + "change.png"
        fig2.savefig(fig2_fname)



        fig3, ratio = plt.subplots(figsize=( (len(x_ax) / 2),max(change) + 10))
        ratio.scatter(count, change, color=my_cmap(rescale(change)))
        ratio.set_xlabel('Symbol')
        ratio.set_ylabel('log(count) * change / 100')
        fig3_fname = name+"ratio.png"
        fig3.savefig(fig3_fname)


''' This class manages the storing and reading of data '''

class Manager:
    def __init__(self, root):
        self.root = root

    def storeDict(self, inDict):
        print("Storing Dictionary...")
        current_time = datetime.now()
        current_time = current_time.strftime('%Y_%m_%d_%H_%M')
        print("Current Time : " + current_time)

        for key in inDict:
            filename = self.root + "/" + key + ".txt"
            with open(filename, 'a') as outFile:
                outFile.write(current_time + ":" + str(inDict[key]) + "\n")

        print("Dict stored")

    def storeDataSet(self,listOfDicts):
        print('STORING DATA')
        a = Counter()
        print("Merging Counters")
        for item in listOfDicts:
            a += Counter(item)

        self.storeDict(a)
        print("DATA STORED")

    def readData(self, symbol):
        out_data = []
        lines = []

        with open(self.root + "/" + symbol + ".txt", "r") as inFile:
            lines = inFile.readlines()

        for line in lines:
            date = line[0:line.find(":")]
            count = line[line.find(":") + 1:len(line) - 1]
            data_point = (date, int(count))
            out_data.append(data_point)

            print(data_point)

        return out_data



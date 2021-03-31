import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd
from datetime import datetime


'''
    Class graph takes in data and a name for the graph files
    
    it is really just a lot of matplotlib stuff and not crazy important long term
    just nice for data visual, this is also where the ratio is calculated but I think I will do that somewhere else
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


'''
    DataTracker puts the data found from the sites into a CSV file.

    @params : data this will be the handled_symbols from YahooFinnanceSearch class

     The first item of each row will be the curent time, then followed by each stock item in data formated into string format Symbol/Count/Change
     returns nothing 

     @functions : 
        writeTo() takes no parameters and writes the variable data to a csv 
        readFrom() 


'''

class DataTracker:

    def __init__(self, data, filename):
        self.filename = filename
        # get the current time when run
        cur_time = datetime.utcnow()
        self.data_strs = [cur_time]
        self.data = data
        self.outdata = []

    def writeTo(self):
        for item in self.data:
            out_str = f"{item[0]}/{item[1]}/{item[2]}"
            self.data_strs.append(out_str)
        with open(self.filename + '.csv', "a", newline='') as fp:
            wr = csv.writer(fp, dialect='excel')
            wr.writerow(self.data_strs)
            print("wrote data to file")

    def readFrom(self):
        with open(self.filename + '.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                self.outdata.append(row)
        print("extracted data from file")

        out_list = []
        for row in self.outdata:

            date = row[0]
            row_obj = [date]
            items = row[1:]
            for item in items:
                item_split = item.split('/')
                item_obj = [item_split[0], int(item_split[1]), float(item_split[2])]
                row_obj.append(item_obj)
            out_list.append(row_obj)

        return out_list


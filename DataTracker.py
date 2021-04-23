import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from collections import Counter
from datetime import datetime


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


'''
    FrameBuilder : 
    @params : 
        - data : input a list of counter objects
        - filepath : enter a new file, an existing file, or just let it use default.csv
        
    @purpose :
        - This is the fix for the long term data storage for our scraper data
    
    @core : 
    
        create frame from data
        - Takes in a list of counter objects -> adds them to a main counter object
        - use list(agg) to get the columns for the dataframe
        - get the current time
        - create an output frame with the inputed data, and date
        
        add to file
        - finds the file at the filepath parameter
        - check if the file is empty or not
            - if file not empty:
                - put the file contents into a dataframe
                - use pd.concat(file_frame, out_frame) to make the final frame
                - write the final_frame to csv
            - else:
                - write to the csv

'''

# takes in a list of counters, and needs a filepath (default is just "default")
class FrameBuilder:
    def __init__(self, data, filepath="defualt.csv"):
        # CREATING THE DATA FRAME
        # create a container for the input counters
        self.agg = Counter()
        for item in data:
            self.agg += item

        # get the symbols from the counter to represent the columns of the data frame
        df_columns = list(self.agg)

        # get current time for the row index of the data frame
        cur_time = datetime.now()

        # create frame from counter data, cur time, and symbol list
        self.out_frame = pd.DataFrame(self.agg, index=[cur_time], columns=df_columns)

        # SAVING TO FILE
        # Pandas is weird to_csv is messy
        # best strategy i could find is to just rewrite a whole file using read_csv -> appending a data frame -> to_csv

        # in order to ensure we don't get errors check for filesize of filepath, if > 0 file is not empty perform ^, else just write to a blank file and call it good
        # check if the file exists, and if its size is greater than 0
        def checkFile():
            return os.path.isfile(filepath) and os.path.getsize(filepath) > 0

        checkFile()
        if checkFile():
            # if file already has content
            print("File has content")

            # create data from from file :
            # pass it a file path
            # index_col = [0] just shifts the data over because by default there will be a column we dont need
            file_frame = pd.read_csv(filepath, index_col=[0])
            print("converting file contents to dataframe")

            final_df = pd.concat([file_frame, self.out_frame])
            print("concating file frame and output frame")

            final_df.to_csv(filepath, mode="w", columns=final_df.columns)
            print("written to file")


        else:
            # if file is empty
            print("File has no content")
            self.out_frame.to_csv(filepath, mode='w', columns=df_columns)
            print("written to file")








import matplotlib.pyplot as plt
import numpy as np


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

        rat = []
        for item in data:
            if item[2] != 0:
                log_count = np.log(item[1] + 1)
                rat.append(item[2] * log_count * (1 / 100))
            else:
                rat.append(0)

        fig3, ratio = plt.subplots(figsize=( (len(x_ax) / 2),max(rat) + 10))
        ratio.bar(x_ax, rat, color=my_cmap(rescale(rat)))
        ratio.set_xlabel('Symbol')
        ratio.set_ylabel('log(count) * change / 100')
        fig3_fname = name+"ratio.png"
        fig3.savefig(fig3_fname)
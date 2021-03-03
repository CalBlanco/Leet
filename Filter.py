




class Filter:
    def __init__(self, word_count, scalar):
        self.word_count = word_count
        self.scalar = scalar

        def getAvg(value_list):
            sum = 0
            for value in value_list:
                sum += value

            avg = round(sum/len(value_list))
            return avg


        self.filtered = self.word_count

        values = list(self.word_count.values())
        count_avg = getAvg(values)

        scalar = 5
        upper_bound = self.scalar*count_avg
        lower_bound = (1/(self.scalar*self.scalar))*count_avg

        keys = list(word_count)
        for key in keys:
            cur_item = self.filtered[key]

            if cur_item >= upper_bound or cur_item <= lower_bound:
                self.filtered.pop(key)









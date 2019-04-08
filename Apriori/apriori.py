#!/usr/bin/python
import itertools
from struct import *
from utils import *
from htree import *
import time
import yappi
import sys
import psutil
import gc
import os

# filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD1000K.data"
# filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD10K.data"
# filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD1K.data"
# sup = 30000
# sup = 50
# sup = 5

blocksize = 4


class Apriori(object):
    def __init__(self, filename, sup, debug=False):
        self.filename = filename
        self.hex = 4
        self.sup = sup
        self.htree = HTree()
        self.debug = debug

    def Read_itemsets(self, f):
        # read TID
        f.read(4 * 2)
        # read row length
        row_hex_num = f.read(4)
        num = int(unpack('<I', row_hex_num)[0])

        # num = int(hex_length[0])
        items = []

        itemset_hex = f.read(4 * num)
        i = 0
        j = 4
        for _ in range(num):
            item = unpack('<I', itemset_hex[i:j])
            items.append(item)
            i = j
            j += 4

        return items

    def Read_head(self, f):
        '''
        hex has 4 byte, but head has 8 byte, should read only one
        '''
        f.read(4)
        f.read(4)

    def Read_items_num(self, f):
        '''
        value has declare how many row data
        '''
        row_hex_num = f.read(4)
        hex_head = unpack('<I', row_hex_num)

        num = int(hex_head[0])
        # print('row data num is ', num)
        return num

    def Read_item(self, f):
        '''
        read one row data
        '''
        item = unpack('<I', f.read(4))
        return item

    def Read_items(self, f, items_num):
        '''
        read many row data
        '''
        items = []
        '''
        for _ in range(items_num):
            item = f.read(4)
            item = unpack('<I', item)
            items.append(item[0])
        '''
        itemset_hex = f.read(4 * items_num)
        i = 0
        j = 4
        for _ in range(items_num):
            item = unpack('<I', itemset_hex[i:j])
            items.append(item)
            i = j
            j += 4

        return items

    def Find_frequent_one(self, support):
        candidate1 = {}
        with open(self.filename, 'rb') as f:
            while True:
                try:
                    # load data
                    items = self.Read_itemsets(f)
                    for row in items:
                        if row not in candidate1.keys():
                            candidate1[row] = 1
                        else:
                            candidate1[row] += 1
                except BaseException:
                    break
            frequent1 = []
            for key in candidate1:
                if candidate1[key] >= support:
                    frequent1.append([key])
        return len(candidate1), len(frequent1), frequent1

    def Generate_candidate(self, prev_frequent, k):

        new_candidates = []
        lenLk = len(prev_frequent)
        for i in range(lenLk):
            for j in range(i + 1, lenLk):
                L1 = list(prev_frequent[i])[:k - 2]
                L2 = list(prev_frequent[j])[:k - 2]
                if L1 == L2:
                    temp = list(set(prev_frequent[i]) | set(prev_frequent[j]))
                    temp.sort()
                    temp = tuple(temp)
                    new_candidates.append(temp)
        new_candidates.sort(key=lambda x: x[0])

        return new_candidates

    def Generate_hash_tree(self, itemsets):
        htree = HTree()
        for itemset in itemsets:
            # add this itemset to hashtree
            htree.insert(itemset)
        return htree

    def Frequent_support(self, k):
        with open(self.filename, 'rb') as f:
            while True:
                try:

                    items = self.Read_itemsets(f)
                    k_subset = itertools.combinations(items, k)
                    '''
                    lenLk = len(items)
                    for i in range(lenLk - 1):
                        for j in range(i + 1, lenLk):
                            L1 = list(items[i])[:k - 2]
                            L2 = list(items[j])[:k - 2]
                            if L1 == L2:
                                temp = list(set(items[i]) | set(items[j]))
                                temp.sort()
                                temp = tuple(temp)
                                print(temp)
                                self.htree.add_support(temp)
                    '''

                    for subset in k_subset:
                        self.htree.add_support(subset)
                except BaseException:
                    break

    def Apriori(self):
        tStart = time.time()
        candidate_num, frequnt_num, all_frequent_itemsets = self.Find_frequent_one(self.sup)

        print('L1====================================')
        print('Frequent 1-itemset is', frequnt_num)
        process = psutil.Process(os.getpid())
        print('Used Memory:', process.memory_info().rss / 1024 / 1024, 'MB')
        prev_frequent_num = frequnt_num
        print('====================================')
        tEnd = time.time()
        print(tEnd - tStart)

        prev_frequent = [x for x in all_frequent_itemsets]
        prev_frequent.sort(key=lambda tup: tup)
        length = 2
        while len(prev_frequent) > 1:
            tStart = time.time()
            if self.debug:
                # profilling
                yappi.clear_stats()  # clear profiler
                yappi.set_clock_type('cpu')
                yappi.start(builtins=True)  # track builtins

            new_candidate = self.Generate_candidate(prev_frequent, length)

            print('L%s====================================' % (length))
            print('Total candidates is ', len(new_candidate) + prev_frequent_num)
            self.htree = self.Generate_hash_tree(new_candidate)
            self.Frequent_support(length)

            # find frequent itemsets
            new_frequent = self.htree.get_frequent_itemsets(self.sup)

            print('Frequent itemset is', len(new_frequent) + prev_frequent_num)
            process = psutil.Process(os.getpid())
            print('Used Memory:', process.memory_info().rss / 1024 / 1024, 'MB')
            print('====================================')
            tEnd = time.time()
            print(tEnd - tStart)

            prev_frequent_num = len(new_frequent) + prev_frequent_num
            # all_frequent_itemsets.extend(new_frequent)
            prev_frequent = [tup[0] for tup in new_frequent]
            prev_frequent.sort()
            if self.debug:
                yappi.stop()
                stat = yappi.get_func_stats()
                var = 'callgrind.generate_tree' + str(length)
                stat.save(var, type='callgrind')
                # profilling end

            length += 1
            '''
            gc
            '''
            del self.htree
            del new_candidate
            del new_frequent
            gc.collect()

        return all_frequent_itemsets


ap = Apriori(filename=str(sys.argv[1]), sup=int(sys.argv[2]))
# ap = Apriori(filename, sup)

tStart = time.time()
frequent = ap.Apriori()
tEnd = time.time()
print("total time is ", tEnd - tStart)
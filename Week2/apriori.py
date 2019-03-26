#!/usr/bin/python
import itertools
from struct import *
from utils import *
from htree import *
import time
import yappi
import sys
#filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD1000K.data"
#filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD10K.data"
#filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD1K.data"
#sup = 30000
#sup = 50
#sup = 5

blocksize = 4


class Apriori(object):
    def __init__(self, filename, sup):
        self.filename = filename
        self.hex = 4
        self.sup = sup

    def Read_head(self, f):
        '''
        hex has 4 byte, but head has 8 byte, should read only one
        '''
        # block = f.read(self.hex_size).hex()
        f.read(4)
        f.read(4)
        # hex_head = unpack('<I', row_hex_head)

        # head = int(hex_head[0])
        #print('head is ', head)


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
        for _ in range(items_num):
            item = f.read(4)
            item = unpack('<I', item)
            items.append(item[0])
        return items

    def Apriori_generate_frequent_itemsets(self):
        tStart = time.time()
        candidate_num, frequnt_num, all_frequent_itemsets = self.Find_frequent_one(self.sup)
        print('L1====================================')
        print('Frequent 1-itemset is', frequnt_num)
        prev_frequent_num = frequnt_num
        print('====================================')
        tEnd = time.time()
        print(tEnd - tStart)
        prev_frequent = [x for x in all_frequent_itemsets]
        prev_frequent.sort(key=lambda tup: tup)

        length = 2
        while len(prev_frequent) > 1:

            #profilling
            yappi.clear_stats()  # clear profiler
            yappi.set_clock_type('cpu')
            yappi.start(builtins=True)  # track builtins

            tStart = time.time()
            h_tree = self.generate_candidate(length)
            print('L%s====================================' %(length))
            #print('Candidate itemset is', len(h_tree.root.bucket))
            # find frequent itemsets
            new_frequent = h_tree.get_frequent_itemsets(self.sup)
            print('Frequent itemset is', len(new_frequent)+prev_frequent_num)
            prev_frequent_num = len(new_frequent)+prev_frequent_num
            print('====================================')
            tEnd = time.time()
            print(tEnd - tStart)

            #all_frequent_itemsets.extend(new_frequent)
            prev_frequent = [tup[0] for tup in new_frequent]
            prev_frequent.sort()

            yappi.stop()
            stat = yappi.get_func_stats()
            var = 'callgrind.generate_tree' + str(length)
            stat.save(var, type='callgrind')
            # profilling end
            length += 1

        return all_frequent_itemsets
    '''
    def generate_candidate(self, prev_frequent, length):
        new_candidates = []
        new_candidates.extend(itertools.combinations(prev_frequent, length))
        
        for i in range(len(prev_frequent)):
            j = i + 1
            while j < len(prev_frequent): #and is_prefix(prev_frequent[i], prev_frequent[j]):
                # this part makes sure that all of the items remain
                # lexicographically sorted.
                new_candidates.append(
                    list(prev_frequent[i][:-1]) + [prev_frequent[i][-1]] + [prev_frequent[j][-1]]
                )
                j += 1
            print(new_candidates[-1])
        
        #print(new_candidates)#((92,), (456,)) ,[496, 497]
        return new_candidates
    '''

    def generate_hash_tree(self, htree, itemsets):

        # add this itemset to hashtree
        htree.insert(itemsets)
        return htree

    def generate_candidate(self, length):
        htree = HTree()
        with open(self.filename, 'rb') as f:
            while True:
                try:
                    # load data
                    self.Read_head(f)
                    num = self.Read_items_num(f)
                    items = self.Read_items(f, num)
                    #subsets.extend(map(list, itertools.combinations(items, length)))
                    #subsets.extend(itertools.combinations(items, length))
                    itemset = itertools.combinations(items, length)
                    htree = self.generate_hash_tree(htree, itemset)

                except BaseException:
                    break
        return htree


    '''
	apriori prune
	'''
    def Find_frequent_one(self, support):
        candidate1 = {}
        with open(self.filename, 'rb') as f:
            while True:
                try:
                    # load data
                    self.Read_head(f)
                    num = self.Read_items_num(f)
                    '''
                    items = []
                    for _ in range(0, num):
                        items.append(self.Read_item(f))
                    '''
                    items = self.Read_items(f, num)
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


ap = Apriori(filename=str(sys.argv[1]), sup=int(sys.argv[2]))
#ap = Apriori(filename, sup)

tStart = time.time()
frequent = ap.Apriori_generate_frequent_itemsets()
tEnd = time.time()
print(tEnd - tStart)


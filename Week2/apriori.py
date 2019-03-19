#!/usr/bin/python
import itertools
from struct import *
from utils import *
from htree import *
import time
import sys

#filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD1000K.data"
#filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD10K.data"
filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD1K.data"
#sup = 30000
#sup = 50
sup = 5

blocksize = 4


class Apriori(object):
    def __init__(self, filename, sup):
        self.filename = filename
        self.hex = 4
        self.sup = sup

    def Load_data(self, filename):
        itemset = []
        with open(filename, 'rb') as f:
            while True:
                try:
                    # load data
                    self.Read_head(f)
                    num = self.Read_items_num(f)
                    items = self.Read_items(f, num)
                    itemset.append(items)
                except BaseException:
                    break

            return itemset

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



    def Read_items(self, f, items_num):
        '''
        read many row data
        '''
        items = []
        for i in range(0, items_num):
            item = f.read(4)
            item = unpack('<I', item)
            items.append(item)
        return items

    def Apriori_generate_frequent_itemsets(self):
        tStart = time.time()
        #dataset = self.Load_data(self.filename)

        candidate_num, frequnt_num, all_frequent_itemsets = self.Find_frequent_one(self.sup)
        print('L1====================================')
        print('Candidate 1-itemset is', candidate_num)
        print('Frequent 1-itemset is', frequnt_num)
        prev_frequent_num = frequnt_num
        print('====================================')
        tEnd = time.time()
        print(tEnd - tStart)

        prev_frequent = [x[0] for x in all_frequent_itemsets]
        prev_frequent.sort(key=lambda tup: tup[0])

        length = 2
        while len(prev_frequent) > 1:
            tStart = time.time()
            new_candidates = []
            for i in range(len(prev_frequent)):
                j = i + 1
                while j < len(prev_frequent) and is_prefix(
                        prev_frequent[i], prev_frequent[j]):
                    # this part makes sure that all of the items remain
                    # lexicographically sorted.
                    new_candidates.append(
                        list(prev_frequent[i][:-1]) + [prev_frequent[i][-1]] + [prev_frequent[j][-1]])
                    j += 1
            # generate hash tree and find frequent itemsets
            h_tree = self.generate_hash_tree(new_candidates)

            # for each transaction, find all possible subsets of size "length"
            k_subsets = self.generate_k_subsets(length)
            #k_subsets.sort(key=lambda tup: tup[1])
            #k_subsets.sort(key=lambda tup: tup[0])

            # support counting and finding frequent itemsets
            for subset in k_subsets:
                h_tree.add_support(subset)

            print('L2====================================')
            print('Candidate itemset is', len(h_tree.root.bucket))
            # find frequent itemsets
            new_frequent = h_tree.get_frequent_itemsets(sup)
            print('Frequent itemset is', len(new_frequent)+prev_frequent_num)
            prev_frequent_num = len(new_frequent)+prev_frequent_num
            print('====================================')
            tEnd = time.time()
            print(tEnd - tStart)

            all_frequent_itemsets.extend(new_frequent)
            prev_frequent = [tup[0] for tup in new_frequent]
            prev_frequent.sort()
            length += 1

        return all_frequent_itemsets
    #4, 5
    def generate_hash_tree(self, candidate_itemsets):
        """
        This function generates hash tree of itemsets with each node having no more than child_max_length
        childs and each leaf node having no more than max_leaf_length.
        :param candidate_itemsets: Itemsets
        :param length: Length if each itemset
        :param max_leaf_length:
        :param child_max_length:
        :return:
        """
        htree = HTree()
        for itemset in candidate_itemsets:
            # add this itemset to hashtree
            htree.insert(itemset)
        return htree

    def generate_k_subsets(self, length):
        subsets = []
        with open(filename, 'rb') as f:
            while True:
                try:
                    # load data
                    self.Read_head(f)
                    num = self.Read_items_num(f)
                    items = self.Read_items(f, num)
                    subsets.extend(map(list, itertools.combinations(items, length)))
                except BaseException:
                    break
        subsets = self.convert_tuple2int(subsets)
        return subsets

    def convert_tuple2int(self, dataset):
        subsets = []
        for itemset in dataset:
            set = []
            for item in itemset:
                set.append(int(item[0]))
            subsets.append(set)
        return subsets


    '''
	apriori prune
	'''

    def Find_frequent_one(self, support):
        candidate1 = {}
        with open(filename, 'rb') as f:
            while True:
                try:
                    # load data
                    self.Read_head(f)
                    num = self.Read_items_num(f)
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




ap = Apriori(sys.argv[1], int(sys.argv[2]))

tStart = time.time()
frequent = ap.Apriori_generate_frequent_itemsets()
tEnd = time.time()
print(tEnd - tStart)


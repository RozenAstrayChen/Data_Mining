#!/usr/bin/python
import itertools
from struct import *
import time
import yappi
import sys
import psutil
from collections import defaultdict
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

        return frozenset(items)

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
        items = frozenset(items)
        return items

    def Read_data(self):
        dataset = []
        with open(self.filename, 'rb') as f:
            while True:
                try:
                    # load data
                    items = self.Read_itemsets(f)
                    dataset.append(items)
                except BaseException:
                    break
        return dataset

    # data; frozenset
    # return: list of 2-item frozensets
    def generate_2items_sets(self, data):
        data = sorted(data)
        lst = []
        i = 1
        for a in data:
            for b in data[i:]:
                lst.append(frozenset([a, b]))
            i += 1
        return lst

    # @param: dataset<list<frozenset>>
    # @param: support<int>
    # @return: results<dict<frozenset: int>>; dhp<Counter>
    def get_frequent_single_items(self, dataset, support, results):
        single_counter = defaultdict(int)
        dhp = defaultdict(int)
        for data in dataset:
            for item in self.generate_2items_sets(data):
                dhp[item] += 1
            for each in data:
                single_counter[each] += 1
        for k in single_counter:
            if single_counter[k] >= support:
                results[frozenset([k])] = single_counter[k]
        return dhp

    # candidates: <dict<frozenset: int>>
    # c: frozenset
    def isFrequent(self, candidates, c):
        for each in c:
            one_subset = c - frozenset([each])
            if one_subset not in candidates:
                # print one_subset
                return False
        return True

    # @param: candidates<dict<frozenset: int>>
    # @param: k<int>
    # return: results<set<frozenset>>
    def generate_candidates(self, candidates, k):
        res = set()
        for a in candidates:
            for b in candidates:
                c = a | b
                if len(c) == k and a != b:
                    if self.isFrequent(candidates, c):
                        res.add(c)
        return res

    # @param: dataset<list<frozenset>>
    # @param: candidates<dict<frozenset: int>>
    # @return counted<Counter<frozenset: int>>
    def count_candidates(self, dataset, candidates):
        counted = defaultdict(int)
        for instance in dataset:
            bucket = [candidate for candidate in candidates if candidate <= instance]
            for each in bucket:
                counted[each] += 1
        return counted

    # @param: counted<dict<frozenset: int>>
    # @param: support<int>
    # @return: results<dict<frozenset: int>>
    def generate_support_candidates(self, counted, support):
        results = {}
        for item in counted:
            if counted[item] >= support:
                # key = frozenset(sorted(item))
                # print key
                results.update({item: counted[item]})
        return results

    def Apriori(self):
        results = {}
        dataset = self.Read_data()
        #process = psutil.Process(os.getpid())
        #print('Used Memory:', process.memory_info().rss / 1024 / 1024, 'MB')

        candidates = self.get_frequent_single_items(dataset, self.sup, results)
        print('This is the 2 iteration')
        support_candidates = {}
        if candidates:
            for item in candidates:
                if candidates[item] >= self.sup:
                    support_candidates.update({item: candidates[item]})
        print(len(results))
        results.update(support_candidates)
        candidates = support_candidates
        k = 3
        while candidates:
            print('This is the %d iteration' % k)
            candidates = self.generate_candidates(candidates.keys(), k)
            if not candidates: break
            counted = self.count_candidates(dataset, candidates)
            support_candidates = self.generate_support_candidates(counted, self.sup)
            results.update(support_candidates)
            candidates = support_candidates

            print(len(results))
            k += 1
        return results





ap = Apriori(filename=str(sys.argv[1]), sup=int(sys.argv[2]), debug=bool(sys.argv[3]))

tStart = time.time()
frequent = ap.Apriori()
tEnd = time.time()
print("total time is ", tEnd - tStart)

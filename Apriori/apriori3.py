from collections import defaultdict
import itertools
import sys
import time
import psutil
import os
from struct import *
import yappi



class Apriori():
    def __init__(self, filename, sup, debug=False):
        self.filename = filename
        self.hex = 4
        self.sup = sup
        self.debug = debug

    def Read_itemsets(self, f):
        f.read(4*2)
        row_hex_num = f.read(4)
        num = int(unpack('<I', row_hex_num)[0])

        items = []

        itemset_hex = f.read(4 * num)
        i = 0
        j = 4
        for _ in range(num):
            item = unpack('<I', itemset_hex[i:j])
            items.append(item)
            i = j
            j += 4

        items = frozenset(items)
        return items

    def Read_data(self):
        itemsets = []
        with open(self.filename, 'rb') as f:
            while True:
                try:
                    # load data
                    itemset = self.Read_itemsets(f)
                    itemsets.append(itemset)

                except BaseException:
                    break

        return itemsets


    def Generate_2items_sets(self, items):
        items = sorted(items)
        lst = []
        i = 1
        for a in items:
            for b in items[i:]:
                lst.append(frozenset([a, b]))
            i += 1
        return lst


    def Get_frequent_single_items(self, results):
        '''

        :param D: DataSet
        :param results: frequent candidates
        :return: k=2 itemsets
        '''
        single_counter = defaultdict(int)
        dhp = defaultdict(int)

        # generate C1
        for TID in self.D:
            #for itemset in self.Generate_2items_sets(TID):
            #    dhp[itemset] += 1

            for itemset in TID:
                single_counter[itemset] += 1

        # count items and collect need delete items
        delete_item = set()
        for k in single_counter:
            if single_counter[k] >= self.sup:
                results[frozenset([k])] = single_counter[k]
            else:
                delete_item.add(k)

        # delete items from D
        delete_item = sorted(delete_item)
        for i in range(len(self.D)):
            temp = self.D[i] - set(delete_item)
            #print('D', D[i], len(D[i]),'\n')
            #print('delete', delete_item,len(delete_item),'\n')
            #print('temp', temp, len(temp))
            self.D[i] = temp

        # generate C2:
        for TID in self.D:
            for itemset in self.Generate_2items_sets(TID):
                dhp[itemset] += 1

        return dhp

    def IsFrequent(self, candidates, c):
        for each in c:
            c = frozenset(c)
            one_subset = c - frozenset([each])
            #print('c', c, '\n')
            #print('each', each, '\n')
            #print(candidates)
            if one_subset not in candidates:
                return False
        return True
    '''
    remove sort <= k-1 from DataSet
    '''
    def Filter_dataSet(self, k):
        pop_i = []
        for i in range(len(self.D)):
            sort = len(self.D[i])
            if sort <= k-1:
                pop_i.append(i)
        print('pop', pop_i)
        # if you pop one ,the items will move ahead, so should n-1
        j = 0
        for i in pop_i:
            self.D.pop(i-j)
            j += 1

    def Generate_candidates(self, candidates, k):

        #res = set()
        res = defaultdict(int)
        for TID in self.D:
            frequent_itemset = itertools.combinations(TID, k)
            for itemset in frequent_itemset:
                if self.IsFrequent(candidates, itemset):
                    res[frozenset(itemset)] += 1

        return res

    # 2: frozenset({(51,), (28,), (444,)}),
    # 3: frozenset({(142,), (217,), (412,)})
    def Count_candidates(self, candidates):
        counted = defaultdict(int)
        for TID in self.D:

            bucket = [candidate for candidate in candidates if candidate <= TID]
            for each in bucket:
                counted[each] += 1


        return counted


    def Generate_support_candidates(self, counted, support):
        results = {}
        for item in counted:
            if counted[item] >= support:
                # key = frozenset(sorted(item))
                # print key
                results.update({item: counted[item]})
        return results

    def Apriori(self):
        results = {}
        support_candidates = {}

        tStart = time.time()
        self.D = self.Read_data()
        tEnd = time.time()
        print('Read Data set', tEnd - tStart)
        process = psutil.Process(os.getpid())
        print('Used Memory:', process.memory_info().rss / 1024 / 1024, 'MB')

        tStart = time.time()
        candidates = self.Get_frequent_single_items(results)
        process = psutil.Process(os.getpid())
        tEnd = time.time()
        print('Used Memory:', process.memory_info().rss / 1024 / 1024, 'MB')
        print('L1', len(results))
        print('Speed time', tEnd - tStart)

        tStart = time.time()
        if candidates:
            for item in candidates:
                if candidates[item] >= self.sup:
                    support_candidates.update({item: candidates[item]})



        results.update(support_candidates)
        candidates = support_candidates

        tEnd = time.time()
        print('L2', len(results), len(support_candidates))
        process = psutil.Process(os.getpid())
        print('Used Memory:', process.memory_info().rss / 1024 / 1024, 'MB\n')

        k = 3

        while candidates:
            tStart = time.time()

            self.Filter_dataSet(k)
            print('after filter data set', len(self.D))
            candidates =self.Generate_candidates(candidates.keys(), k)

            if not candidates: break
            #support_candidates = self.Count_candidates(candidates)
            candidates = self.Generate_support_candidates(candidates, self.sup)
            results.update(candidates)
            print('L%s====================================' % (k))
            print(len(results), len(candidates))

            k += 1
            tEnd = time.time()
            print('Speed time', tEnd - tStart)
            process = psutil.Process(os.getpid())
            print('Used Memory:', process.memory_info().rss / 1024 / 1024, 'MB\n')




ap = Apriori(filename=str(sys.argv[1]), sup=int(sys.argv[2]), debug=bool(sys.argv[3]))

tStart = time.time()
ap.Apriori()
tEnd = time.time()
print("total time is ", tEnd - tStart)
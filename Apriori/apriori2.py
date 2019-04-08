from collections import defaultdict
import itertools
import sys
import time
from struct import *
import yappi


class Apriori():
    def __init__(self, filename, sup, debug=False):
        self.filename = filename
        self.hex = 4
        self.sup = sup
        self.debug = debug

    def Read_itemsets(self, f):
        f.read(4 * 2)
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

        single_counter = defaultdict(int)
        dhp = defaultdict(int)

        with open(self.filename, 'rb') as f:
            while True:
                try:
                    # load data
                    items = self.Read_itemsets(f)
                    for item in self.Generate_2items_sets(items):
                        dhp[item] += 1
                    for item in items:
                        single_counter[item] += 1
                except BaseException:
                    break

        for k in single_counter:
            if single_counter[k] >= self.sup:
                results[frozenset([k])] = single_counter[k]
        return dhp

    def IsFrequent(self, candidates, c):
        for each in c:
            one_subset = c - frozenset([each])
            if one_subset not in candidates:
                return False
        return True

    def Generate_candidates(self, candidates, k):

        res = set()
        for a in candidates:
            for b in candidates:
                c = a | b
                if len(c) == k and a != b:
                    if self.IsFrequent(candidates, c):
                        res.add(c)
        print(res)
        return res

    def Count_candidates(self, candidates, k):
        counted = defaultdict(int)
        with open(self.filename, 'rb') as f:
            while True:
                try:
                    # load data
                    items = self.Read_itemsets(f)

                    bucket = [candidate for candidate in candidates if candidate <= items]

                    for each in bucket:
                        counted[each] += 1

                    '''
                    for can in candidates:
                        if can.issubset(items):
                            counted[can] += 1
                    '''
                except BaseException:
                    break
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

        candidates = self.Get_frequent_single_items(results)
        print('L1', len(results))

        '''filter support'''
        if candidates:
            for item in candidates:
                if candidates[item] >= self.sup:
                    support_candidates.update({item: candidates[item]})

        results.update(support_candidates)
        candidates = support_candidates
        print('L2', len(results), len(support_candidates))

        k = 3
        while candidates:

            candidates = self.Generate_candidates(candidates.keys(), k)
            print('total candidate', len(candidates))
            if not candidates: break
            support_candidates = self.Count_candidates(candidates, k)
            candidates = self.Generate_support_candidates(support_candidates, self.sup)
            results.update(candidates)
            print('L3', len(results), len(candidates))

            k += 1


ap = Apriori(filename=str(sys.argv[1]), sup=int(sys.argv[2]), debug=bool(sys.argv[3]))

tStart = time.time()
ap.Apriori()
tEnd = time.time()
print("total time is ", tEnd - tStart)
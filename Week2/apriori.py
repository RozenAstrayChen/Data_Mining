#!/usr/bin/python
import itertools
from struct import *
from utils import *
from htree import *
import time

filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD1000K.data"
#filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD10K.data"
#filename = "/Users/Rozen_mac/code/mining/Week2/T15I7N0.5KD1K.data"
sup = 30000
#sup = 50
#sup = 5

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
        dataset = self.Load_data(self.filename)

        candidate_num, frequnt_num, all_frequent_itemsets = self.Find_frequent_one(
            dataset, sup)
        print('L1====================================')
        print('Candidate 1-itemset is', candidate_num)
        print('Frequent 1-itemset is', frequnt_num)
        prev_frequent_num = frequnt_num
        print('====================================')
        prev_frequent = [x[0] for x in all_frequent_itemsets]
        prev_frequent.sort(key=lambda tup: tup[0])
        length = 2
        while len(prev_frequent) > 1:
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
            k_subsets = self.generate_k_subsets(dataset, length)
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
            if len(new_frequent) == 0:
                break
            all_frequent_itemsets.extend(new_frequent)
            prev_frequent = [tup[0] for tup in new_frequent]
            prev_frequent.sort()
            length += 1
            #break
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

    def generate_k_subsets(self, dataset, length):

        subsets = []
        for itemset in dataset:
            subsets.extend(map(list, itertools.combinations(itemset, length)))
            """
            for i in range(0, len(itemset)):
                for j in range(i+1, len(itemset)):
                    set = []
                    set.append(i)
                    set.append(j)
                    subsets.append(set)
            """
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

    def Find_frequent_one(self, itemset, support):
        candidate1 = {}
        for row in itemset:
            for word in row:
                if word not in candidate1.keys():
                    candidate1[word] = 1
                else:
                    candidate1[word] += 1
        frequent1 = []
        for key in candidate1:
            if candidate1[key] >= support:
                frequent1.append([key])

        return len(candidate1), len(frequent1), frequent1

    def generate_association_rules(self, f_itemsets, confidence):
        """
        This method generates association rules with confidence greater than threshold
        confidence. For finding confidence we don't need to traverse dataset again as we
        already have support of frequent itemsets.
        Remember Anti-monotone property ?
        I've done pruning in this step also, which reduced its complexity significantly:
        Say X -> Y is AR which don't have enough confidence then any other rule X' -> Y'
        where (X' subset of X) is not possible as sup(X') >= sup(X).
        :param f_itemsets: Frequent itemset with their support values
        :param confidence:
        :return: Returns association rules with associated confidence
        """

        hash_map = {}
        for itemset in f_itemsets:
            hash_map[tuple(itemset[0])] = itemset[1]

        a_rules = []
        for itemset in f_itemsets:
            length = len(itemset[0])
            if length == 1:
                continue

            union_support = hash_map[tuple(itemset[0])]
            for i in range(1, length):

                lefts = map(list, itertools.combinations(itemset[0], i))
                for left in lefts:
                    conf = 100.0 * union_support / hash_map[tuple(left)]
                    if conf >= confidence:
                        a_rules.append([left, list(set(itemset[0]) - set(left)), conf])
        return a_rules


ap = Apriori(filename, sup)

tStart = time.time()
frequent = ap.Apriori_generate_frequent_itemsets()
a_rules = ap.generate_k_subsets(frequent, 5)
tEnd = time.time()
print(tEnd - tStart)

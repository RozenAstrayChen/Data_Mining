class HNode:
    """
    Class which represents node in a hash tree.
    """
    def __init__(self):
        self.bucket = {}

class HTree:
    """
    Wrapper class for HTree instance
    """

    def __init__(self):
        self.bucket = {}
        self.frequent_itemsets = []

    def insert(self, itemsets):
        self.bucket = dict.fromkeys(itemsets, 0)
        '''
        for itemset in itemsets:
            self.bucket[itemset] = 0
        '''

    def add_support(self, itemsets):
        for itemset in itemsets:
            #print(itemset)
            if itemset in self.bucket:
                self.bucket[itemset] += 1


    def bfs(self, support):
        '''
        for key, value in self.bucket.items():
            if value >= support:
                self.frequent_itemsets.append(key)
        '''
        self.frequent_itemsets = list((k, v) for k, v in self.bucket.items() if v >= support)

    def get_frequent_itemsets(self, support_cnt):
        """
        Returns all frequent itemsets which can be considered for next level
        :param support_cnt: Minimum cnt required for itemset to be considered as frequent
        :return:
        """
        self.frequent_itemsets = []
        self.bfs(support_cnt)
        return self.frequent_itemsets

    def hash(self, val):
        if type(val) is tuple:
            val = int(val[0])
        #return val % self.max_child_cnt
        return val
class HNode:
    """
    Class which represents node in a hash tree.
    """
    def __init__(self):
        #self.children = {}
        self.bucket = {}
        self.isLeaf = True



class HTree:
    """
    Wrapper class for HTree instance
    """

    def __init__(self):
        self.root = HNode()
        self.frequent_itemsets = []

    def insert(self, itemsets):
        for itemset in itemsets:
            if itemset in self.root.bucket:
                self.root.bucket[itemset] += 1
            else:
                self.root.bucket[itemset] = 1

    def add_support(self, itemset):
        runner = self.root
        itemset = tuple(itemset)
        if itemset in runner.bucket:
            runner.bucket[itemset] += 1


    def bfs(self, node, support):

        for key, value in node.bucket.items():
            if value >= support:
                self.frequent_itemsets.append((list(key), value))
                # print key, value, support_cnt

    def get_frequent_itemsets(self, support_cnt):
        """
        Returns all frequent itemsets which can be considered for next level
        :param support_cnt: Minimum cnt required for itemset to be considered as frequent
        :return:
        """
        self.frequent_itemsets = []
        self.bfs(self.root, support_cnt)
        return self.frequent_itemsets

    def hash(self, val):
        if type(val) is tuple:
            val = int(val[0])
        #return val % self.max_child_cnt
        return val
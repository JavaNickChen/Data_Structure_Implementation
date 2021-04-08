'''
    Hash map/table based Dictionary Structure:
        'hashTable' is the key variable in class Dictionary.
        'hashTable' is built-in list of Python, and consists of 'HeadNode' (a class).
        'HeadNode' refer to a Singly Linked List which consists of 'ChainNode' (a class).
        A 'ChainNode' store a key and relevant values.
'''


class ChainNode:
    def __init__(self):
        # 'key' and 'value' store the pair of (key,value)
        self.key = None
        self.values = []  # the dictionary support the different values with the same key


# HeadNodes consist of a hash table.
class HeadNode(object):
    def __init__(self):
        # 'count' is to store the length of chain that the 'singlyLinkedList' refers to, the number of values, not keys
        self.count = 0
        # to store existing keys in the linked list--'singlyLinkedList'
        self.keys = []
        # 'SinglyLinkedList' refers to a Singly Linked List which store the pairs of (key,value)
        # that share the same hash address.
        self.singlyLinkedList = []


class Dictionary(object):
    def __init__(self):
        # length of hash table. It means that the hash address is in {0,1,2,3,4,5,6,7,8,9}
        self.length = 10
        self.hashTable = [HeadNode() for i in range(self.length)]
        self.iter_index = -1  # used for __next__

    # To convert the 'key' to hash address.
    # Return: the integer between 0 to 9.
    def hash_func(self, key):
        # List, dict and set are unhashable type. We cannot call __hash__() if the type of key is list, dict or set.
        # 没有考虑到多键情况。应该支持传入的key是list、set和tuple类型的。
        # 但是需要将list、set转换为tuple，且进行重复检查。若有重复的键，则应该报错。
        if type(key) in [list, dict, set] or (key is None):
            return -1  # '-1' means that the key is invalid
        return key.__hash__() % self.length

    # To validate the 'key' and 'value'
    # If 'key' and 'value' are valid, return the hash address and the True.
    def validation_check(self, key, value):
        hash_address = self.hash_func(key)
        if (hash_address == -1) or (value is None):
            return [False, "Fail. Invalid key or value"]
        else:
            return [True, hash_address]

    # Add a new element by key.
    # 应该支持value是list\set\tuple\dict类型。
    def add(self, key, value):
        [is_valid, message] = self.validation_check(key, value)
        if not is_valid:
            return "Fail. Invalid key or value"

        # If is_valid is True, the 'message' is hash_address.
        head_node = self.hashTable[message]

        # Create a new node and assign values.
        node_new = ChainNode()
        node_new.key = key
        node_new.values.append(value)

        # If there is no collision, enter.
        if head_node.count == 0:
            # use the built-in list for storing new node and modify Statistical information.
            head_node.singlyLinkedList.append(node_new)
            head_node.count = 1
            head_node.keys.append(key)
        else:
            # If there is no same key in the head_node.keys, enter.
            if key not in head_node.keys:
                head_node.singlyLinkedList.append(node_new)
                head_node.keys.append(key)
                head_node.count = head_node.count + 1
            else:
                for index in range(len(head_node.singlyLinkedList)):
                    if key == head_node.singlyLinkedList[index].key:
                        if value not in head_node.singlyLinkedList[index].values:
                            head_node.singlyLinkedList[index].values.append(value)
                            head_node.count = head_node.count + 1
                        break
        return "Successfully store"

    # remove an element by key.
    def remove_by_key(self, key):
        # validation part
        hash_address = self.hash_func(key)
        if hash_address == -1:
            return "Fail. Invalid key"
        head_node = self.hashTable[hash_address]
        if key not in head_node.keys:
            return "Fail. No such key"

        for index in range(len(head_node.singlyLinkedList)):
            if head_node.singlyLinkedList[index].key == key:
                head_node.singlyLinkedList.pop(index)
                break
        return "Successfully delete"

    # Return the number of keys and values in the hash table.
    def size(self):
        count_keys = 0  # store the number of different keys
        count_values = 0  # store the the number of different values
        for node in self.hashTable:
            count_values = count_values + node.count
            count_keys = count_keys + len(node.keys)
        return [count_keys, count_values]

    # Conversion to built-in list.
    def to_list(self):
        keys = []
        values = []
        for head_node in self.hashTable:
            if head_node.count != 0:
                for node in head_node.singlyLinkedList:
                    keys.append(node.key)
                    keys.sort()
                    values.insert(keys.index(node.key), node.values)
        result = []
        for index in range(0, len(keys)):
            result.append((keys[index], values[index]))
        return result

    # Conversion to built-in list.
    def from_list(self, lst):
        for element in lst:
            key = element[0]
            value = element[1]
            self.add(key, value)

    # Find element by specific key.
    def get_by_key(self, key):
        hash_address = self.hash_func(key)
        if key == -1:
            return "Fail. Invalid key."
        head_node = self.hashTable[hash_address]
        result = None
        for node in head_node.singlyLinkedList:
            if node.key == key:
                result = node
                break
        return result.values

    '''
        predicate can be "even_value" or "odd_value".
        The former will make the function to pick out the keys with even number of values.
        The latter will make the function to pick out the keys with odd number of values.
    '''
    def filter(self, predicate):
        keys_even = []
        keys_odd = []

        for head_node in self.hashTable:
            for node in head_node.singlyLinkedList:
                if len(node.values) % 2 == 0:
                    keys_even.append(node.key)
                else:
                    keys_odd.append(node.key)
        if predicate == "even_value":
            keys_even.sort()  # It must be a separate line. Otherwise it will show a value of None.
            return keys_even
        elif predicate == "odd_value":
            keys_odd.sort()
            return keys_odd

    # Map structure by specific function.
    def map_my(self, func):
        for head_node in self.hashTable:
            for node in head_node.singlyLinkedList:
                value = node.values[0]
                node.values = [func(value)]

    # Reduce process structure elements to build a return value by specific functions.
    # The object of reducing is the values of "key-value". The object is a list.
    def reduce_my(self, func, key, initial_state):
        hash_address = self.hash_func(key)
        if hash_address == -1:
            return "Fail. Invalid key."
        iterable = []
        head_node = self.hashTable[hash_address]
        for node in head_node.singlyLinkedList:
            if key == node.key:
                iterable = node.values
        it = iter(iterable)
        value = initial_state
        for element in it:
            value = func(value, element)
        return value

    '''
        An iterable object is an object that implements __iter__, which is expected to return an iterator object.
        An iterator is an object that implements __next__, which is expected to return the next element of the iterable object 
        that returned it, and raise a StopIteration exception when no more elements are available.
    '''
    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration
        # if self.iter_index == 10:
        #     self.iter_index = 0
        #     raise StopIteration
        # keys_values_list = self.hashTable[self.iter_index].singlyLinkedList
        # self.iter_index = self.iter_index + 1
        # self.tmp = self.hashTable[self.iter_index].singlyLinkedList
        # return keys_values_list

    # To concatenate two dictionary objects and self store the result.
    def mconcat(self, dictionary):
        # to traverse the hash table and add the special nodes in dictionary to self.
        for index in range(self.length):
            if dictionary.hashTable[index].count != 0:
                for node in dictionary.hashTable[index].singlyLinkedList:
                    if node.key not in self.hashTable[index].keys:
                        self.hashTable[index].singlyLinkedList.append(node)
                        self.hashTable[index].keys.append(node.key)
                        self.hashTable[index].count = self.hashTable[index].count + 1

    def mempty(self):
        return Dictionary()


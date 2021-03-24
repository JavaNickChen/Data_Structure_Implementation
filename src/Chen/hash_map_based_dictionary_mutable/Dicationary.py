'''
Dictionary based on hash-map (collision resolution: separate chaining, link)
• You can use the built-in list for storing buckets and bucker itself.
• You need to check that your implementation correctly works with None value
• You need to implement functions/methods for getting/setting value by key.
'''

'''
    mutable的字典应该使用链表结构来实现。因为其允许自身的值发生变化，反而（首）地址可以不用变化
    immutable因为不允许其自身发生变化，反而在实现动态增长的时候，返回的对象会变化。
    
    我需要实现的是mutable版本，因为对象首地址不发生变化，若采用链表结构来实现字典，则需要使用带有头结点的单链表。
'''


class ChainNode:
    def __init__(self):
        # 'key' and 'value' store the pair of (key,value)
        # the dictionary support the different values with the same key
        self.key = None
        self.values = []
        # 'next' refers to another ChainNode


# HeadNodes consist of a hash table.
class HeadNode(object):
    def __init__(self):
        # 'count' is to store the length of chain that the 'SinglyLinkedList' refers to, not the number of keys
        self.count = 0
        # to store existing keys in the linked list
        self.keys = []
        # 'SinglyLinkedList' refers to a Singly Linked List which store the pairs of (key,value)
        # that share the same hash address.
        self.singlyLinkedList = []


# class HashTable(object):
#     def __init__(self, length):
#         self.length = length
#         self.hash_table = [HeadNode() for i in range(self.length)]
#         self.iter_index = 0
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         raise StopIteration

        # if self.iter_index == self.length:
        #     self.iter_index = 0
        #     raise StopIteration
        # # get the keys and values with the same hash address.
        # keys_values_list = self.hash_table[self.iter_index].singlyLinkedList
        # self.iter_index = self.iter_index + 1
        # # self.tmp = self.hash_table[self.iter_index].singlyLinkedList
        # return keys_values_list


class Dictionary(object):
    def __init__(self):
        # length of hash table. It means that the hash address is in {0,1,2,3,4,5,6,7,8,9}
        self.length = 10
        self.hashTable = [HeadNode() for i in range(self.length)]
        # self.HashTable = HashTable(self.length)
        # self.hashTable = self.HashTable.hash_table
        self.iter_index = -1  # used for __next__

    # To convert the 'key' to hash address.
    # Return: the integer between 0 to 9.
    def hash_func(self, key):
        if type(key) in [list, dict, set, tuple] or (key is None):
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
    def add(self, key, value):
        [is_valid, message] = self.validation_check(key, value)
        if not is_valid:
            return "Fail. Invalid key or value"

        # If is_valid is True, the 'message' is hash_address
        head_node = self.hashTable[message]

        # Create a new node and assign values
        node_new = ChainNode()
        node_new.key = key
        node_new.values.append(value)

        # If there is no collision, enter
        if head_node.count == 0:
            # use the built-in list for storing new node and modify Statistical information
            head_node.singlyLinkedList.append(node_new)
            head_node.count = 1
            head_node.keys.append(key)
        else:
            # If there is no same key in the head_node.keys, enter
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

    # remove an element by key
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

    # Return the number of keys and values in the hash table
    def size(self):
        count_keys = 0  # store the number of different keys
        count_values = 0  # store the the number of different values
        for node in self.hashTable:
            count_values = count_values + node.count
            count_keys = count_keys + len(node.keys)
        return [count_keys, count_values]

    # Conversion from/to built-in list
    def to_list(self):
        keys = []
        values = []
        for head_node in self.hashTable:
            if head_node.count != 0:
                for node in head_node.singlyLinkedList:
                    keys.append(node.key)
                    keys.sort()
                    values.insert(keys.index(node.key), node.values)
        return [keys, values]

    def from_list(self, keys, values):
        if len(keys) != len(values):
            return "Fail. The length of key set and value set are not equal."

        for index in range(len(keys)):
            if type(values[index]) is list:
                tmp_list = values[index]
                for value in tmp_list:
                    self.add(keys[index], value)
            else:
                self.add(keys[index], values[index])

    # Find element by specific key
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
            keys_even.sort()  # It must be a separate line. Otherwise it will show a value of None
            return keys_even
        elif predicate == "odd_value":
            keys_odd.sort()
            return keys_odd

    # Map structure by specific function
    def map_my(self, func):
        for head_node in self.hashTable:
            for node in head_node.singlyLinkedList:
                value = node.values[0]
                node.values = [func(value)]

    # Reduce process structure elements to build a return value by specific functions
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
        # to traverse the hash table.
        for index in range(self.length):
            # if (self.hashTable[index].count != 0) and (dictionary.hashTable[index].count != 0):
            if dictionary.hashTable[index].count != 0:
                for node in dictionary.hashTable[index].singlyLinkedList:
                    if node.key not in self.hashTable[index].keys:
                        self.hashTable[index].singlyLinkedList.append(node)
                        self.hashTable[index].keys.append(node.key)
                        self.hashTable[index].count = self.hashTable[index].count + 1
            # elif (self.hashTable[index].count == 0) and (dictionary.hashTable[index].count != 0):
            #     self.hashTable[index].singlyLinkedList = dictionary.hashTable[index].singlyLinkedList

    def mempty(self):
        return Dictionary()


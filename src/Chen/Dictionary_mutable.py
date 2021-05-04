import logging
import functools

from TestUtils import *
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ChainNode:
    def __init__(self):
        """
        To initialize the variables used to store the key and value.
        """
        self.key = None
        # The dictionary support the different values with the same key.
        self.values = []


class HeadNode(object):
    def __init__(self):
        """
        To initialize a linked list structure used to handle hash conflicts and two variables for counting work.
        """
        # 'count' is to store the length of chain that the 'singlyLinkedList' refers to, the number of values, not keys
        self.count = 0
        # To store existing keys in the 'singlyLinkedList'
        self.keys = []
        # To deal with collision.
        self.singlyLinkedList = []


class Dictionary(object):
    def __init__(self):
        """
        To initialize the custom dictionary object.
        """
        # Length of hash table.
        self.length = 10
        self.hashTable = [HeadNode() for i in range(self.length)]

        # The following variables are used for implementing iterator.
        self.iter_head_node_index = 0
        self.iter_chain_node_index = -1
        self.iter_value_index = -1
        # To store values and key if there are multiple values.
        self.iter_values = None
        self.iter_key = None

    def __eq__(self, other):
        """
        To determine whether two custom dictionary objects contain the same keys and related values.
        :param other: Another custom dictionary object to compare
        :return: If the two objects' keys and corresponding values are exactly the same, return True;
        Otherwise, return False.
        """
        lst_1 = self.to_list()
        lst_2 = other.to_list()
        is_equal = True
        for index in range(len(lst_1)):
            if lst_1[index] != lst_2[index]:
                is_equal = False
                break
        return is_equal

    def get_hash_address(self, key):
        """
        To convert the 'key' to hash address.
        :param key: an valid element.
        :return: The hash address of the key.
        """
        # List and set are unhashable type. So transform the type into 'tuple' if needed.
        if type(key) is set:
            key = tuple(key)
        elif type(key) is list:
            key = tuple(key)
        return key.__hash__() % self.length

    def validate(self, key=None, value=None):
        """
        To check whether key and value are valid.
        :param key: The "key" which is needed to be validated.
        :param value: The value needed to be validated.
        :return: True, if key and value are valid; otherwise, False.
        """
        return self.validate_key(key) and self.validate_value(value)

    def validate_value(self, value=None):
        """
        To check whether 'value' is valid.
        :param value: The "value" which is needed to be validated.
        :return: True, if value is valid; otherwise, False.
        """
        if value is None:
            raise Exception
        return True

    def validate_key(self, key=None):
        """
        To check whether 'key' is valid.
        :param key: The "key" which is needed to be validated.
        :return:  True, if value is valid; otherwise, False.
        """
        if type(key) is dict:
            raise Exception
        if key is None:
            raise Exception
        # Numerical key object has no len(),
        # so explicitly specify which types are not allowed to use empty value as keys
        if (type(key) in [str, tuple, set, list]) and (len(key) == 0):
            raise Exception
        return True

    def add(self, key, value):
        """
        To add a new element by key and value without covering.
        :param key: The "key" in the new element.
        :param value: The "value" in the new element.
        :return: None
        """

        self.validate(key, value)
        hash_address = self.get_hash_address(key)
        head_node = self.hashTable[hash_address]

        # To uniform form of key
        if type(key) in [list, set]:
            key = tuple(key)
        # Create a new node and assign values.
        node_new = ChainNode()
        node_new.key = key
        node_new.values.append(value)

        # 'head_node.count == 0' means that there is no collision.
        if head_node.count == 0:
            head_node.singlyLinkedList.append(node_new)
            head_node.count = 1
            head_node.keys.append(key)
        else:
            # To deal with collision.
            if key not in head_node.keys:
                head_node.singlyLinkedList.append(node_new)
                head_node.keys.append(key)
                head_node.count = head_node.count + 1
            else:
                # For the same 'key', determine whether 'value' already exists. If not, then store.
                for index in range(len(head_node.singlyLinkedList)):
                    if key == head_node.singlyLinkedList[index].key:
                        if value not in head_node.singlyLinkedList[index].values:
                            head_node.singlyLinkedList[index].values.append(value)
                            head_node.count = head_node.count + 1
                        break
        logger.info("Successfully add a new element.")

    def exist_key(self, key):
        """
        To check whether the 'key' exist in the dictionary object.
        :param key: A key that needs to be checked for existence.
        :return: If exist, return the location
        """
        for head_node_index in range(self.length):
            if key in self.hashTable[head_node_index].keys:
                link_lst = self.hashTable[head_node_index].singlyLinkedList
                for chain_node_index in range(len(link_lst)):
                    if link_lst[chain_node_index].key == key:
                        return head_node_index, chain_node_index
        return -1, -1

    def set_value(self, key, new_value):
        """
        To add a new value with covering to a specific key.
        :param key: A 'key' which the 'new_value' belongs to.
        :param new_value: A new value .
        :return: None
        """
        self.validate(key, new_value)
        head_node_index, chain_node_index = self.exist_key(key)
        # "head_node_index is equal to -1" means that 'key' doesn't exist in dictionary object.
        if head_node_index == -1:
            self.add(key, new_value)
        else:
            self.hashTable[head_node_index].singlyLinkedList[chain_node_index].values = [new_value]

    def remove_value(self, key, value):
        """
        To delete a specific value (not values).
        :param key: the 'key' which the 'value' belonging to.
        :param value: The value which is needed to be deleted.
        :return:
        """
        self.validate(key, value)
        head_node_index, chain_node_index = self.exist_key(key)
        if head_node_index == -1:
            raise Exception
        if value not in self.hashTable[head_node_index].singlyLinkedList[chain_node_index].values:
            raise Exception
        if self.hashTable[head_node_index].count == 1:
            self.hashTable[head_node_index] = HeadNode()
        elif self.hashTable[head_node_index].count > 1:
            values_number = len(self.hashTable[head_node_index].singlyLinkedList[chain_node_index].values)
            if 1 == values_number:
                self.hashTable[head_node_index].count -= 1
                self.hashTable[head_node_index].singlyLinkedList.pop(chain_node_index)
            elif values_number > 1:
                self.hashTable[head_node_index].count -= 1
                self.hashTable[head_node_index].singlyLinkedList[chain_node_index].values.remove(value)
            else:
                raise Exception
        else:
            raise Exception

    # Delete all value belonging to a key
    def remove_key(self, key):
        """
        To remove an element by key.
        :param key: The "key" of the element which is to be removed.
        :return: None
        """
        self.validate_key(key)
        hash_address = self.get_hash_address(key)
        head_node = self.hashTable[hash_address]
        if key not in head_node.keys:
            raise Exception

        for index in range(len(head_node.singlyLinkedList)):
            if head_node.singlyLinkedList[index].key == key:
                head_node.count -= len(head_node.singlyLinkedList[index].values)
                head_node.keys.remove(key)
                head_node.singlyLinkedList.pop(index)
                break
        logger.info("Successfully remove the element.")

    def size(self):
        """
        To get the numbers of unique keys and values in the hash table.
        :return: a list with two numbers: the first is number of key, and the second is number of values.
        """
        count_keys = 0  # store the number of different 'key'.
        count_values = 0  # store the the number of different 'value'.
        for node in self.hashTable:
            count_values = count_values + node.count
            count_keys = count_keys + len(node.keys)
        return [count_keys, count_values]

    def compare_for_key(self, key_1, key_2):
        """
        To compare the two keys for order.
        :param key_1: A key.
        :param key_2: A key.
        :return: Return -1, If the hash value of key_1 is less than key_2;
                Return 1, if the hash value of key_1 is not less than key_2's.
        """
        if hash(key_1) < hash(key_2):
            return -1
        return 1

    def compare_for_list_key_value(self, item_1, item_2):
        """
        To compare 'key' first for order. If they are the same, compare 'values'.
        :param item_1: A tuple object like (key, values)
        :param item_2: A tuple object like (key, values)
        :return: Return -1, If the hash value of item_1 is less than item_2;
                 Return 1, if the hash value of item_1 is not less than item_2's.
        """
        # When one element is tuple and the other is another type, such as str,
        # using hash value can make the '<' operator function function normally.
        if hash(item_1[0]) != hash(item_2[0]):
            if hash(item_1[0]) < hash(item_2[0]):
                return -1
            return 1
        else:
            tmp_1 = item_1[1]
            tmp_2 = item_2[1]
            # 'values' could be list or set which don't have hash() function.
            if type(item_1[1]) in [list, set]:
                tmp_1 = tuple(item_1[1])
            if type(item_2[1]) in [list, set]:
                tmp_2 = tuple(item_2[1])
            if hash(tmp_1) < hash(tmp_2):
                return -1
            return 1

    def to_list(self):
        """
        To convert a self-defined dictionary object into list.
        :return: A list with key-value pairs.
        """
        if self.size() == [0, 0]:
            return []
        keys = []
        values = []
        for head_node in self.hashTable:
            if head_node.count != 0:
                for node in head_node.singlyLinkedList:
                    keys.append(node.key)
                    keys.sort(key=functools.cmp_to_key(self.compare_for_key))
                    values.insert(keys.index(node.key), node.values)
        result = []
        for index in range(0, len(keys)):
            for value in values[index]:
                result.append((keys[index], value))
        return sorted(result, key=functools.cmp_to_key(self.compare_for_list_key_value))

    def from_list(self, lst):
        """
        To use a list to build a self-defined dictionary objects.
        :param lst: A list with key-value pairs.
        :return: None
        """
        [key_size, value_size] = self.size()
        if key_size > 0:
            self.__init__()
        for element in lst:
            key = element[0]
            value = element[1]
            self.add(key, value)

    def get_by_key(self, key):
        """
        Find element by specific key.
        :param key: the unique element used to get key-value pair.
        :return: the "value" which is Corresponding to the "key".
        """

        self.validate_key(key)
        hash_address = self.get_hash_address(key)
        head_node = self.hashTable[hash_address]
        result = None
        if key in head_node.keys:
            for node in head_node.singlyLinkedList:
                if node.key == key:
                    result = node
                    break
        else:
            raise Exception
        # If there is only one value in the 'values', it is better to return a value, not a list.
        if len(result.values) == 1:
            return result.values[0]
        else:
            return result.values

    def filter(self, func):
        """
        To apply the function/operation defined by users to every item in the dictionary.
        :param func: the function defined by users.
        :return: A list that store the result of items after self-defined operation.
        """
        result = []
        it = iter(self)
        while True:
            try:
                key, value = next(it)
                pair = (key, value)
                tmp = func(pair)
                if not (tmp is None):
                    result.append(tmp)
            except StopIteration:
                break
        return result

    def map_my(self, func):
        """
        To map structure by specific function.
        :param func:  the function defined by users.
        :return: None
        """
        def list_func(lst):
            """
            To apply the function/operation defined by users to every item in the list.
            :param lst: A list object like [element1, [element2, element3], element4].
            :return:  A list that store the result of items after user-defined operation.
            """
            tmp = []
            for e in lst:
                if type(e) in [list, set, tuple]:
                    e = list(e)
                    tmp.append(list_func(e))
                else:
                    if type(e) in [int, float]:
                        tmp.append(func(e))
                    else:
                        raise Exception
            return tmp

        for head_node in self.hashTable:
            for node in head_node.singlyLinkedList:
                node.values = list_func(node.values)

    def reduce_my(self, func, key, initial_state):
        """
        To reduce process structure elements to build a return value by specific functions.
        :param func: The function defined by users.
        :param key: indicate which value-list will be the operated object.
        :param initial_state: A number.
        :return: A list that store the result of items after user-defined operation.
        """
        iterable = self.get_by_key(key)
        it = iter(iterable)
        value = initial_state
        for element in it:
            # Support the element with one-dimension list
            if type(element) is list:
                for e in element:
                    value = func(value, e)
            else:
                value = func(value, element)
        return value

    def __iter__(self):
        """
        To get a iterable object.
        :return: A custom dictionary object that contains the same keys and corresponding values.
        """
        dictionary = Dictionary()
        dictionary.from_list(self.to_list())
        return dictionary

    def __next__(self):
        """
        To get the next key-value item.
        :return: The next key-value item.
        """
        key = None
        value = None
        # To determine if it has encountered a situation where a key has multiple values.
        if (self.iter_values is not None) and (self.iter_value_index < len(self.iter_values) - 1):
            self.iter_value_index += 1
            key = self.iter_key
            value = self.iter_values[self.iter_value_index]
            return key, value
        else:
            self.iter_value_index = -1
            self.iter_values = None

        # To find next node if the nodes in the chain are all visited.
        def get_new_head_node_index(old_head_node_index):
            # '-1' means that there is no more new node not visited.
            new_head_index = -1
            if old_head_node_index < self.length - 1:
                for index in range(old_head_node_index + 1, self.length):
                    if len(self.hashTable[index].keys) > 0:
                        new_head_index = index
                        break
            return new_head_index

        head_node = self.hashTable[self.iter_head_node_index]
        # head_node.count > 0 means node existing.
        if len(head_node.keys) > 0:
            # There are nodes in the linked list is not accessed
            self.iter_chain_node_index += 1
            if len(head_node.keys) > self.iter_chain_node_index:
                keys_values_list = head_node.singlyLinkedList
                node = keys_values_list[self.iter_chain_node_index]
                key = node.key
                if len(node.values) == 1:
                    value = node.values[0]
                else:
                    self.iter_values = node.values
                    value = node.values[0]
                    self.iter_key = node.key
                    self.iter_value_index += 1

            # All nodes in the linked list have been accessed. The new node should be accessed.
            else:
                # Find the hash address of the next node.
                new_hash_address = get_new_head_node_index(self.iter_head_node_index)
                # Find a new node that has not been visited.
                if new_hash_address != -1:
                    # update the hash address and the node index.
                    self.iter_head_node_index = new_hash_address
                    self.iter_chain_node_index = 0
                    head_node = self.hashTable[new_hash_address]

                    keys_values_list = head_node.singlyLinkedList
                    node = keys_values_list[self.iter_chain_node_index]
                    key = node.key
                    if len(node.values) == 1:
                        value = node.values[0]
                    else:
                        self.iter_values = node.values
                        value = node.values[0]
                        self.iter_key = node.key
                        self.iter_value_index = 0
                # There are no new and accessible nodes.
                else:
                    raise StopIteration
        else:
            new_hash_address = get_new_head_node_index(self.iter_head_node_index)
            if new_hash_address != -1:
                self.iter_head_node_index = new_hash_address
                self.iter_chain_node_index = 0
                head_node = self.hashTable[new_hash_address]

                keys_values_list = head_node.singlyLinkedList
                node = keys_values_list[self.iter_chain_node_index]
                key = node.key
                if len(node.values) == 1:
                    value = node.values[0]
                else:
                    self.iter_values = node.values
                    value = node.values[0]
                    self.iter_key = node.key
                    self.iter_value_index = 0
            # There is no new and accessible node.
            else:
                raise StopIteration
        return key, value

    def mconcat(self, dictionary):
        """
        To concatenate two dictionary objects and self stores the result.
        :param dictionary: A dictionary object.
        :return: None
        """
        # to traverse the 'dictionary' and add the special nodes of 'dictionary' to self.
        for index in range(self.length):
            if dictionary.hashTable[index].count != 0:
                for node in dictionary.hashTable[index].singlyLinkedList:
                    if node.key not in self.hashTable[index].keys:
                        self.hashTable[index].singlyLinkedList.append(node)
                        self.hashTable[index].keys.append(node.key)
                        self.hashTable[index].count = self.hashTable[index].count + 1
                    else:
                        for element in node.values:
                            if element not in [self.get_by_key(node.key)]:
                                self.add(node.key, element)

    def mempty(self):
        """
        To return an mempty element in the dictionary object set.
        :return: A custom dictionary object.
        """
        return Dictionary()


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
        self.key = None
        self.value = None
        # 'next' refers to another ChainNode
        # 或许这个变量的设置是多余的
        self.next = None


# HeadNodes consist of a hash table.
class HeadNode(object):
    def __init__(self):
        # 'count' is to store the length of chain that the 'SinglyLinkedList' refers to
        self.count = 0
        # to store existing keys in the linked list
        self.keys = []
        # 'SinglyLinkedList' refers to a Singly Linked List which store the pairs of (key,value)
        # that share the same hash address.
        self.SinglyLinkedList = []


class Dictionary:

    def __init__(self):
        # length of hash table. It means that the hash address is in {0,1,2,3,4,5,6,7,8,9}
        self.length = 10
        self.hashTable = [HeadNode() for i in range(self.length)]

    # to convert the 'key' to hash address
    def hash_func(self, key):
        if type(key) in [list, dict, set, tuple] or (key is None):
            return -1  # '-1' means that the key is invalid
        return key.__hash__()

    # add a new element by key
    def add(self, key, value):
        hash_address = self.hash_func(key)
        if hash_address == -1:
            return "invalid key"
        head_node = self.hashTable[hash_address]

        # Create a new node and assign values
        node_new = ChainNode()
        node_new.key = key
        node_new.value = value
        node_new.next = None  # 或许这是多余的

        # If there is no collision, enter
        if head_node.count == 0:
            # use the built-in list for storing new node and modify Statistical information
            head_node.SinglyLinkedList.append(node_new)
            head_node.count = 1
            head_node.keys.append(key)
        else:
            # If there is no same key in the head_node.keys, enter
            if key not in head_node.keys:
                head_node.SinglyLinkedList.append(node_new)
                head_node.keys.append(key)
                head_node.count = head_node.count + 1
        return "Successfully store"

    # remove an element by value


    # Size, member, reverse (if applicable), intersection

    # Conversion from/to built-in list (you should avoid of usage these function into your library)



    # Find element by specific predicate (lst.find(is_even), find(lst, is_even))

    # Filter data structure by specific predicate (lst.filter(is_even), filter(lst, is_even))

    # Map (link) structure by specific function (lst.map(increment), map(lst, increment))

    # Reduce (link)– process structure elements to build a return value by specific functions (lst.reduce(sum),
    # reduce(lst, sum))


    # Data structure should be an iterator (link)
    # – for the mutable version in Python style [10, Chapter 7. Classes & Iterators]ho


    # Data structure should be a monoid and implement mempty and mconcat.


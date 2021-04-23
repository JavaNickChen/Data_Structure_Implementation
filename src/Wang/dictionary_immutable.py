import copy


class Hashdic:
    def __init__(self, Hashcode=1024):
        """

        :param Hashcode: max len of hashset
        """
        self.code = Hashcode
        self.key = [-1 for i in range(self.code)]
        self.value = [-1 for i in range(self.code)]
        self.size = 0

    def __eq__(self, other):
        """

        :param other:another object
        :return: True if equal to another object, False if not
        """
        if other is None:
            return False
        for x in range(0, len(self.key)):
            if self.key[x] == -1:
                if self.key[x] != other.key[x]:
                    return False
                if self.value[x] != other.value[x]:
                    return False
            else:
                if self.key[x][0] != other.key[x][0]:
                    return False
                if self.value[x][0] != other.value[x][0]:
                    return False
        return True

    def __iter__(self):
        return Hashdic_Iterator(self.key, self.value)


class Hashdic_Iterator:

    def __init__(self, key, value):
        self.index = 0
        self.iterator_list = []
        for i in range(0, len(key)):
            if key[i] == -1:
                continue
            temp = key[i]
            tempv = value[i]
            self.iterator_list.append([temp[0], tempv[0]])
            while temp[1] != -1:
                temp = temp[1]
                tempv = tempv[1]
                self.iterator_list.append([temp[0], tempv[0]])

    def __next__(self):
        try:
            temp = self.iterator_list[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return temp

    def __iter__(self):
        return self


def cons(Hd, key, value):
    """
    cons function provides a way to add element to dictionary
    :param Hd: a dictionary
    :param key: key added to dictionary
    :param value: value added to dictionary
    :return:a dictionary with a Key-value pair added in
    """
    new = Hashdic()
    new.size = Hd.size
    if key is None:
        raise Exception("key cant be NULL")
        return -1
    k = key.__hash__() % new.code
    for x in range(0, len(Hd.key)):
        new.key[x] = Hd.key[x]
        new.value[x] = Hd.value[x]
    if new.key[k] == -1:
        new.key[k] = [key, -1]
        new.value[k] = [value, -1]
        new.size += 1
    else:
        temp = new.key[k]
        tempv = new.value[k]
        if temp[0] == key:
            tempv[0] = value
        else:
            while temp[1] != -1:

                temp = temp[1]
                tempv = tempv[1]
                if temp[0] == key:
                    tempv[0] = value
                    break
            temp[1] = [key, -1]
            tempv[1] = [value, -1]
            new.size += 1
    return new


def remove(Hd, key):
    """
    remove a key from a dictionary
    :param Hd: dictionary
    :param key: removed key
    :return: a dictionary with a Key-value pair removed
    """
    if key is None:
        raise Exception("key cant be NULL")
    new = Hashdic()
    new.size = Hd.size
    k = int(key) % new.code
    for x in range(0, len(Hd.key)):
        new.key[x] = Hd.key[x]
        new.value[x] = Hd.value[x]
    if new.key[k] == -1:
        raise Exception("no such key")
    else:
        temp = new.key[k]
        tempv = new.value[k]
        if temp[0] == key:
            new.key[k] = -1
            new.value[k] = -1
            new.size -= 1
        else:
            while temp[1] != -1:

                btemp = temp[1]
                btempv = tempv[1]
                if btemp[0] == key:
                    temp[1] = btemp[1]
                    tempv[1] = btempv[1]
                    new.size -= 1
                    break
                else:
                    temp = btemp
                    tempv = btempv
    return new


def size(Hd):
    """
    return the size of dictionary
    :param Hd:  dictionary
    :return: Hd.size
    """
    if Hd:
        return Hd.size
    else:
        return -1


def to_list(h):
    """
    Convert a dictionary to a list
    :param h: dictionary
    :return:  a list
    """
    outlist = []
    if not h:
        return outlist
    for i in range(0, len(h.key)):
        if h.key[i] == -1:
            continue
        else:
            temp = h.key[i]
            tempv = h.value[i]
            outlist.append([temp[0], tempv[0]])
            while temp[1] != -1:
                temp = temp[1]
                tempv = tempv[1]
                outlist.append([temp[0], tempv[0]])
    return outlist


def from_list(list):
    """
    Create a dictionary from a list
    :param list: a list contains some key-value pairs
    :return: dictionary contains those key-value pairs
    """
    p = Hashdic()
    for st in list:
        if not len(st) == 2:
            raise Exception(
                "Element with more than 2 elements in the list are not allow")
        p = cons(p, st[0], st[1])
    return p


def find(mp, key):
    """
    find a key-value pair by key
    :param mp: dictionary
    :param key:  key
    :return: -1 if can't find the key,[key,value] if find the key
    """
    if not key:
        return -1
    fin = key % mp.code
    find = 0
    if mp.key[fin] == -1:
        print("no such value")
        return -1
    else:
        temp = mp.key[fin]
        tempv = mp.value[fin]
        if temp[0] == key:
            return [temp[0], tempv[0]]
        while temp[1] != -1:
            temp = temp[1]
            tempv = tempv[1]
            if temp[0] == key:
                return [temp[0], tempv[0]]
    print("no such value")
    return -1


def mempty(h):
    """
    clear a dictionary
    :param h: dictionary needed to be cleared
    :return: a empty dictionary
    """
    return Hashdic()


def mconcat(a, b):
    """
    Combine two dictionaries
    :param a: a dictionary
    :param b: a dictionary
    :return: A dictionary formed by combining two dictionaries
    """
    if not a and not b:
        return None
    new = Hashdic()
    if not a:
        new.size = b.size
        for x in range(0, len(b.key)):
            new.key[x] = b.key[x]
            new.value[x] = b.value[x]
        return new
    elif not b:
        new.size = a.size
        for x in range(0, len(a.key)):
            new.key[x] = a.key[x]
            new.value[x] = a.value[x]
        return new
    else:
        list = to_list(b)
        for st in list:
            a = cons(a, st[0], st[1])
        return a


def iterator(hp):
    """
    a iterator of dictionary
    :param hp: dictionary
    :return: Iterator of a dictionary   use fun() to get the next key-value pair
    """
    iterator_list = []
    for i in range(0, len(hp.key)):
        if hp.key[i] == -1:
            continue
        else:
            temp = hp.key[i]
            tempv = hp.value[i]
            iterator_list.append([temp[0], tempv[0]])
            while temp[1] != -1:
                temp = temp[1]
                tempv = tempv[1]
                iterator_list.append([temp[0], tempv[0]])
    na = 0

    def next():
        nonlocal na
        t = na
        na = na + 1
        if t >= len(iterator_list):
            return -1
        return iterator_list[t]
    return next


def map(a, f):
    """
    map() will map the specified sequence according to the provided function.
    :param a: dictionary
    :param f: function
    :return: a new dictionary
    """
    new = Hashdic()
    new.size = a.size
    for x in range(0, len(a.key)):
        new.key[x] = a.key[x]
        new.value[x] = a.value[x]

    for i in range(0, len(new.key)):
        if new.key[i] == -1:
            continue
        else:
            temp = new.key[i]
            tempv = new.value[i]
            tempv[0] = f(tempv[0])
            while temp[1] != -1:
                temp = temp[1]
                tempv = tempv[1]
                tempv[0] = f(tempv[0])
    return new


def reduce(a, f, state):
    """
    The reduce() function accumulates the elements in the parameter sequence.
    :param a: a dictionary
    :param f: a function
    :param state: the input state
    :return: output state
    """
    instate = state
    for i in range(0, len(a.key)):
        if a.key[i] == -1:
            continue
        else:
            temp = a.key[i]
            tempv = a.value[i]
            instate = f(tempv[0], instate)
            while temp[1] != -1:
                temp = temp[1]
                tempv = tempv[1]
                tempv[0] = f(tempv[0])
                instate = f(tempv[0], instate)
    return instate


def filter(a, f):
    """
    The filter() function is used to filter the sequence, filter out the elements that do not
    meet the conditions,and return a new list of elements that meet the conditions.
    :param a: a dictionary
    :param f: function uesd to filter
    :return: a list of result
    """
    result = []
    for i in range(0, len(a.key)):
        if a.key[i] == -1:
            continue
        else:
            temp = a.key[i]
            tempv = a.value[i]
            if f(tempv[0]):
                result.append([temp[0], tempv[0]])

            while temp[1] != -1:
                temp = temp[1]
                tempv = tempv[1]
                if f(tempv[0]):
                    result.append([temp[0], tempv[0]])
    return result


def is_even(a):
    return a % 2 == 0

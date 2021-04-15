from Dictionary_mutable import Dictionary
import functools


# To process the test data as Dictionary() object does.
def lst_validate(lst):
    """
        To pick out invalid 'key' or 'value',and then remove them.
        And also, remove the duplicate key-value and remain only one.
    :param lst: a list object such as [(key_1, value_1), ..., (key_n, value_n)]
    :return: lst itself.
    """
    dictionary = Dictionary()
    indexes = []
    for index in range(len(lst)):
        if not dictionary.validate(lst[index][0], lst[index][1]):
            indexes.append(index)
    indexes.reverse()
    for index in indexes:
        lst.pop(index)
    return list(set(lst))


def sort(lst):
    """
        To sort the list object.
    :param lst: a list object such as [(key_1, value_1), ..., (key_n, value_n)]
    :return: a sorted list object.
    """
    dictionary = Dictionary()
    return sorted(lst, key=functools.cmp_to_key(dictionary.compare_for_list_key_value))


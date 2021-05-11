from Dictionary_mutable import Dictionary
import functools
from typing import List, Tuple, TypeVar

keyType = TypeVar("keyType", int, str, float, tuple, set, list)
valueType = TypeVar("valueType", int, str, float, bool, tuple, set, list, dict)

# Define the following functions for processing the test data as Dictionary() object does.


def lst_validate(lst: List[Tuple[keyType, valueType]]) -> List[Tuple[keyType, valueType]]:
    """
    To pick out invalid 'key' or 'value',and then remove them.
    And also, remove the duplicate key-value and remain only one.
    :param lst: a list object such as [(key_1, value_1), ..., (key_n, value_n)]
    :return: A legal list.
    """
    dictionary = Dictionary()
    indexes = []
    for index in range(len(lst)):
        try:
            if type(lst[index][0]) in [set, list]:
                lst[index][0] = tuple(lst[index][0])
            dictionary.validate(lst[index][0], lst[index][1])
        except Exception:
            indexes.append(index)
    indexes.reverse()
    for index in indexes:
        lst.pop(index)
    return list(set(lst))


def sort(lst: List[Tuple[keyType, valueType]]) -> List[Tuple[keyType, valueType]]:
    """
    To sort the list object.
    :param lst: a list object such as [(key_1, value_1), ..., (key_n, value_n)]
    :return: a sorted list object.
    """
    dictionary = Dictionary()
    return sorted(lst, key=functools.cmp_to_key(dictionary.compare_for_list_key_value))






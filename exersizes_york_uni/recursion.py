import re
def ispalindrome(word):
    """
    Recursively checks if a given string is a palindrome, ignoring punctuation and case.

    Args:
        word (str): The string to check.

    Returns:
        bool: True if the input is a palindrome, False otherwise.

    Raises:
        TypeError: If the input is not a string.
    """
    if not isinstance(word, str):
        raise TypeError("Input must be a string")

    # Clean only once: remove non-alphanumeric characters and lowercase it
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', word).lower()

    def helper(w):
        if len(w) <= 1:
            return True
        return w[0] == w[-1] and helper(w[1:-1])

    return helper(cleaned)



def rec_sum(numbers):
    """
    Recursively calculates the sum of a list of integers.

    Args:
        numbers (list): A list of integers.

    Returns:
        int: The sum of all integers in the list.

    Raises:
        TypeError: If the input is not a list of integers.

    Example:
        >>> rec_sum([1, 2, 3])
        6
        >>> rec_sum([])
        0
    """
    if not isinstance(numbers, list) or not all(isinstance(n, int) for n in numbers):
        raise TypeError("Input must be a list of integers")
    if len(numbers) == 0:
        return 0
    sum = numbers[0]
    sum += rec_sum(numbers[1:])
    return sum


def sum_digits(number):
    """
    Recursively calculates the sum of the digits of an integer.

    Args:
        number (int): A non-negative integer.

    Returns:
        int: The sum of the digits of the input number.

    Raises:
        ValueError: If the input is not an integer.

    Example:
        >>> sum_digits(123)
        6
        >>> sum_digits(0)
        0
    """
    if not isinstance(number, int):
        raise ValueError("Input must be an integer.")
    if number < 0:
        raise ValueError("Input must be a non-negative integer.")
    if number ==  0:
        return 0
    summ = number % 10
    summ += sum_digits(number//10)    
    return summ


def flatten(mlist):
    """
    Recursively flattens a nested list into a single-level list.

    Args:
        mlist (list): A (possibly nested) list of elements.

    Returns:
        list: A flat list containing all the elements from the nested list.

    Raises:
        TypeError: If the input is not a list.
    """
    if not isinstance(mlist, list):
        raise TypeError("Input must be a list")
    if len(mlist) == 0:
        return []
    result = []
    if isinstance(mlist[0], list):
        result.extend(flatten(mlist[0]))
    else:
        result.append(mlist[0])
    result.extend(flatten(mlist[1:]))
    return result


# Tests for flatten
assert flatten([1, 2, 3]) == [1, 2, 3], "Test 1 Failed"
assert flatten([1, [2, 3], [4, [5]]]) == [1, 2, 3, 4, 5], "Test 2 Failed"
assert flatten([[[[1]]], 2, [[3, [4]]]]) == [1, 2, 3, 4], "Test 3 Failed"
assert flatten([]) == [], "Test 4 Failed"
assert flatten([[], [[], []], [[[]]]]) == [], "Test 5 Failed"
try:
    flatten("not a list")
except TypeError:
    pass
else:
    raise AssertionError("Test 6 Failed")


def merge(sorted_listA, sorted_listB):
    """
    Recursively merges two sorted lists into a single sorted list.

    Args:
        sorted_listA (list): First sorted list.
        sorted_listB (list): Second sorted list.

    Returns:
        list: A new sorted list containing all elements from both input lists.
    """
    if not sorted_listA:
        return sorted_listB
    if not sorted_listB:
        return sorted_listA
    if sorted_listA[0] <= sorted_listB[0]:
        return [sorted_listA[0]] + merge(sorted_listA[1:], sorted_listB)
    else:
        return [sorted_listB[0]] + merge(sorted_listA, sorted_listB[1:])


# Tests for merge
assert merge([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6], "Test 1 Failed"
assert merge([], [1, 2, 3]) == [1, 2, 3], "Test 2 Failed"
assert merge([], []) == [], "Test 3 Failed"
assert merge([1, 2], [3, 4]) == [1, 2, 3, 4], "Test 4 Failed"
assert merge([1, 3, 5], [1, 3, 5]) == [1, 1, 3, 3, 5, 5], "Test 5 Failed"
assert merge([-3, -1, 2], [-2, 0, 3]) == [-3, -2, -1, 0, 2, 3], "Test 6 Failed"


def something_ish(pattern, word):
    """
    Generalized predicate that checks whether all characters in pattern exist in word.

    Args:
        pattern (str): The characters to check for.
        word (str): The string in which to search.

    Returns:
        bool: True if all characters in pattern are in word, otherwise False.

    Raises:
        TypeError: If inputs are not strings.
    """
    def helper(w, p):
        if not p:
            return True
        if not w:
            return False
        if p[0] in w:
            return helper(w.replace(p[0], '', 1), p[1:])
        return False

    if not isinstance(pattern, str) or not isinstance(word, str):
        raise TypeError("Both inputs must be strings")

    return helper(word.lower(), pattern.lower())


def iselfish(word):
    """
    Checks whether a word is 'elfish'—i.e., contains the letters 'e', 'l', and 'f'.

    Args:
        word (str): The input string to check.

    Returns:
        bool: True if the word contains 'e', 'l', and 'f'; False otherwise.
    """
    return something_ish('elf', word)


# Tests for iselfish and something_ish
assert iselfish("waffle") == True, "Test 1 Failed"
assert iselfish("hello") == False, "Test 2 Failed"
assert iselfish("ELFISH") == True, "Test 3 Failed"
assert iselfish("elf") == True, "Test 4 Failed"
assert iselfish("el") == False, "Test 5 Failed"
try:
    iselfish(123)
except TypeError:
    pass
else:
    raise AssertionError("Test 6 Failed")

# Exersize 1
def order_price(quantity):
    """
    Calculate total price in pence for a banana order.
    
    Parameters:
    quantity (int): Number of kilograms of bananas
    
    Returns:
    int: Total price in pence
    """
    if not isinstance(quantity, (int, float)):
        raise TypeError("Quantity must be a number (int or float).")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    
    price_per_item = 3.00
    postage = 4.99
    total = quantity * price_per_item + postage
    if total > 50.00:
        total -= 1.50
    return int(round(total * 100))


#Test cases for the order_price function
# Basic functionality
assert order_price(1) == 799     # 3.00 + 4.99 = 7.99 → 799 pence
assert order_price(10) == 3499   # 30.00 + 4.99 = 34.99 → 3499 pence
assert order_price(17) == 5449  # 51.00 + 4.99 - 1.50 = 54.49 → 5449 pence

# Test for floating point quantity
assert order_price(2.5) == 1249  # 7.5 + 4.99 = 12.49 → 1249 pence

# Test exact threshold
assert order_price(16.67) == 5350 # 50.01 + 4.99 - 1.50 = 53.50 → 5350 pence

# Test with no discount applied
assert order_price(15) == 4999  # No discount applied

# Test just below the threshold 
assert order_price(16.66) == 5347 # 49.98 + 4.99 = 54.97 → 5347 pence

# Edge case: minimum quantity
assert order_price(0.01) == 502   # 0.03 + 4.99 = 5.02 → 502 pence

# Invalid inputs (you'd test these only if you included type checks)
try:
    order_price("five")
except TypeError:
    pass
else:
    assert False, "Expected TypeError for string input"

try:
    order_price(-1)
except ValueError:
    pass
else:
    assert False, "Expected ValueError for negative input"
    

# Exersize 2

def maximum_heart_rate(age):
    """
    Calculates the estimated maximum heart rate for a given age using the formula: 208 - 0.7 × age.

    Args:
        age (int): The person's age in years. Must be a positive integer.

    Returns:
        float: The estimated maximum heart rate.

    Raises:
        ValueError: If age is not a positive integer.
    """
    if not isinstance(age, int) or age <= 0:
        raise ValueError("Age must be a positive integer.")
    
    return 208 - 0.7 * age


def training_zone(age, rate):
    """
    Determines the training zone based on a person's age and current heart rate.

    This function calculates the person's maximum heart rate using the
    `maximum_heart_rate(age)` function, then computes the percentage of
    the max rate that the current heart rate represents. Based on this
    percentage, it returns a string describing the training zone:

    - 90% and above: "Interval training"
    - 70% to 89.9%: "Threshold training"
    - 50% to 69.9%: "Aerobic training"
    - Below 50%: "Couch potato"

    Parameters:
    age (int): The person's age.
    rate (int or float): The person's current heart rate.

    Returns:
    str: A label representing the training zone.
    """
    max_rate = maximum_heart_rate(age)
    percentage = rate / max_rate
    zones = [
        (0.9, 'Interval training'),
        (0.7, 'Threshold training'),
        (0.5, 'Aerobic training'),
        (0.0, 'Couch potato')
    ]
    return next(label for boundary, label in zones if percentage >= boundary)

# Exersize 3

def is_valid_password(password, min_length=8, has_upper=True, has_lower=True, has_numeric=True):
    """
    Validate a password based on given criteria.

    Args:
        password (str): Password to validate
        min_length (int): Minimum length of the password
        has_upper (bool): Require at least one uppercase letter
        has_lower (bool): Require at least one lowercase letter
        has_numeric (bool): Require at least one digit

    Returns:
        bool: True if the password is valid, False otherwise
    """
    checks = [
        len(password) >= min_length,
        not has_upper or any(c.isupper() for c in password),
        not has_lower or any(c.islower() for c in password),
        not has_numeric or any(c.isdigit() for c in password)
    ]
    return all(checks)

# Test cases for is_valid_password function
assert is_valid_password("Password123", 8, True, True, True) == True        # Valid password    
assert is_valid_password("password123", 8, True, True, True) == False       # Missing uppercase
assert is_valid_password("PASSWORD123", 8, True, True, True) == False       # Missing lowercase
assert is_valid_password("Password", 8, True, True, True) == False       # Missing numeric
assert is_valid_password("Pass123", 8, True, True, True) == False       # Too short
assert is_valid_password("Valid1", 6, True, True, True) == True        # Valid password with minimum length
assert is_valid_password("ValidPassword", 8, True, True, False) == True  # Valid without numeric
assert is_valid_password("Valid123", 8, True, False, True) == True  # Valid without lowercase
assert is_valid_password("Valid123", 8, False, True, True) == True  # Valid without uppercase       

# Exersize 4

def sum_digits(number):
    """
    Calculates the sum of the digits of a whole number.

    Args:
        number (int): The whole number whose digits are to be summed.

    Returns:
        int: The sum of the digits.

    Raises:
        ValueError: If the input is not an integer.
    """
    if not isinstance(number, int):
        raise ValueError("Input must be an integer.")
    
    return sum(int(dig) for dig in str(number))


def sum_digits_challenge(number):
    """
    Calculate the sum of the digits of a number without converting it to a string.

    Args:
        number (int): A whole number (non-negative integer).

    Returns:
        int: The sum of the digits of the number.
    
    Raises:
        ValueError: If the input is not a non-negative integer.
    """
    if not isinstance(number, int):
        raise ValueError("Input must be an integer.")
    total = 0
    while number:
        total += number % 10
        number //= 10
    return total
        
        
# Exersize 5

def pairwise_digits(number_a, number_b):
    """
    Compares digits at corresponding positions in two whole numbers and returns a binary result.

    Pads the shorter number with '0's on the right to match the length of the longer one.
    Each digit is compared pairwise:
    - '1' if digits match
    - '0' if digits differ

    The binary string is then returned as an integer.

    Args:
        number_a (str or int): The first whole number to compare.
        number_b (str or int): The second whole number to compare.

    Returns:
        int: An integer representing the binary result of digit comparisons.
    """
    num_a, num_b = str(number_a), str(number_b)
    max_len = max(len(num_a), len(num_b))
    num_a,num_b  = num_a.ljust(max_len, '0'), num_b.ljust(max_len, '0')
    return (''.join('1' if a == b else '0' for a, b in zip(num_a, num_b)))


assert pairwise_digits(123, 123) == '111'
assert pairwise_digits(123, 456) == '000'
assert pairwise_digits(123, 12) == '110'
assert pairwise_digits(123, 1234) == '1110'
assert pairwise_digits(123, 12345) == '11100'
assert pairwise_digits(12345, 123) == '11100'
assert pairwise_digits(123, 123456) == '111000'
assert pairwise_digits(123456, 123) == '111000'


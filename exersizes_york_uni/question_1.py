def extract_text(text, keys):
    
    """Extracts words from a given text that contain only letters from a specified subset of keys.

    This function is case-insensitive and preserves the original casing of the words.
    It ensures that:
    - Each word in the output is separated by a single space.
    - The output does not start or end with a space.
    - Only words made up entirely of letters in `keys` are included.

    Args:
        text (str): The input string containing only alphabetic characters and spaces.
        keys (str): A non-empty string of allowed characters.

    Returns:
        str: A string with valid words separated by a single space, or an empty string if no words match.
    """

    #if the parameter text is an empty string, the function returns an empty string
    if not text:
        return ""
    keys = set(keys.lower())  # Convert keys to a set for faster lookup and make it case insensitive
    words = text.split()  # Split the text into words
    filtered = [ word for word in words if all(char in keys for char in word.lower())]  # List to hold the filtered words    
    return ' '.join(filtered) #returned string is separated by a single blank space
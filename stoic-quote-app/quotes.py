from all_meditations_quotes import quotes

def get_quote(index=0):
    """
    Returns the quote at the given index.
    Loops back if index is out of range.
    """
    if index >= len(quotes):
        index = 0
    elif index < 0:
        index = len(quotes) - 1
    return quotes[index]
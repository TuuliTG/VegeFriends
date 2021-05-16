def is_valid(object : str, min_length, max_length):
    print("security")
    object = object.strip()
    if len(object) < min_length or len(object) > max_length:
        return False
    return True
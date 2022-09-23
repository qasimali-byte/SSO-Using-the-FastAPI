def get_item(collection, key, target):
    return next((item for item in collection if item.get(key, None) == target), None)
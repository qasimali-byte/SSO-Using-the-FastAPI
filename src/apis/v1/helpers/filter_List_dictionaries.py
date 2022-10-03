def get_item(collection, key, target):
    return next((item for item in collection if item.get(key, None) == target), None)

def reduce_list_dictionaries(collection, key, target):
    return [item for item in collection if item.get(key, None) == target]


def reduce_list_products(collection, key, target):
    return [item.get("id") for item in collection if item.get(key, None) == target]
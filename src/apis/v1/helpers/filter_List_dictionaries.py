def get_item(collection, key, target):
    return next((item for item in collection if item.get(key, None) == target), None)

def reduce_list_dictionaries(collection, key, target):
    return [item for item in collection if item.get(key, None) == target]


def reduce_list_products(collection, key, target):
    return [dict({"id":item.get("id"),"name":item.get("display_name"),"logo":item.get("logo_url")}) for item in collection if item.get(key, None) == target]
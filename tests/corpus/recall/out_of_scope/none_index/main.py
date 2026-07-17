def lookup(items, index, optional):
    return items[index] if optional is None else optional.name

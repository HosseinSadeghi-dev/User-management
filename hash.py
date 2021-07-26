import basehash


class Hash:

    def __init__(self):
        self.__hash_fn = basehash.base94()

    def __encrypt__(self, value):
        return self.__hash_fn.hash(value)

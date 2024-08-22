import math

from bitarray import bitarray


class BloomFilter(object):

    def __init__(self, size, number_expected_elements=100000):
        self.size = size
        self.number_expected_elements = number_expected_elements

        self.bloom_filter = bitarray(self.size)
        self.bloom_filter.setall(0)

        self.number_hash_functions = round(
            (self.size / self.number_expected_elements) * math.log(2)
        )

    def _hash_djb2(self, s):
        _hash = 5381
        for x in s:
            _hash = ((_hash << 5) + _hash) + ord(x)
        return _hash % self.size


    def _hash(self, item, x):
        return self._hash_djb2(str(x) + item)


    def add_to_filter(self, item):
        for i in range(self.number_hash_functions):
            self.bloom_filter[self._hash(item, i)] = 1


    def check(self, item):
        return all(
            self.bloom_filter[self._hash(item, i)]
            for i in range(self.number_hash_functions)
        )


    def check_is_not_in_filter(self, item):
        for i in range(self.number_hash_functions):
            if self.bloom_filter[self._hash(item, i)] == 0:
                return True

        return False



if __name__ == "__main__":
    bloom = BloomFilter(size=1000_000, number_expected_elements=100000)

    bloom.add_to_filter("cat")
    bloom.add_to_filter("dog")

    print(bloom.check("cat"))  # True
    print(bloom.check("dog"))  # True
    print(bloom.check("fish"))  # False
    print(bloom.check_is_not_in_filter("bird"))  # True

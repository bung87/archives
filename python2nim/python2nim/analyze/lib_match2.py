from simhash import Simhash, SimhashIndex
from store_index import py_std_index, nim_std_index
from collections import defaultdict
import re

stop_words = set(["This", "module", "implements",
                  "a", "the", "an", "support", "and"])


def get_hash(content):
    hash = Simhash(content)
    return hash


def process_line(p):
    result = []
    with open(p) as f:
        for x in f:
            line = x.strip()
            it = line.split()
            uni = [x for i, x in enumerate(it) if it.index(x) == i]
            filterd = [x for x in uni if x not in stop_words]
            hash = get_hash(filterd)
            result.append((it[0], hash))
    return result


def main():

    py_set = process_line(py_std_index)
    nim_set = process_line(nim_std_index)
    # final_set = py_set + nim_set
    index = SimhashIndex(py_set, k=10)
    # for key, hash in py_set:
    #     try:
    #         lsh.insert("py_"+key, hash)
    #     except:
    #         pass

    # for key, hash in nim_set:
    #     try:
    #         lsh.insert("nim_"+key, hash)
    #     except:
    #         pass

    result = defaultdict(list)
    for key, hash in nim_set:
        r = index.get_near_dups(hash)
        result[key] = r

    print(result)


if __name__ == "__main__":
    main()

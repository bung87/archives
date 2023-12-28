from datasketch import MinHash, MinHashLSH

from store_index import py_std_index, nim_std_index
from collections import defaultdict

num_perm = 128


stop_words = set(["this", "module", "implements",
                  "a", "the", "an", "support", "and"])


def it2hash(seq):
    hash = MinHash(num_perm=num_perm)
    for x in set(seq):
        hash.update(x.encode())
    return hash


def process_line(p):
    result = []
    with open(p) as f:
        for x in f:
            line = x.strip().lower()
            it = line.split()
            uni = [x for i, x in enumerate(it) if it.index(x) == i]
            filterd = [x for x in uni if x not in stop_words]
            hash = it2hash(filterd)
            result.append((it[0], hash))
    return result


def main():
    lsh = MinHashLSH(threshold=0.3, num_perm=num_perm)
    py_set = process_line(py_std_index)
    nim_set = process_line(nim_std_index)
    final_set = py_set + nim_set

    for key, hash in py_set:
        try:
            lsh.insert("py_"+key, hash)
        except:
            pass

    # for key, hash in nim_set:
    #     try:
    #         lsh.insert("nim_"+key, hash)
    #     except:
    #         pass

    result = defaultdict(list)
    for key, hash in nim_set:
        r = lsh.query(hash)
        result[key] = r

    print(result)


if __name__ == "__main__":
    main()


def _combine_dict(key, val):
    def f(acc, cur):
        src = cur[key]
        out = cur[val]
        if src not in acc:
            acc[src] = set()
        acc[src].add(out)
        return acc
    return f

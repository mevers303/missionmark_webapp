# Sam Cohan
# https://stackoverflow.com/a/43419027

import pickle
import globals as g


class BigFile(object):

    def __init__(self, f):
        self.f = f

    def __getattr__(self, item):
        return getattr(self.f, item)

    def read(self, n):
        # print("reading total_bytes=%s" % n, flush=True)
        if n >= (1 << 31):
            buffer = bytearray(n)
            idx = 0
            while idx < n:
                batch_size = min(n - idx, 1 << 31 - 1)
                # print("reading bytes [%s,%s)..." % (idx, idx + batch_size), end="", flush=True)
                buffer[idx:idx + batch_size] = self.f.read(batch_size)
                # print("done.", flush=True)
                idx += batch_size
            return buffer
        return self.f.read(n)

    def write(self, buffer):
        n = len(buffer)
        g.debug(f" -> Writing {n} total bytes...", 3)
        idx = 0
        while idx < n:
            batch_size = min(n - idx, 1 << 31 - 1)
            g.debug(f" ---> Writing bytes [{idx}, {idx + batch_size})... ", 3)
            self.f.write(buffer[idx:idx + batch_size])
            g.debug(f" ---> Done", 3)
            idx += batch_size


def pickle_dump(obj, file_path):
    g.debug(f"Caching {file_path}...")
    with open(file_path, "wb") as f:
        result = pickle.dump(obj, BigFile(f), protocol=pickle.HIGHEST_PROTOCOL)
    g.debug(" -> Done", 1)
    return result


def pickle_load(file_path):
    g.debug(f"Loading {file_path} from cache...")
    with open(file_path, "rb") as f:
        obj = pickle.load(BigFile(f))
    g.debug(" -> Done", 1)
    return obj

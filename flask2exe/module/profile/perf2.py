from line_profiler import LineProfiler

LEN = 10000

# ひどいコード
def hoge():
    a = []
    for i in range(LEN):
        a.append(i * i)
        a.append(i * i)
        a.append(i * i)
        a.append(i * i * i * i * i * i)
    return a


prof = LineProfiler()
prof.add_function(hoge)
prof.runcall(hoge)
prof.print_stats()
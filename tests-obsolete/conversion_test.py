import timeit

if __name__ == "__main__":
    a = True

    t = timeit.Timer("json.dumps(True)", "import json")

    t_bool2json = t.timeit(1000) / 1000
    print("bool 2 json")
    print(t_bool2json)

    t = timeit.Timer("str(True).lower()", "")

    t_bool2string = t.timeit(1000) / 1000
    print("bool 2 string")
    print(t_bool2string)

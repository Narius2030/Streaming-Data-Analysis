def convert_to_list(line):
    data = eval(line)
    return data

if __name__ == "__main__":
    string = "[{'a':1},{'b':2}]"
    print(type(convert_to_list(string)))
    
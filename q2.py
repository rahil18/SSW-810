
import unittest


def read_file(path, fields, seperator, header):

    result = ('')
    file_name = path
    try: 
        fp = open(file_name, 'r' )
    except FileNotFoundError: 
        print("Can't open", file_name)

    else:
        with fp:
            lines = fp.readlines()

    count = 0

    for i in lines:
        count+=1 
        if count == 1: 
            if header: continue
        
        test = i.split(seperator)
        if len(test) != fields:
            raise ValueError

        x = i.split(seperator)
        yield (x)

    

def main(): 

    path = 'abc'
    for name, cwid, major in read_file(path, 3, ',', header=True):
        print("name: {} cwid: {} major: {}".format(name, cwid, major))


if __name__ == '__main__':
    main()

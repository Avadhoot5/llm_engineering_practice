
# exception handling 

def open_file(name):
    try:
        with open(f'{name}', 'r') as fs:
            contents = fs.readlines()
            ans = int(contents[0])/int(contents[1])
            print(ans)

    except FileNotFoundError:
        print('File Not Found, please check again')
    except ZeroDivisionError:
        print('the number is zero')
    except ValueError:
        print('Value not valid')
    finally:
        print('Done with the code')

# open_file('writing.txt')

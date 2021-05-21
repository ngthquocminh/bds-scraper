file_name = "post_urls_chotot_dat.json"
file_to =  "post_urls_chotot_dat1.json"
file_to2 = "post_urls_chotot_dat2.json"

def foo2():
    lines = []
    try:
        file = open(file_to, "r")
        lines = file.readlines()
        file.close
    except:
        ""
    print(len(lines))

    l = 0
    for line in lines:
        try:
            eval(line)
            l += 1
        except:
            ""
    print(l)

def foo1():
    file = open(file_to, "w")
    i = 0
    with open(file_name) as f:
        while True:
            data = f.read(102400)
            if not data:
                break
            # print(data)
            data = data.replace("\"}}{\"", "\"}}\n{\"")
            file.write(data)
            i += 1
            print(i)
            # if i == 2000:
            #     break
def foo3():
    file = open(file_to, "r")    
    i = 0
    with open(file_to2, "r") as f:
        while True:
            data = f.read(102400)
            if not data:
                break
            # print(data)
            data = data.replace("\"}}{\"", "\"}}\n{\"")
            file.write(data)
            i += 1
            print(i)
            # if i == 2000:
            #     break
# foo1()
# foo2()

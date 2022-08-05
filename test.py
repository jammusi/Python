l = []
l.append("fileNAme")
l.append(("fileNAme","newName"))
l.append(("fileNAme1"))

for item in l:
    
    if isinstance(item,tuple):
        if len(item) == 2:
            tname = item[1]
        else:
            tname = item[0]
    elif(isinstance(item,str)):
        tname = item
    else:
        print("unsupported expected 2 items tuple or string get():",item)

    print(tname)

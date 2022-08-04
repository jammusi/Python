from dbApp import insert_row
from dbApp import select

def _get_conn_dict():
    conn = {
        "host": "localhost",
        #"host": None,
        "db_name" : "test_db",
        "db_name" : "postgres",
        "user" : "postgres",
        "psswrd" : "12345",
        "port" : None
        }

    return conn
def _testInsert():
    print ("test insert")
    conn = _get_conn_dict()

    tname = "table1"
    colname1 = "Name"
    colname2 = "number"
    vc1 = "Oren"
    vc2 = 3

    row = {colname1: vc1, colname2: vc2}

    insert_row(conn, tname, row)

    row[colname2] = 4
    row[colname1] = "Alon"
    insert_row(conn, tname, row)
    
    row[colname2] = 3
    row[colname1] = "Roi"
    insert_row(conn, tname, row)
    print ("test insert - done")

def _testSelect():
    print("test Select... ")
    
    conn = _get_conn_dict()
    tname = "table1"
    colname1 = "Name"
    colname2 = "number"
    
    by = {colname2: 3,colname1: "Oren"}

    res = select(conn, tname, by ,None)
    
    print("select res:", res)

def main(args):

    check = lambda dct,key : key in dct 

    d = {"k1": 4,"k2":"e"}


    print(check(d,"e"))
    
    return
    print(d.keys())


    if "k3" in d:
        print("yes")
    else:
        print("no")


    return
    _testInsert()
    _testSelect()
    return

if __name__ == '__main__':
   
    main(None)
  

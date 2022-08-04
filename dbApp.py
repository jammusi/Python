
from typing import Tuple
import psycopg2

#_from curses import has_key

default_port = 5432
default_host = "localhost"

con_key_host = "host"
con_key_db_name = "db_name"
con_key_user = "user"
con_key_passwrd = "psswrd"
con_key_port = "port"

_db_key_conn = "conn"
_db_key_cur = "cur"

def _close_connection(db: Tuple):
    
    if db[_db_key_cur] is not None:
        db[_db_key_cur].close()

    if db[_db_key_conn] is not None:
        db[_db_key_conn].close()

def _connect(conn: dict) -> dict:
    res = {"conn": None, "cur": None}
    
    try:
        
        # NOTE:
        # assumption port & host will be presnt in dictionay!!
        host = conn[con_key_host] if conn[con_key_host] else default_host
        port = conn[con_key_port] if conn[con_key_port] else default_port

        _conn = psycopg2.connect(host = host, 
                                    database = conn[con_key_db_name],
                                    user = conn[con_key_user],
                                    password = conn[con_key_passwrd],
                                    port = port)

        res[_db_key_conn] = _conn
        res[_db_key_cur] = _conn.cursor()

    except Exception as e:
        print("Connection to {} failed".format(conn))
        print(e)
    
    return res

#wrap input string with double qoutes
def _wrap_col_with_qoutes(col_name: str) -> str:
    return '"{0}"'.format(col_name)

#wrap input string with single qoutes
def _wrap_val_with_qoutes(col_name: str) -> str:
    return "'{0}'".format(col_name)

def _get_cols_list(cols):
    #wrap all cols    
    wrap_cols = map(_wrap_col_with_qoutes, cols)
    #join to str
    cols_str = ",".join( wrap_cols)
    return cols_str

def _get_ins_statement(table_name: str, row: dict) -> str:

    # wrap() all cols names
    wrap_cols = map(_wrap_col_with_qoutes, row.keys())

    #join to str
    cols_str = ",".join( wrap_cols)

    cols_str = _get_cols_list(row.keys())
    #prepare vals place holders
    formats = ""
    for i in range (len(row)):
        formats += "%s,"

    #remove trailing comma
    formats = formats[0:len(formats)-1]

    sql = "INSERT INTO {0}({1}) VALUES({2})" \
                    .format(table_name, cols_str, formats)

    return sql

def _getSelectCols(cols: list) -> str:
    col_list = "*"

    #sanity.
    #for any issue select *
    if cols is not None \
                and isinstance(cols,list) \
                and cols.count > 0:
        #use col named list
        col_list = _get_cols_list(cols)

    return col_list

def _get_where(whereD: dict) -> str:
    where = ""
    if (whereD is not None and len(whereD) > 0):
        where = "WHERE " 
    
        #convert to list
        l = []
        for key, val in whereD.items():
            #wrap: 
            # col name with double qoutes
            # val with single quotes
            l.append(" {0}={1} ".format(_wrap_col_with_qoutes(key), 
                                                _wrap_val_with_qoutes(val)))
            
        #join & append
        where += " and ".join(l)

    return where

def _get_full_sel_statement(tname: str, cols_list: str, whereClause: str):

    return "SELECT {0} FROM {1} {2}" \
                        .format(cols_list, tname, whereClause)

def select(conn: dict, table_name: str, by: dict, cols=[]) -> list:
    rows = []
    try:
        db = _connect(conn)

        #only if connected
        if db[_db_key_conn] is not None: 

            _cols = _getSelectCols(cols)
            _where = _get_where(by)
            select = _get_full_sel_statement(table_name, _cols, _where)

            #select & fetch 
            cur = db[_db_key_cur]
            cur.execute(select)
            rows = cur.fetchall()
        
    except Exception as e:
        print('select ex: '+ str(e))

    finally:
        _close_connection(db)        
        return rows

def insert_row(conn: dict, table_name: str, row: dict) -> bool:
    
    # sanity
    if row is None or not isinstance(row, dict):
        print("row is None or not dict", row)
        return False

    ret = True

    #connect to db
    db = _connect(conn)
    
    #connect faild -> abort
    if not db[_db_key_conn]:
        return False

    try:
        sql = _get_ins_statement(table_name, row)
        #convert to list
        _vals = []
        for v in row.values():
            _vals.append(v)

        #insert row
        db[_db_key_cur].execute(sql, _vals)
        db[_db_key_conn].commit()

    except Exception as e:
        print('insert_row ex: '+ str(e))
        ret = False

    finally:
        _close_connection(db)

    return ret


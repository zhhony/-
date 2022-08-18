import pymysql
import pandas
import time
import sys
import traceback
from pathlib import Path
from typing import *

pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)

# 定义数据库连接


def UseConn(userHost: str, userPort: int, userUser: str, userPassword: str, userDatabase: str) -> pymysql.connect:
    conn = pymysql.connect(host=userHost, port=userPort,
                           user=userUser, password=userPassword, database=userDatabase)
    return conn


# 验证数据库连接是否成功
def ConnVerify(conn) -> bool:
    cur = conn.cursor()
    try:
        cur.execute('SELECT VERSION()')
        conn.commit()
        return True
    except:
        return False
    finally:
        cur.close()


# 定义清空数据库表的命令
def truncate(conn):
    cur = conn.cursor()
    try:
        cur.execute("truncate t_account_book")
        conn.commit()
        print('截断数据成功')
    except:
        print('截断表发生错误！')
    finally:
        cur.close()


# 验证path是否是一个合法的文件路径
def PathVerify(userPath: str) -> bool:
    if Path(userPath).exists():
        if Path(userPath).is_file():
            return True
    else:
        return False


# 验证path是否是xlsx或者xls文件
def TypeVerify(userPath: str) -> bool:
    if Path(userPath).match('*.xlsx'):
        return True
    elif Path(userPath).match('*.xls'):
        return True
    else:
        return False


# 数据库写入
def InsertDB(conn, userList: list):
    cur = conn.cursor()
    try:
        sql = "INSERT INTO `zq_server`.`t_account_book` (`t_type`, `t_figer`, `t_udfiger`, `t_count1`, `t_count2`, `t_amount`, `t_date`, `t_person`, `t_project`, `t_shop`, `t_notice`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur.executemany(sql, userList)
        conn.commit()
        print('写入成功')
    except:
        print('写入发生了错误！')
        traceback.print_exc()
    finally:
        cur.close()


# 主程序
def run(host, port, user, password, database, path):
    try:
        conn = UseConn(host, port, user, password, database)

        if ConnVerify(conn):
            print('>>数据库连接成功！')
        else:
            print('>>连接数据库失败！')

        time.sleep(0.5)
        while True:
            if PathVerify(path):
                pass
            else:
                print('>>无效的文件路径')
                continue
            if TypeVerify(path):
                break
            else:
                print('>>不是有效的xlsx或xls文件')
                continue

        with pandas.ExcelFile(path, engine='xlrd') as f:
            try:
                del contantList
            except:
                pass

            for i in range(6):
                try:
                    contantList
                except NameError:
                    contantList = f.parse(sheet_name=i).fillna(value='')
                    continue
                else:
                    contantList = pandas.concat(
                        [contantList, f.parse(sheet_name=i).fillna(value='')])

        contantList = pandas.concat(
            [contantList]).values.tolist()   # 这个变量存储了所有sheet数据的集合

        # 清空表
        truncate(conn)
        # 写入表
        InsertDB(conn, contantList)
    except:
        print('----------------------------------')
        print('错误信息:%s' % sys.exc_info()[1])
        traceback.print_exc()
        print('----------------------------------')
    finally:
        conn.close()

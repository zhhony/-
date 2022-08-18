import argparse
import pandas
import time
import sys
import traceback
from pathlib import Path
from typing import *
from mudules import *


# 验证数据库连接是否成功
def ConnVerify() -> bool:
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
def truncate():
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


# 验证path是否是xlsx文件
def TypeVerify(userPath: str) -> bool:
    if Path(userPath).match('*.xlsx'):
        return True
    elif Path(userPath).match('*.xls'):
        # TypeTransform(userPath)
        # global xlPath
        # xlPath = userPath + 'x'
        return True
    else:
        return False


# 数据库写入
def InsertDB(userList: list):
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
try:
    if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument('-ho', '--host', help='数据库地址')
        parser.add_argument('-po', '--port', type=int,
                            default=3306, help='端口号')
        parser.add_argument('-us', '--user', help='用户名')
        parser.add_argument('-pa', '--password', help='密码')
        parser.add_argument('-da', '--database', help='数据库名称')
        args = parser.parse_args()

        conn = UseConn(args.host, args.port, args.user,
                       args.password, args.database)
        if ConnVerify():
            print('>>数据库连接成功！')
        else:
            print('>>连接数据库失败！')

        time.sleep(0.5)
        while True:
            xlPath = input('>>请输入Excel路径\n■:')
            if PathVerify(xlPath):
                pass
            else:
                print('>>无效的文件路径')
                continue
            if TypeVerify(xlPath):
                break
            else:
                print('>>不是有效的xlsx或xls文件')
                continue

        filePath = Path(xlPath)  # 得到有效的xlsx文件路径

        with pandas.ExcelFile(filePath) as f:
            try:
                del contantList
            except:
                pass

            for i in range(6):
                try:
                    contantList
                except NameError:
                    contantList = f.parse(sheet_names=i).fillna(value='')
                    continue
                else:
                    contantList = pandas.concat(
                        [contantList, f.parse(sheet_names=i).fillna(value='')])

        contantList = pandas.concat(
            [contantList]).values.tolist()   # 这个变量存储了所有sheet数据的集合

        # 清空表
        truncate()
        # 写入表
        InsertDB(contantList)
except:
    print('----------------------------------')
    print('错误信息:%s' % sys.exc_info()[1])
    traceback.print_exc()
    print('----------------------------------')
finally:
    conn.close()

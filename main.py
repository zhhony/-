import cookie
import url
import importDB
import json


cookie.run()  # 执行获取最新cookie的模块
url.run()  # 执行获取下载链接的模块


xlPath = url.getLatestFiles('./data/', '朱朱与倩倩-流水')
with open('D:/workdata/sui-api/db', 'r') as f:
    DB = json.load(f)


importDB.run(host=DB['host'], port=DB['port'],
             user=DB['user'], password=DB['password'], database=DB['database'], path=xlPath)

import cookie
import url
import importDB
import json




cookie.run()  # 执行获取最新cookie的模块
url.run()  # 执行获取下载链接的模块(注意这一段会启用一般三个子线程，主线程未设置阻塞，所以主线程完成后可能会出现未下载完的情况)


xlPath = url.getLatestFiles('./data/','abc')
with open('D:/workdata/sui-api/db', 'r') as f:
    DB = json.load(f)


importDB.run(host=DB['host'], port=DB['port'],
             user=DB['user'], password=DB['password'],database= DB['database'],path=xlPath)

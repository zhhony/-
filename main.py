import cookie
import url
import pandas


pandas.set_option('display.unicode.east_asian_width', True)
pandas.set_option('display.unicode.ambiguous_as_wide', True)


cookie.run()  # 执行获取最新cookie的模块
url.run()  # 执行获取下载链接的模块(注意这一段会启用一般三个子线程，主线程未设置阻塞，所以主线程完成后可能会出现未下载完的情况)

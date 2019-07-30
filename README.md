# RssCollector
通过RSS收集展示特定网站更新内容[南京分行辖内政务信息关注网站]

第三方库：feedparser，flask,SQLalchemy
项目基于Flask制作，入口为app.py.

部分网站需要代理才能正确获取信息，如无代理，不会报错，但这些网站的内容将无法爬取。

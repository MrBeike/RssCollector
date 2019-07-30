import feedparser, re, sqlite3, time
from flask import flash
from frozen_dir import app_path
dir = app_path()

class RssCollector:
    def __init__(self):
        self.db = sqlite3.connect(dir+r'\RssNews.db')
        self.container = []
        self.imf()
        self.worldbank()
        self.adb()
        self.federalreserve()
        self.cbo()
        self.taxfoundtaion()
        self.economist()
        self.eiu()
        self.bruegel()
        self.db_createtable()
        self.data2db()

    def data2db(self):
        i = 0
        flash("信息收集完成，正在写入数据库")
        for item in self.container:
            if self.db_checkedata(item):
                self.db_add_data(item)
                i += 1
            else:
                continue
        self.db.commit()
        self.db_close()
        flash("数据库写入完成，本次共收集%d条新信息" % i)

    def db_createtable(self):
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS news(id integer primary key,title TEXT,publish_time TEXT,link TEXT,add_time TEXT);")
        self.db.commit()

    def db_checkedata(self, item):
        cursor = self.db.cursor()
        cursor.execute("SELECT * from news WHERE title=? AND link=?", (item['title'], item['link']))
        if not cursor.fetchall():
            return True
        else:
            return False

    def db_add_data(self, item):
        self.db.execute("INSERT INTO news(title,publish_time,link,add_time) VALUES(?,?,?,?)", (
            item['title'], item['date'], item['link'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))

    def db_close(self):
        self.db.close()

    def htmltag_remove(html):
        htmltag = re.compile(r'<[^>]+>')  # 从'<'开始匹配，不是'>'的字符都跳过，直到'>'
        string = htmltag.sub('', html)
        return string

    '''
    IMF
    :return title date link
    :url:https://www.imf.org/en/news/rss
    '''

    def imf(self):
        feed = feedparser.parse('https://www.imf.org/en/news/rss')
        for item in feed.entries:
            news = {}
            news['title'] = item['title']
            news['date'] = time.strftime("%Y-%m-%d %X", item['published_parsed'])
            news['link'] = item['link']
            self.container.append(news)
        flash("IMF collected %d" % len(feed))

    '''
    worldbank
    :return title date link summary  keyword
    :url http://search.worldbank.org/api/v2/news?format=xml&rows=50
         http://search.worldbank.org/api/v2/news?format=atom&rows=100
    '''

    def worldbank(self):
        feed = feedparser.parse('http://search.worldbank.org/api/v2/news?format=atom&rows=50')
        for item in feed.entries:
            news = {}
            news['title'] = item['title']
            news['date'] = item['wb_news.lnchdt']
            news['link'] = item['link']
            # news['summary'] = item['summary']
            # news['keyword'] = item['wb_news.keywd']
            self.container.append(news)
        flash("worldbank collected %d" % len(feed))

    '''
    adb
    :return  title date link summary
    :url https://www.adb.org/rss
         http://feeds.feedburner.com/adb_news
         http://feeds.feedburner.com/adb_publications
         http://feeds.feedburner.com/adb_blogs
    '''

    def adb(self):
        feed = feedparser.parse('http://feeds.feedburner.com/adb_news')
        for item in feed.entries:
            news = {}
            news['title'] = item['title']
            news['date'] = time.strftime("%Y-%m-%d %X", item['published_parsed'])
            news['link'] = item['link']
            # news['summary'] = item['summary']
            self.container.append(news)
        flash("ADB collected %d" % len(feed))

    '''
    federalreserve
    :return title date link summary #keyword
    :url https://www.federalreserve.gov/feeds/press_all.xml
    '''

    def federalreserve(self):
        feed = feedparser.parse('https://www.federalreserve.gov/feeds/press_all.xml')
        for item in feed.entries:
            news = {}
            news['title'] = item['title']
            news['date'] = time.strftime("%Y-%m-%d %X", item['published_parsed'])
            news['link'] = item['link']
            # news['summary'] = item['summary']
            #     news['keyword'] = item['wb_news.keywd']
            self.container.append(news)
        flash("federalreserve collected %d" % len(feed))

    '''
    cbo
    :return title date link summary 
    :url https://www.cbo.gov/publications/all/rss.xml
    '''

    def cbo(self):
        feed = feedparser.parse('https://www.federalreserve.gov/feeds/press_all.xml')
        for item in feed.entries:
            news = {}
            news['title'] = item['title']
            news['date'] = time.strftime("%Y-%m-%d %X", item['published_parsed'])
            news['link'] = item['link']
            # news['summary'] = item['summary']
            self.container.append(news)
        flash("CBO collected %d" % len(feed))

    '''
    taxfoundtaion
    :return  title summary link
    :url https://taxfoundation.org/rss
         https://taxfoundation.org/feed
    '''

    def taxfoundtaion(self):
        feed = feedparser.parse('https://taxfoundation.org/feed')
        for item in feed.entries:
            news = {}
            news['title'] = item['title']
            news['date'] = time.strftime("%Y-%m-%d %X", item['published_parsed'])
            news['link'] = item['link']
            # news['summary'] = item['summary']
            self.container.append(news)
        flash("taxfoundtation collected %d" % len(feed))

    '''
    economist
    :url https://www.economist.com/the-world-this-week/rss.xml
    :return  title date link 
    https://www.economist.com/china/
    VPN 搜索 print RSS newsletter  [subscribe]
    '''

    def economist(self):
        feed = feedparser.parse('https://www.economist.com/the-world-this-week/rss.xml')
        for item in feed.entries:
            news = {}
            news['title'] = item['title']
            news['date'] = time.strftime("%Y-%m-%d %X", item['published_parsed'])
            news['link'] = item['link']
            # news['summary'] = item['summary']
            self.container.append(news)
        flash("economist collected %d" % len(feed))

    '''
    EIU TheEconomist Intelligence Unit
    :return title date link summary
    :url http://gfs.eiu.com/rss.aspx
    '''

    def eiu(self):
        feed = feedparser.parse('http://gfs.eiu.com/rss.aspx')
        for item in feed.entries:
            news = {}
            news['title'] = item['title']
            news['date'] = time.strftime("%Y-%m-%d %X", item['published_parsed'])
            news['link'] = item['link']
            # news['summary'] = item['summary']
            self.container.append(news)
        flash("EIU collected %d" % len(feed))

    '''
    bruegel
    :return  title date link summary author content
    :url bruegel.org/feed/
    '''

    def bruegel(self):
        feed = feedparser.parse('http://bruegel.org/feed/')
        for item in feed.entries:
            news = {}
            news['title'] = item['title']
            news['date'] = time.strftime("%Y-%m-%d %X", item['published_parsed'])
            news['link'] = item['link']
            # news['summary'] = item['summary']
            # news['author'] = item['author']
            # news['content'] = self.htmltag_remove(item['content'][0]['value'])
            self.container.append(news)
        flash("bruegel collected %d" % len(feed))

    ''' 
    hudson
    :return 
    :url https://www.hudson.org/feed.xml
    '''

    def hudson(self):
        feed = feedparser.parse('https://www.hudson.org/feed.xml')
        for item in feed.entries:
            news = {}
            news['title'] = item['title']
            news['date'] = time.strftime("%Y-%m-%d %X", time.strptime(item['published'], "%B %d, %Y"))
            news['link'] = item['link']
            # news['author'] = item['author']
            self.container.append(news)
        flash("hudson collected %d" % len(feed))

    '''
    moodys
    :return 
    :url https://www.moodys.com/researchandratings/research-type/industry-sector-research/003003/003003/-/-1/0/-/0/-/-/-/global/rr
    subscribe?
    '''

    '''
    :url https://www.oxfordeconomics.com/
    subscribe?
    '''


if __name__ == "__main__":
    k = RssCollector()

#coding:utf-8
import json, re, time
from lxml import etree
import requests
from model import CpModel

class Crawler(object):
    def __init__(self):
        self.count = 0
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
        }

    def get_html(self):
        url = 'http://caipiao.163.com/order/cqssc/#from=leftnav'
        resp = requests.get(url, headers=self.headers)
        html = etree.HTML(resp.content)
        self.parse(html)


    def parse(self, html):
        num = html.xpath('//*[@id="j-todayNumTable"]//tr')
        print len(num)
        item = {}

        item['tic_date'] = self.parse_list(html.xpath('//strong/span/text()'))[:-3]
        for n in range(1,len(num)):
            for i in xrange(4):
                item['period'] = self.parse_list(html.xpath('//*[@id="j-todayNumTable"]//tr[%s]//td[%s]//@rel' % (n+1, (5*i)+2)))
                item['awardTd'] = self.parse_list(html.xpath('//*[@id="j-todayNumTable"]//tr[%s]//td[%s]/text()' % (n+1, (5*i)+2)))
                # print item, n
                # break
                if item['awardTd'].replace('-','').strip():
                    self.save(item)


    def parse_list(self, list):
        if len(list) == 1:
            return list[0]
        else:
            string = ''
            for l in list:
                string = string + '\n' + l.strip()
            return string


    def save(self, item):
        try:
            CpModel.create(
                            tic_date=item['tic_date'],
                            w_wan=item['awardTd'][0],
                            w_qian=item['awardTd'][1],
                            w_bai=item['awardTd'][2],
                            w_shi=item['awardTd'][3],
                            w_ge=item['awardTd'][4],
                            tic_num=item['awardTd'],
                            qishu=item['period'],
                            )
        except Exception,err:
            print err



def run():
    agent = Crawler()
    agent.get_html()

    print 'finish!'


if __name__ == '__main__':
    while True:
        run()
        time.sleep(60*3)
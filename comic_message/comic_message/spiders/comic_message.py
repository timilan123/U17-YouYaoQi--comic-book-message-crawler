#by LHF2020.12.21
import scrapy
import requests
import json
from ..items import ComicMessageItem
#获取每本漫画的id，并保存为一个列表，然后返回
def get_id():
    comic_id=[] #建立一个空的列表
    #循环爬取前（?）页
    for page in range(3):
        post_url='https://www.u17.com/comic/ajax.php?mod=comic_list&act=comic_list_new_fun&a=get_comic_list'
        headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60"
            }

        data={
            'data[group_id]': 'no',
            'data[theme_id]': 'no',
            'data[is_vip]': 'no',
            'data[accredit]': 'no',
           ' data[color]': 'no',
            'data[comic_type]': 'no',
            'data[series_status]': 'no',
            'data[order]': '2',
            'data[page_num]': page+1,
            'data[read_mode]': 'no'
        }


        response = requests.post(url=post_url,data=data,headers=headers)#发送post请求
        content  = response.text#获取相应文件的文本
        dic = json.loads(content)#转换为字典的格式
        comic_list = dic['comic_list']#获取一页里面的漫画列表
        for num in range(50):
            comic_id.append(comic_list[num]['comic_id'])

    return comic_id
        #append()->将元素添加到末尾,并不是加一段哦
        #漫画的页面=https://www.u17.com/comic/漫画的id.html
        #可以用post请求循环获取每一个漫画的id保存起来，再循环地去访问每部漫画的页面

#生成每本漫画的url地址，并保存为一个列表，然后返回
def gen_url():
    id_list = get_id()
    url_list = []
    for i in range(len(id_list)):
        single_url = 'https://www.u17.com/comic/'+id_list[i]+'.html'
        url_list.append(single_url)

    return url_list


class ExampleSpider(scrapy.Spider):
    name = 'comic_message'
    allowed_domains = ['www.u17.com']      #域名
    start_urls = ['https://www.u17.com/']   #起始爬取点

    def parse(self, response):  #解析每个页面的链接，注意这个函数名字必须为parse，下面的函数就可以随便取名字了
        url_list= gen_url()
        for i in range(len(url_list)):
            yield scrapy.Request(url=url_list[i], callback=self.parse_page)     #将每个页面返回给页面解析函数
        pass

    def parse_page(self, response): #解析每个页面,注意了，这个函数的名字必须为parse否则会报错
        information = ComicMessageItem()
        #注意：后面那四个必须用字符串赋值，如果要提取字符串必须要用到extract_first()
        information['漫画名'] = response.css('[class=comic_info]>div>h1::text').extract_first().strip()                                     #漫画名
        information['点击量'] = response.css('[class="cf line2"]>div:nth-last-of-type(3)>span::text').extract_first().strip()           #漫画总点击量
        information['月投票'] = response.css('[class="cf line2"]>div:nth-last-of-type(2)>span::text').extract_first().strip()      #漫画的月票量
        #information['comic_introduction'] = response.css('[id="words1"]::text').extract_first().strip()                                         #漫画的文字简介
        yield information
        pass

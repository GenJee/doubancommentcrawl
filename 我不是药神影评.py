import json
import random
import requests
import re
from time import sleep
from bs4 import BeautifulSoup
from lxml import etree

if __name__ == '__main__':
    # 豆瓣影评URL
    url = 'https://movie.douban.com/subject/{}/reviews?start='.format(26752088)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }
    count = 0
    with open('影评.csv', 'w', encoding='utf-8') as fcsv:
        fcsv.write(
            '昵称' + '\t' + '推荐指数' + '\t' + '评论时间' + '\t' + '赞同人数' + '\t' + '字数：' + '\t' + '评论内容' + '\n')
        with open('影评.txt', 'w', encoding='utf-8') as ftxt:
            for page in range(0, 200):
                print('===========================第' + str(page) + '页===========================')
                start_url = url + str(page * 20)
                print(start_url)
                page_text = requests.get(url=start_url, headers=headers).text
                pt = etree.HTML(page_text)
                name_list = re.findall('class="name">(.*?)</a>', page_text, re.S)

                # 找到ID号列表
                div_list = re.findall('data-cid="(.*?)"', page_text, re.S)
                # print("ID号列表：", end='')
                # print('长度：' + str(len(div_list)))
                # print(div_list)

                # 定位到影评的div

                for i in range(len(div_list)):
                    count += 1
                    print('--------------------第' + str(count) + '个--------------------')
                    ftxt.writelines('--------------------第' + str(count) + '个--------------------\n')
                    env = etree.HTML(page_text).xpath('//*[@data-cid="' + str(div_list[i]) + '"]')
                    # print(env)
                    try:
                        for content in env:
                            # 用户名
                            name_src = content.xpath('.//a[@class="name"]/text()')
                            if len(name_src) == 0:
                                name_src = 'null'
                            else:
                                name = name_src[0]
                            print('用户名：', end='')
                            print(name)
                            ftxt.writelines('用户名：' + str(name) + '\n')

                            # 推荐
                            recommend1_src = content.xpath('.//span[contains(@class,"rating")]')
                            if len(recommend1_src) == 0:
                                recommend1 = 'null'
                            else:
                                recommend = content.xpath('.//span[contains(@class,"rating")]')[0].get('class')
                                recommend1 = re.findall('allstar(.*?)0', recommend, re.S)[0]
                            print('推荐指数：', end='')
                            print(recommend1)
                            ftxt.writelines('推荐指数：' + str(recommend1) + '\n')

                            # 时间
                            comment_time_src = content.xpath('.//span[@class="main-meta"]/text()')
                            if len(comment_time_src) == 0:
                                comment_time_src = 'null'
                            else:
                                comment_time = comment_time_src[0]
                            print('时间：', end='')
                            print(comment_time)
                            ftxt.writelines('时间：' + str(comment_time) + '\n')
                    except Exception as e:
                        print('\n\n！！！！！！！！！！！！！！！出错，跳过该数据！！！！！！！！！！！！！！！！！！！！！\n\n')
                        continue
                    # 评论
                    full_text = requests.get(url='https://movie.douban.com/j/review/' + str(div_list[i]) + '/full',
                                             headers=headers).text
                    content_text = BeautifulSoup(json.loads(full_text)['html'], 'html.parser').get_text()
                    print("评论：", end='')
                    print(content_text)

                    # 字数
                    print('字数：' + str(len(content_text)))
                    ftxt.writelines('字数：' + str(len(content_text)) + '\n')

                    # 点赞数
                    like_src = pt.xpath('//span[@id="r-useful_count-' + str(div_list[i]) + '"]/text()')
                    if len(like_src) == 0:
                        like_src = 'null'
                    else:
                        like = like_src[0]
                        like = like.strip()
                    print('点赞：', end='')
                    print(like)
                    ftxt.writelines('点赞：' + str(like) + '\n')

                    ftxt.writelines('评论：' + str(content_text) + '\n\n\n')

                    fcsv.write(str(name) + '\t' + str(recommend1) + '\t' + str(comment_time) + '\t' + str(
                        like) + '\t' + str(len(content_text)) + '\t' + str(content_text.replace('\n', '')) + '\n')
                    sleep(random.randint(0, 2))
        ftxt.close()
    fcsv.close()

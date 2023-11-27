import csv
import random
import requests
import re
import os
from time import sleep
from lxml import etree

if __name__ == '__main__':
    # 豆瓣影评URL
    url = 'https://movie.douban.com/subject/{}/comments'.format(26752088)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    }

    # 影评页面：
    with open('短评.csv', 'w', encoding='utf-8') as f:
        f.write(
            '昵称' + '\t' + '推荐指数' + '\t' + '评论时间' + '\t' + '赞同人数' + '\t' + '评论内容' + '\n')
        for start_page in range(0, 201):
            comment_url = url + '?start=' + str(start_page * 20) + '+&limit=20&status=P&sort=new_score'
            comment_text = requests.get(url=comment_url, headers=headers).text
            print('第' + str(start_page) + '页***************************')
            tree = etree.HTML(comment_text)
            for temp in range(0, 20):

                try:
                    print('======================第' + str(start_page * 20 + temp) + '个===========================')
                    # 名字
                    name = tree.xpath('//*[@id="comments"]/div[' + str(temp + 1) + ']/div[2]/h3/span[2]/a/text()')
                    if len(name) == 0:
                        name = ['null'];
                    print('名字：' + str(tree.xpath(
                        '//*[@id="comments"]/div[' + str(temp + 1) + ']/div[2]/h3/span[2]/a/text()')[0]))

                    # 推荐等级
                    rand_text = tree.xpath('//*[@id="comments"]/div[' + str(temp + 1) + ']/div[2]/h3/span[2]/span[2]')[
                        0]
                    allstar_rating = rand_text.get('class')
                    recommend = re.findall('allstar(.*?)0 rating', allstar_rating, re.S)
                    if len(recommend) == 0:
                        recommend = ['null'];
                    print('推荐等级：' + str(recommend[0]))

                    # 时间
                    c_time = tree.xpath('//*[@id="comments"]/div[' + str(temp + 1) + ']/div[2]/h3/span[2]/span[3]')
                    comment_time = c_time[0].get('title')
                    if type(comment_time) == None:
                        comment_time = ['null'];
                    print('时间：' + str(comment_time))

                    # 评论
                    comment_content = tree.xpath('//*[@id="comments"]/div[' + str(temp + 1) + ']/div[2]/p/span/text()')
                    comment_content = comment_content[0].replace('\n', '')
                    if len(comment_content) == 0:
                        comment_content = ['null'];
                    print('评价：' + str(comment_content))
                    # 点赞
                    like = tree.xpath('//*[@id="comments"]/div[' + str(temp + 1) + ']/div[2]/h3/span[1]/span/text()')
                    if len(like) == 0:
                        like = ['null'];
                    print('点赞：' + str(like[0]))
                except Exception as e:
                    print('出错,跳过改数据！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！')
                    continue
                f.write(
                    str(name[0]) + '\t' + str(recommend[0]) + '\t' + str(comment_time) + '\t' + str(like[
                                                                                                        0]) + '\t' + str(
                        comment_content) + '\n')
                sleep(1)
            sleep(random.randint(1, 4))

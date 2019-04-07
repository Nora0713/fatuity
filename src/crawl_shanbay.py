# !/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import csv
import bs4
import codecs


# 检查url地址并返回网页contents
def check_link(url):
    try:

        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('无法链接服务器！！！')


# 判断一个unicode是否是英文字母
def is_alphabet(uchar):
    if ('\u0041' <= uchar <= '\u005a') or ('\u0061' <= uchar <= '\u007a'):
        return True
    else:
        return False


# 爬取表格数据
def get_contents(urlist):
    '''urlist: a list containing all the useful urls'''
    result = []
    for url in urlist:
        content = check_link(url)
        soup = BeautifulSoup(content, 'lxml')
        trs = soup.find_all('tr')
        for tr in trs:
            ui = []
            for td in tr:
                ui.append(td.string)
            result.append(ui)
    return result


# 爬取URL链接
def get_urls(url_content, root_url="https://www.shanbay.com"):
    '''get all the urls from url_content and save into a list'''
    ulist = []
    soup = BeautifulSoup(url_content, 'lxml')
    urls = soup.find_all('a')
    for url in urls:
        try:
            if url.string.startswith('【无老师7天TOEFL】List'):
                ulist.append(root_url + url.get('href'))
                for j in range(2, 11):
                    extend_url = root_url + url.get('href') + '?page=' + str(j)
                    ulist.append(extend_url)
        except:
            pass
    return ulist


def save_contents(result):
    '''result: all the useful result from urls'''
    with codecs.open('shanbay.csv', 'w', 'utf_8_sig') as f:
        writer = csv.writer(f)
        for i in range(len(result)):
            try:
                if is_alphabet(result[i][1]):
                    writer.writerow([result[i][1], result[i][3]])
                    print("write in line:", i)
            except:
                print("error in line:{}, contents is:{}".format(i, result[i]))

def main():
    src_url = "https://www.shanbay.com/wordbook/5440/"
    # get the contents in source page
    src_content = check_link(src_url)

    # get all the useful urls in source page
    urls = get_urls(src_content)

    # scrapy all the useful contents from all the urls
    result = get_contents(urls)
    # save all the useful contents into csv
    save_contents(result)


if __name__ == '__main__':
    main()
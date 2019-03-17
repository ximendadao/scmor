import execjs
import requests
from lxml import etree
import re

with open('scmor.js', 'r', encoding='utf-8') as f:
    js1 = f.read()
    ctx = execjs.compile(js1)


def get_html(url):
    html = ''
    while html=='':
        try:
            html = requests.get(url).text
        except:
            pass
    return html


def parse_content(html):
    tree = etree.HTML(html)
    script_text = tree.xpath('//script/text()')[0]
    securty = re.findall(r'QSQ7X[a-zA-Z0-9]+=*', script_text)
    return securty


def decode(string):
    string = ctx.call('base64decode',string)  # base64解码string参数,string参数的值就是上面代码中的那段base64编码后的内容
    key = " link@scmor.comok "  # Gword的值+ 'ok '  注意，有空格
    Len = len(key)  # Gword长度
    code = ''
    for i in range(0, len(string)):
        k = i % Len
        n = ord(str(string[i])) ^ ord(str(key[k]))
        code += chr(n)
    return ctx.call('base64decode',code)


if __name__ == '__main__':
    html = get_html("http://ac.scmor.com/")
    security_list = parse_content(html)
    for security_text in security_list:
        print(decode(security_text))

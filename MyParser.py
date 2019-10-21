from html.parser import HTMLParser
import string
import re


class MyParser(HTMLParser):
    newid = ""
    text = False
    content = ""
    one_dict = dict()

    def handle_starttag(self, tag, attrs):
        # print("Step1:")
        if tag == "reuters":
            for attr in attrs:
                if attr[0] == "newid":
                    MyParser.newid = attr[1]

        if tag == "title" or tag == "body":
            self.text = True

    def handle_endtag(self, tag):
        # print("Step2:")
        if tag == "title" or tag == "body":
            self.text = False
        if tag == "reuters":
            a = str(MyParser.newid)
            b = str(MyParser.content)
            # 标点
            # punctuation = '!,;:?"\'()'
            # b = re.sub(r'[{}]+'.format(punctuation),'',b)
            # b = b.replace(string.punctuation, " ")
            # print("**" * 20)
            # print("MyParser.newid: " + a)
            # print("MyParser.content: " + b)
            MyParser.one_dict[a] = b
            MyParser.content = ""

    def handle_data(self, data):
        # print("Step3:")
        if self.text:
            MyParser.content = MyParser.content + " " + data
            # 大小写
            # MyParser.content = MyParser.content + " " + data.lower()

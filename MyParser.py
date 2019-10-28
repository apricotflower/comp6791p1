from html.parser import HTMLParser


class MyParser(HTMLParser):
    """  catch title and body from the raw corpus """
    newid = ""
    text = False
    content = ""
    one_dict = dict()

    def handle_starttag(self, tag, attrs):
        if tag == "reuters":
            for attr in attrs:
                if attr[0] == "newid":
                    MyParser.newid = attr[1]

        if tag == "title" or tag == "body":
            self.text = True

    def handle_endtag(self, tag):
        if tag == "title" or tag == "body":
            self.text = False
        if tag == "reuters":
            a = str(MyParser.newid)
            b = str(MyParser.content)
            MyParser.one_dict[a] = b
            MyParser.content = ""

    def handle_data(self, data):
        if self.text:
            MyParser.content = MyParser.content + " " + data


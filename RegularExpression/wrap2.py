import requests, re

def search(url):
    # regex = r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)"
    regex = r"([a-zA-Z0-9_.+-]+@[a-pr-zA-PRZ0-9-]+\.[a-zA-Z0-9-.]+)"
    html = requests.get(url).text
    # print(html)
    emails = re.findall(regex, html)
    i = 0
    for email in emails:
        i += 1
        #if i < 16:
        print("{} :{}".format(i, email))

print("\nnkust\n")
search("http://www.csie.kuas.edu.tw/teacher.php")
print("\nncku\n")
search("http://www.csie.ncku.edu.tw/ncku_csie/depmember/teacher")
print("\nshu\n")
search("http://www.shu.edu.tw/SHU-Contact.aspx")
print("\ntaf\n")
search("https://www.taftw.org.tw/wSite/ct?xItem=61&ctNode=283")
print("\ncga\n")
search("https://www.cga.gov.tw/GipOpen/wSite/lp?ctNode=9331&mp=9991/&idPath=9238_9331")
print("\nfju\n")
search("http://www.fju.edu.tw/article.jsp?articleID=13")
print("\ntnua\n")
search("http://1www.tnua.edu.tw/~TNUA_THEATRE/members/teacher.php")


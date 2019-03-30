# http://www.csie.kuas.edu.tw/teacher.php
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

def nkust():
    emails = []
    res = requests.get('http://www.csie.kuas.edu.tw/teacher.php')
    soup = BeautifulSoup(res.text, 'html.parser')
    #print(soup.prettify())


    divs = soup.find_all('div', {"id": "content"})
    for d in divs:
        tds = soup.find_all('td')
        tds_len = len(tds)

        for i in range(1, tds_len, 2):
            text = str(tds[i].text)
            email_head = text.find("箱：")
            email_tail = text.find(".tw")

            emails.append(text[email_head+2:email_tail])
    return emails

def ncku():
    emails = []
    res = requests.get('http://www.csie.ncku.edu.tw/ncku_csie/depmember/teacher')
    soup = BeautifulSoup(res.text, 'html.parser')

    divs = soup.find_all('div', {"id": "wrap"})
    for _ in divs:
        divs = soup.find_all('div', {"id": "page"})
        for _ in divs:
            divs = soup.find_all('div', {"class": "container"})
            for _ in divs:
                divs = soup.find_all('div', {"class": "row-fluid"})
                for _ in divs:
                    divs = soup.find_all('div', {"class": "content_maintext tab-content"})
                    for _ in divs:
                        divs = soup.find_all('td', {"class": "teacherInfo"})
                        for _ in divs:
                            br = soup.find_all('br')
                            print(br.extract())



ncku()


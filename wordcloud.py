
#! /usr/bin/python3.4
# -*- coding: utf-8 -*-

from collections import Counter
import urllib.request, urllib.parse, urllib.error
import random
import webbrowser

from konlpy.tag import Hannanum
from lxml import html
import pytagcloud # requires Korean font support
import sys

if sys.version_info[0] >= 3:
    urlopen = urllib.request.urlopen
else:
    urlopen = urllib.request.urlopen


r = lambda: random.randint(0,255)
color = lambda: (r(), r(), r())

def get_bill_text(billnum):
#    url = 'http://pokr.kr/bill/%s/text' % billnum
    url = 'https://raw.githubusercontent.com/eventia/CandSpeech/master/%s.txt' % billnum
    response = urlopen(url).read().decode('utf-8')
    page = html.fromstring(response)
    text = response
    return text

def get_tags(text, ntags=50, multiplier=10):
    h = Hannanum()
    nouns = h.nouns(text)
    count = Counter(nouns)
    return [{ 'color': color(), 'tag': n, 'size': c*multiplier }\
                for n, c in count.most_common(ntags)]

def draw_cloud(tags, filename, fontname='NanumGothic', size=(1280, 720)):
    pytagcloud.create_tag_image(tags, filename, fontname=fontname, size=size)
    webbrowser.open(filename)

bill_num = ['n1_moon','n2_hong','n3_ahn','n4_yoo','n5_sim', ]

for candperson in bill_num:
    text = get_bill_text(candperson)
    tags = get_tags(text)
    print(tags)
    draw_cloud(tags, 'speech_'+candperson+'.png')

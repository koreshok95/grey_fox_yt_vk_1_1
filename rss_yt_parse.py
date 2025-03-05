import requests
from lxml import etree
from googletrans import Translator
import re

#связб между тегами из xml и мусорными тегами получеными из response
tags_codes={'entry':"{http://www.w3.org/2005/Atom}entry",'id':"{http://www.w3.org/2005/Atom}id",'title':'{http://www.w3.org/2005/Atom}title',\
    'videoId':'{http://www.youtube.com/xml/schemas/2015}videoId','description':'{http://search.yahoo.com/mrss/}description'}
#убирает смайлики символы перевода каретки и прочий шклак
def clear_string(text):
    '''
    убирает смайлики символы перевода каретки и прочий шклак из text
    '''
    a=['\\n','\\r','\\t']
    text=text[1:]
    for c in a:
        text=text.replace(c,'')
    ltext=list(text)
    while '\\' in ltext:
        k=text.index('\\')
        try:
            ltext.pop(k)
            ltext.pop(k+1)
            ltext.pop(k+2)
        except:
            break
            return text
    return ''.join(ltext)

def get_yt_news(chanel_id,ntry=2):
    '''
    #возвращает список словарей с новостями (сортированый по дате)-но это не точно
    #id канала, количество попыток
    #возвращает {'id','title','url','description'}
    '''
    url=f'https://www.youtube.com/feeds/videos.xml?channel_id={chanel_id}'
    news=[]
    while ntry>0:
        try:
            translator = Translator()
            resp=requests.get(url)
            if resp.status_code==200:
                page=etree.fromstring(resp.content)
                try:
                    entrys=page.findall(tags_codes['entry'])
                except:
                    ntry-=1
                    continue
                for d in entrys:
                    try:
                        id=str(etree.tostring(d.find(tags_codes['videoId']), method="text",encoding='UTF-8'))
                        id=clear_string(id).replace("'",'').replace(" ",'')#для id нужно почище строчку
                        title=str(etree.tostring(d.find(tags_codes['title']), method="text",encoding='UTF-8'))
                        title=translator.translate(clear_string(title),src='en',dest='ru').text 
                        videourl='https://www.youtube.com/watch?v='+id
                        try:
                            description=str(etree.tostring(d.find(tags_codes['description']), method="text",encoding='UTF-8'))
                            description=translator.translate(clear_string(description),src='en',dest='ru').text
                        except Exception as e:
                            description='Новое видео на канале'
                        news.append({'id':id,'title':title,'url':videourl,'description':description})
                    except:
                        continue
            else:
                ntry_=1
                continue
            return news
        except:
            ntry-=1
            continue
    return -1
#print(get_yt_news('UCdC0An4ZPNr_YiFiYoVbwaw',5),sep='\n')

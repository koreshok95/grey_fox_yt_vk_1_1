
import requests
import os
import random


class vk_manage_app:
    def __init__(self,app_token):
        self.app_token=app_token
    def upload_vk_video(self,title,description,group_id,album_id,full_file):
        '''
        title,description,group_id,album_id,full_file
        загружает видео с названием title и описанием description d группу group id 
        в плейлист album id(0-если не нужен плейлист) видеофайл по полному пути full_file
        '''
        params= {
        'access_token': self.app_token,
        'name':title,
        'description':description,
        'group_id':group_id,
        'no_comments':1,
        'v': 5.199
        }
        if album_id!=0:
            params['album_id']=album_id
        resp=requests.get('https://api.vk.com/method/video.save',params=params).json()
    #print(resp)
        if 'response' in resp.keys():
            url=resp['response']['upload_url']
            params={'access_token': self.app_token, 'v': 5.199}
            try:
                upload_video_req=requests.post(url, params=params, files={'video_file': open(full_file, 'rb')})
                video_id = upload_video_req.json()['video_id']
                return video_id
            except:
                return 0
        else:
            return 0
    def make_video_post(self,group_id,video_id,author,group_token):
        '''
        group_id,video_id,author,group_token
        делаем пост с видео в группу
        '''
        params = {
        "access_token": group_token,
        "owner_id": "-" + str(group_id),
        "message": f'Новое видео с канала {author}, в переводе от Мурзилка. Не пропустите!',
        'from_group':1,
        "v": 5.199,
        'attachments':f'video-{group_id}_{video_id}'
        }
        req=requests.post("https://api.vk.com/method/wall.post",params=params).json()
        if 'response' in req.keys():
            return req['response']['post_id']
        else:
            return 0
    def make_template_post(self,group_id,dir,group_token):
        '''
        Создает текстовый пост из готового случайногор шаблона из папки dir
        group_id,dir,group_token
        '''
        samples=os.listdir(dir)
        x=random.choice(samples)
        with open(dir+'/'+x, "r", encoding="utf-8") as f:
            txt=f.read()
        params = {
        "access_token": group_token,
        "owner_id": "-" + str(group_id),
        "message": txt,
        'from_group':1,
        "v": 5.199,
        }
        req=requests.post("https://api.vk.com/method/wall.post",params=params).json()
        if 'response' in req.keys():
            return req['response']['post_id']
        else:
            return 0

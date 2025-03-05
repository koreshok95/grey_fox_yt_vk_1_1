
import vk_upload
import grey_fox_db
import sched,time
import os
from datetime import datetime
import time

class vk_settings:
    def __init__(self,path='vk_settings.ini'):
        with open(path) as f:
            self.dbase_path=f.readline().rstrip('\n')
            self.video_dir=f.readline().rstrip('\n')#'C:/Users/koreshok_main/Videos/youtube_scrap/'#
            self.rep_time=int(f.readline())
            self.upload_trys=int(f.readline())
            self.app_key=f.readline().rstrip('\n')
            self.max_sec_from_last_post=int(f.readline())
            self.template_dir=f.readline().rstrip('\n')
            self.db=grey_fox_db.data_transfer_from_db(self.dbase_path)
            self.mng=vk_upload.vk_manage_app(self.app_key)
            #self.db=grey_fox_db.data_transfer_from_db('grey_fox_1.db')

def main():
    st.enter(s.rep_time,1,main)
    try:
        news=s.db.get_news_to_upload()#получаем не загруженные новости
        for n in news:
            k=s.upload_trys
            while k>0:
                try:
                    a=s.db.get_author(n[1])
                    if n[11]==0:
                        vid=s.mng.upload_vk_video(n[9],n[8],n[3],0,f'{s.video_dir}/{n[10]}')#грузим в личную группу 
                        s.mng.make_video_post(n[3],vid,a,n[2])#постим 
                        s.db.mark_news_person_uploaded(n[0])#помечасем успешную загрузку
                        s.db.set_post_time(n[1])#ставим временную отметку
                    if n[3]!=n[5] and n[12]==0:
                        vid=s.mng.upload_vk_video(n[9],n[8],n[5],n[6],f'{s.video_dir}/{n[10]}')# грузим в главную если она отличается от личной
                        s.mng.make_video_post(n[5],vid,a,n[4])
                        s.db.mark_news_main_uploaded(n[0])#помечасем успешную загрузку
                        s.db.set_main_post_time(n[1])#ставим временную отметку
                    else:
                        s.db.mark_news_main_uploaded(n[0])#помечасем "успешную" загрузку-т.к. она не нужна
                        s.db.set_main_post_time(n[1])#ставим временную отметку
                    break
                except Exception as e:
                    k-=1
            if k==0:
                 with open('logs.txt','a') as f:
                    f.write(f'{datetime.now()} : error upload news {n[0]}\n')
    except Exception as e:
        with open('logs.txt','a') as f:
            f.write(f'{datetime.now()} : {e}\n')

    #проверяем основную группу в которых давно небыло постов и постим гой слоп
    try:
        t_main,gr_key,gr_id=s.db.get_main_last_post_time() 
        if abs(int(time.time())-t_main)>s.max_sec_from_last_post:
            s.mng.make_template_post(gr_id,s.template_dir,gr_key)
            s.db.set_every_main_post_time()
    except Exception as e:
        with open('logs.txt','a') as f:
            f.write(f'{datetime.now()} : {e}\n')
    try:
        pst=s.db.get_groups_last_post_time(s.max_sec_from_last_post)
        for p in pst:
            last_post_time,vk_group_api_key,vk_group_id,cid=p[0],p[1],p[2],p[3]
            x=s.mng.make_template_post(vk_group_id,s.template_dir,vk_group_api_key)
            if x>0:
                s.db.set_post_time(cid)
    except Exception as e:
        with open('logs.txt','a') as f:
            f.write(f'{datetime.now()} : {e}\n')

if __name__=='__main__':
    s=vk_settings()
    #mng=vk_upload.vk_manage_app(s.app_key) 
    print('start_time',time.time())
    st=sched.scheduler()
    main()
    st.run()
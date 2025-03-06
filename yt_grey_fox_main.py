import grey_fox_db
import auto_sub_yt_dlp
import rss_yt_parse
import sched,time
import os
from datetime import datetime

class settings:
    def __init__(self,path='settings.ini'):
        with open(path) as f:
            self.dbase_path=f.readline().rstrip('\n')
            self.video_dir=f.readline().rstrip('\n')#'C:/Users/koreshok_main/Videos/youtube_scrap/'#
            self.rep_time=int(f.readline())
            self.down_trys=int(f.readline())
            self.burn_trys=int(f.readline())
            self.sec_before_del=int(f.readline())
            #print(self.dbase_path)
            self.db=grey_fox_db.data_transfer_from_db(self.dbase_path)
            #self.db=grey_fox_db.data_transfer_from_db('grey_fox_1.db')


def main():
    st.enter(s.rep_time,1,main)
    chanels=[]
    try:
        chanels=s.db.get_chanel_list()
    except Exception as e:
        with open('logs.txt','a') as f:
            f.write(f'{datetime.now()} : {e}\n')
    for ch in chanels:
        id,authour=ch[0],ch[1]
        news=[]
        try:
            news=rss_yt_parse.get_yt_news(id)
        except Exception as e:
            with open('logs.txt','a') as f:
                f.write(f'{datetime.now()} : {e}\n')
            continue
        for n in news:
            try:
                if s.db.is_new(n['id']):
                    x=auto_sub_yt_dlp.yt_load(n['url'],s.video_dir,s.down_trys)
                    fname=auto_sub_yt_dlp.gen_burn_sub(x,s.burn_trys,True)
                    n_dict=[{'id':n['id'], 'chanel_id':ch[0],'vk_group_api_key':ch[2],'vk_group_id':ch[3],'vk_main_group_api_key':ch[4],\
                    'vk_main_group_id':ch[5], 'vk_playlist_key':ch[6], 'video_url':n['url'],'description':n['description'] , \
                    'title':n['title'].replace('«','').replace('»','').replace('"','').replace("'",''), \
                    'file_name':os.path.basename(fname), 'is_up':0,'is_up_main':0, 'is_shorts':auto_sub_yt_dlp.might_short(fname)}]
                    s.db.append_new_news_record(n_dict)
            except Exception as e:
                with open('logs.txt','a') as f:
                    f.write(f'{datetime.now()} : {e}\n')
                continue
    #удаляем старые видео с момента паблика которых прошло больше чем vk_settings.sec_before_del секунд
    s.db.delete_old_video(s.sec_before_del,s.video_dir)

if __name__=='__main__':
    s=settings()
    print('start_time',time.time())
    st=sched.scheduler()
    main()
    st.run()


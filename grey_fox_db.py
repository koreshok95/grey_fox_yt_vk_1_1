
import sqlite3
import time
import os

#connect_str='grey_fox_1.db'

#создает  новую базу 
def create_new_base(db_name):
    """
        создает  новую базу db-name-имя файла БД
    """
    try:
        with sqlite3.connect(db_name) as connection:
            cursor = connection.cursor()
            c1='''CREATE TABLE IF NOT EXISTS Chanels (id TEXT PRIMARY KEY, author TEXT NOT NULL, vk_group_api_key TEXT NOT NULL,vk_group_id TEXT NOT NULL,
            vk_main_group_api_key TEXT NOT NULL, vk_main_group_id TEXT NOT NULL, vk_playlist_key TEXT NOT NULL,last_post_time INTEGER NOT NULL,main_last_post_time INTEGER NOT NULL)'''
            c2='''CREATE TABLE IF NOT EXISTS News (id TEXT PRIMARY KEY, chanel_id TEXT NOT NULL, vk_group_api_key TEXT NOT NULL,vk_group_id TEXT NOT NULL,
            vk_main_group_api_key TEXT NOT NULL, vk_main_group_id TEXT NOT NULL, vk_playlist_key TEXT NOT NULL, video_url TEXT NOT NULL,
            description TEXT NOT NULL, title TEXT NOT NULL, file_name TEXT NOT NULL, is_up INTEGER NOT NULL,is_up_main INTEGER NOT NULL,is_shorts INTEGER NOT NULL, last_use INTEGER NOT NULL)'''
            cursor.execute(c1)
            cursor.execute(c2)
            connection.commit()
        return 0
    except Exception as e:
        return str(e)
    
class data_transfer_from_db:
    """
    класс для взаимодействаия с БД для grey fox 
    """
    def __init__(self,path):
        '''
        подключение к базе
        '''
        self.connection=sqlite3.connect(path)
    def is_new(self,news_id):
        """
        проверка была ли эта новость или ролик уже загружена ранее
        """
        cm=f'SELECT COUNT(*) FROM News WHERE id="{news_id}";'
        cr=self.connection.cursor()
        cr.execute(cm)
        y=cr.fetchone()
        if y[0]>0:
            return False
        else:
            return True
    def append_new_news_record(self,news_records):
        '''
        news_recordы список словарей с новостями
        ключи словаря news_record должны совпадать с полями таблицы(кроме last_use-он создасться автоматом),видео уже быть загружено
        id, chanel_id, vk_group_api_key, vk_group_id, vk_main_group_api_key, vk_main_group_id, vk_playlist_key, video_url, description, title, file_name, is_up,is_up_main, is_shorts
        '''
        m=0
        for news_record in news_records:
            cm=f'''INSERT INTO News (id, chanel_id, vk_group_api_key, vk_group_id, vk_main_group_api_key, vk_main_group_id, vk_playlist_key, video_url, description, title, file_name, is_up,is_up_main, is_shorts,last_use) 
            VALUES ("{news_record['id']}","{news_record['chanel_id']}","{news_record['vk_group_api_key']}","{news_record['vk_group_id']}",
            "{news_record['vk_main_group_api_key']}","{news_record['vk_main_group_id']}","{news_record['vk_playlist_key']}",
            "{news_record['video_url']}","{news_record['description']}","{news_record['title']}","{news_record['file_name']}",{news_record['is_up']},{news_record['is_up_main']},{news_record['is_shorts']},{int(time.time())})'''
            try:
                cr=self.connection.cursor()
                x=cr.execute(cm)
                m+=1
            except:
                return 0
        self.connection.commit()
        return m
    def get_chanel_list(self):
        '''
        Возвращает список записей всех кканалов, каждый канал-tuple
        id , author , vk_group_api_key ,vk_group_id ,vk_main_group_api_key , vk_main_group_id , vk_playlist_key, last_post_time
        '''
        cm='SELECT * FROM Chanels'
        cr=self.connection.cursor()
        cr.execute(cm)
        chanels=cr.fetchall()
        return chanels
    def add_chanel(self,chanel):
        '''
        Добавляет канал, chanel-словарь ключи которого совпадают с полями таблицы
        id , author , vk_group_api_key ,vk_group_id ,vk_main_group_api_key , vk_main_group_id , vk_playlist_key , last_post_time , main_last_post_time
        возвращает 1 если успешно добавил канал
        '''
        cm=f'''INSERT INTO Chanels (id , author , vk_group_api_key , vk_group_id , vk_main_group_api_key , vk_main_group_id , vk_playlist_key, last_post_time, main_last_post_time) VALUES
        ("{chanel["id"]}","{chanel["author"]}","{chanel["vk_group_api_key"]}","{chanel["vk_group_id"]}","{chanel["vk_main_group_api_key"]}",
        "{chanel["vk_main_group_id"]}","{chanel["vk_playlist_key"]}",{chanel["last_post_time"]},{chanel["main_last_post_time"]})'''
        try:
            cr=self.connection.cursor()
            x=cr.execute(cm)
        except Exception as e:
            return e
        self.connection.commit()
        return 1
    def get_news_to_upload(self):
        '''
        Возвращает список туплей из всех новостей которые еще не загружаны хотябы куда-то
        id,chanel_id, vk_group_api_key, vk_group_id, vk_main_group_api_key, vk_main_group_id, vk_playlist_key,
        video_url, description,	title, file_name, is_up,is_up_main,is_short
        '''
        cm=f'SELECT * FROM News WHERE is_up=0 OR is_up_main=0;'
        cr=self.connection.cursor()
        cr.execute(cm)
        chanels=cr.fetchall()
        return chanels
    def mark_news_person_uploaded(self,id):
        '''
        Отмечает новость c id как загруженную в личную группу 
        возвращает 1 если успешно
        '''
        cm=f'UPDATE News SET is_up=1,last_use={int(time.time())} WHERE id="{id}"'
        try:
            cr=self.connection.cursor()
            x=cr.execute(cm)
        except Exception as e:
            return e
        self.connection.commit()
        return 1
    def mark_news_main_uploaded(self,id):
        '''
        Отмечает новость c id как загруженную в главную группу 
        возвращает 1 если успешно
        '''
        cm=f'UPDATE News SET is_up_main=1,last_use={int(time.time())} WHERE id="{id}"'
        try:
            cr=self.connection.cursor()
            x=cr.execute(cm)
        except Exception as e:
            return e
        self.connection.commit()
        return 1
    def get_author(self,chanel_id):
        '''
        Находит имя автора по id канала
        '''
        cm=f'SELECT author FROM Chanels where id="{chanel_id}" LIMIT 1'
        cr=self.connection.cursor()
        cr.execute(cm)
        a=cr.fetchone()
        return a[0]
    def set_post_time(self,chanel_id):
        '''
        устанавливает время последнего поста для канала chanel_id
        '''
        cm = f'UPDATE Chanels SET last_post_time={int(time.time())} WHERE id="{chanel_id}"'
        try:
            cr=self.connection.cursor()
            x=cr.execute(cm)
        except Exception as e:
            return e
        self.connection.commit()
        return 1
    def set_every_main_post_time(self):
        '''
        устанавливает время последнего поста в главной группе для всех канало(т.к. автора нет)
        '''
        cm = f'UPDATE Chanels SET main_last_post_time={int(time.time())}'
        try:
            cr=self.connection.cursor()
            x=cr.execute(cm)
        except Exception as e:
            return e
        self.connection.commit()
        return 1
    def set_main_post_time(self,chanel_id):
        '''
        устанавливает время последнего поста в основной группе из  канала chanel_id
        '''
        cm = f'UPDATE Chanels SET main_last_post_time={int(time.time())} WHERE id="{chanel_id}"'
        try:
            cr=self.connection.cursor()
            x=cr.execute(cm)
        except Exception as e:
            return e
        self.connection.commit()
        return 1
    def get_groups_last_post_time(self,tdelta):
        '''
        возвращает список туплей с last_post_time,vk_group_api_key,vk_group_id для всех каналов 
        у которых небыло постов больше секунд чем tdelta
        '''
        cm=f'SELECT last_post_time,vk_group_api_key,vk_group_id,id FROM Chanels WHERE {int(time.time())}-last_post_time>{tdelta} '
        cr=self.connection.cursor()
        cr.execute(cm)
        chanels=cr.fetchall()
        return chanels
    def get_main_last_post_time(self):
        '''
        возвращает время публикации последнего поста в основной группе, а также vk_main_group_api_key,vk_main_group_id
        '''
        cm=f'SELECT max(main_last_post_time) FROM Chanels'
        cr=self.connection.cursor()
        cr.execute(cm)
        a=cr.fetchone()
        cm=f'SELECT vk_main_group_api_key,vk_main_group_id FROM Chanels LIMIT 1'
        cr=self.connection.cursor()
        cr.execute(cm)
        b=cr.fetchone()
        return a[0],b[0],b[1]
    def delete_old_video(self,t,dir):
        '''
        удаляет файлы- с момента взаимодействия с которыми прошло больше t секунд- из директории dir
        заменяет имя файла в базе на @del
        '''
        t_now=int(time.time())
        cm=f'SELECT id,file_name FROM News WHERE is_up=1 and is_up_main=1 and file_name<>"@del" and abs(last_use-{t_now})>{t}'
        cr=self.connection.cursor()
        cr.execute(cm)
        news=cr.fetchall()
        ids,files=['\"'+x[0]+'\"' for x in news],[x[1] for x in news]
        cm=f'UPDATE News SET file_name ="@del" WHERE id in ({",".join(ids)})'
        try:
            cr=self.connection.cursor()
            x=cr.execute(cm)
        except Exception as e:
            return e
        self.connection.commit()
        print(files)
        for f in files:
            try:
                os.remove(dir+'/'+f)
            except:
                continue
        return 1

#mdb=data_transfer_from_db('grey_fox_1.db')
#print(mdb.delete_old_video(10,'C:/Users/koreshok_main/Videos/youtube_scrap'))
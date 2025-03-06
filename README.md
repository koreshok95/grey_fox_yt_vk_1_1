# grey_fox_yt_vk_1_1
Manager for Vk groups based on stollen youtube videos
require almost everything from requirments.txt + ffmpeg.exe and ffprobe.exe in the main project directory
Setteings .ini files describe
settings.ini - settings for yt_grey_fox_main.py
  path to database
  path to directory to store downloaded stolen youtube videos
  time in seconds between check and download new videos 
  number of attempts to download video
  number of attempts to generate rus  subtitles and hard burn  them in video
vk_settings.ini describe
vk_settings.ini - settings for vk_upload_app.py
  path to database
  path to directory to store downloaded stolen youtube videos
  time in seconds between check and upload new videos
  number of attempts to upload video
  app_key for stndalone vk app
  max time in seconds allowed between post in group, after exceeding it-generating template post
  directory to store templates for posts
Describe of apps
yt_grey_fox_main.py - get updates from rss xml over youtube chanels in database. Download and add video files(with rus subs)(using file storage) to database(grey_fox_1.db)
vk_upload_app.py - upload videos from database(grey_fox_1.db) and make posts in groups. if there are no any new videos from the chanel for over a certain time -<so no new posts in Vk group>-  ()-make random post from template
INSTAL
get python 3.10 - is optimal
install via pip everything from requirments.txt
install ffmpeg.exe and ffprobe.exe in the main project directory (https://ffmpeg.org/download.html#build-windows)
install git and wisper --- python -m pip install git+https://github.com/openai/whisper.git
install yt-dlp via pip
DATABASE DESCRIBE
Chanels-yotube chanels data to stole + data for target Vk group
  id - just id (chanel id in youtube)
  author - displayed in Vk name for youtube chanel
  vk_group_api_key - api key to post in group wall
  vk_group_id - id of group connected to chanel 
  vk_main_group_api_key - api key of group unifying all videos and content from all groups 
  vk_main_group_id - id of group unifying all videos and content from all groups 
  vk_playlist_key - playlist order number in main group - where stolen videos will uploads
  last_post_time - time stamp(seconds from 1970) for last post in this group
  main_last_post_time - time stamp(seconds from 1970) for last post in this main group
News - videos stolen from youtube and they status
  id - ust id (video id in youtube
  chanel_id - ust id (chanel id in youtube)
  vk_group_api_key -api key to post in group wall
  vk_group_id - id of group connected to chanel 
  vk_main_group_api_key - api key of group unifying all videos and content from all groups 
  vk_main_group_id - id of group unifying all videos and content from all groups
  vk_playlist_key - playlist order number in main group - where stolen videos will uploads
  video_url - url for download video
  description - description of video from rss? if its empty set to-   'Новое видео на канале'
  title - translated title of video 
  file_name - file name for video in filestorage
  is_up - flag (1)-video is uploaded to conected group 
  is_up_main - flag (1)-video is uploaded to main(group unifying all videos and content from all groups ) group 
  is_shorts - flag (1)-video duration is less then 3 min, and could bee vk_clip
Other Modules 
auto_sub_yt_dlp.py - functions for downloading videos? and hard burning rus subtitles
manual_load.py - manual video downloads and subtitles burning from youtube
rss_yt_parse.py - get essential info from xmls over youtube rss requests
vk_upload.py - class vk_manage_app to manage uploading video and posts
grey_fox+db.py - class data_transfer_from_db to make sql querys, create_new_base - create empty DB 

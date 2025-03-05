# grey_fox_yt_vk_1_1
Manager for Vk groups based on stollen youtube videos
require almost everything from requirments.txt + ffmpeg.exe and ffprobe.exe in the main project directory
Setteings .ini files describe
settings.ini - settings for yt_grey_fox_main.py
  path to database
  path to directory to store downloaded stolen youtube videos
  time in seconds between check and download new videos 
  number of attempts to download video
  number of attempts to generate  subtitles and hard burn in them video
vk_settings.ini
vk_settings.ini - settings for vk_upload_app.py
  path to database
  path to directory to store downloaded stolen youtube videos
  time in seconds between check and upload new videos
  number of attempts to upload video
  app_key for stndalone vk app
  max time in seconds allowed between post in group, after exceeding it-generating template post
  directory to store templates for posts
Describe of apps
yt_grey_fox_main.py - get updates from rss xml over youtube chanels in database. Download and add files(using file storage) to database(grey_fox_1.db)
vk_upload_app.py -upload videos from database(grey_fox_1.db) and make posts in groups
  

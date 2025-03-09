import yt_dlp
import os
from googletrans import Translator
import whisper
import subprocess
from datetime import timedelta
from uuid import uuid4
import json

#ссылка,папка для сохранения,число попыток загрузки=5,rname_output перименовывать файл видео
#return -1-ошибка загрузки, полный путь до файла
def yt_load(link,dir,ntrys=5,rname_output=True):
	"""
	загружает видео с ютуба по ссылке
	link-ссылка,dir-папка для сохранения,ntry-число попыток загрузки=5,rname_output перименовывать файл видео после загрузки
	return -1-ошибка загрузки, полный путь до файла
	сначала пытается скачать видео в 1080р, при неудаче в 720р
	"""
	yt_opts = {'outtmpl': f'{dir}%(title)s.%(ext)s','format':'bestvideo[height=1080]+bestaudio/best' }
	if dir[-1]!='/':
		dir+='/'
	while ntrys>0:
		try:
			with yt_dlp.YoutubeDL(yt_opts) as ydl:
				y=ydl.extract_info(link, download=True)
				fname = ydl.prepare_filename(y)
				ext=fname[fname.rfind('.'):]
				nname=f'{uuid4().hex}'
				if rname_output:
					os.rename(fname,f'{dir}{nname}{ext}')
					return f'{dir}{nname}{ext}'
				else:
					return fname
		except:
			ntrys-=1
			yt_opts['format']='bestvideo[height=720]+bestaudio/best'
	return -1


def gen_burn_sub(fpath,ntrys=3,del_sourse=True):
	"""
	создает субтиры и затем выжигает их на видео
	fpath полный путь к файлу,ntrys число попыток генирации,del_sourse-удалить исходное видео
	-1 ошибка, полный путь к созданому .mp4 файлу 
	"""
	while ntrys>0: 
		try:#подготовка моделей
			translator = Translator()
			model = whisper.load_model("small", device="cpu")
		except:
			ntrys-=1
			continue
		try:#создание файла субтитров
			audio = whisper.load_audio(fpath)
			result = model.transcribe(audio, language="en")
			lines=[]
			for i,x in enumerate(result['segments']):
				result = translator.translate(x['text'],src='en',dest='ru')
				x['text']=result.text
				startTime = str(0)+str(timedelta(seconds=int(x['start'])))+',000'
				endTime = str(0)+str(timedelta(seconds=int(x['end'])))+',000'
				text = x['text']
				text=text.replace('youtube','VK видео').replace('Youtube','VK видео').replace('YOUTUBE','VK видео').replace('YouTube','VK видео')
				lines.append(f'{i+1}\n')
				lines.append(f'{startTime} --> {endTime}\n')
				lines.append(f'{text}\n')
				lines.append('\n')
			with open(f'subs.srt','w',encoding='utf-8') as f:
				f.writelines(lines)
		except Exception as e:
			if os.path.isfile('subs.srt'):
				os.remove('subs.srt')
			ntrys-=1
			print(e)
			continue
		try:#выжигание субтитров
			ext=fpath[fpath.rfind('.'):]
			dir=os.path.dirname(fpath)
			nname=f'{uuid4().hex}'
			out_name=f'{dir}/{nname}.mp4'
			ffmpeg_command = f"""ffmpeg.exe -i {fpath} -vf "subtitles=subs.srt" {out_name}"""
			subprocess.run(ffmpeg_command)
		except Exception as e:
			if os.path.isfile('subs.srt'):
				os.remove('subs.srt')
			if os.path.isfile(out_name):
				os.remove(out_name)
			ntrys-=1
			print(e)
			continue
		if os.path.isfile('subs.srt'):
			os.remove('subs.srt')
		tmps=os.listdir()
		for j in tmps:
			ext=os.path.basename(j)[os.path.basename(j).rfind('.'):]
			if ext=='.tmp':
				os.remove(j)
		if del_sourse:
			if os.path.isfile(fpath):
				os.remove(fpath)
		return out_name
	return -1


def might_short(fpath):
	"""
	проверяет может ли скаченное видео быть шортом(короче ли оно 3 минут) fpath-путь к видео
	"""
	try:
		com=f'ffprobe.exe {fpath} -v error -show_format'
		res=subprocess.check_output(com)
		fn=str(res).split('\\r\\n')
		for j in fn:
			if 'duration=' in j:
				v=float(j.replace('duration=',''))
				return int(v+1)<180
		return False
	except:
		return False



import auto_sub_yt_dlp

def main():
    default_dir='C:/Users/koreshok_main/Videos/youtube_scrap'
    link_file=input('введите путь до файла с сылками (\\)->/ ')
    s=input(f'введите путь для папаки сохранения, поумолчанию {default_dir} ')
    if s!='':
        default_dir=s
    with open(link_file) as f:
        links=f.readlines()
    downs=[]
    for l in links:
        x=auto_sub_yt_dlp.yt_load(l,default_dir)
        downs.append(x)
    if len(downs)==0:
        x=input('введите полный путь к видео файлу, список с сылками пуст ')
        downs.append(x)
    for d in downs:
        auto_sub_yt_dlp.gen_burn_sub(d)

if __name__=='__main__':
    main()

import os
import requests
import csv
from bs4 import BeautifulSoup
from tqdm import *
import os.path

def exist_file_list():
    exist_files = []
    if not os.path.isdir('videos'):
        os.mkdir('videos')
    for file in os.listdir("videos"):
        if file.endswith(".mp4"):
            exist_files.append(file)
    return exist_files

def download_video_series(video_links, filename):
    exist_files = exist_file_list()
    for link in video_links:
        if link in exist_files:
            continue

        '''iterate through all links in video_links 
        and download them one by one'''

        # obtain filename by splitting url and getting
        # last string
        print("Downloading file: %s" % filename)

        # download started
        file_path = "videos/%s" % filename
        if not os.path.isdir('videos'):
            os.mkdir('videos')
        with requests.get(link, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                progress = tqdm(total=int(r.headers['Content-Length']))
                for chunk in r.iter_content(chunk_size=1024*1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
                        progress.update(len(chunk))

        print("\n%s download!\n" % filename)

    # print("All videos were downloaded!")
    return


def get_video_links():
    video_links = []
    file = "download/Ford_how_to_video_download.csv"
    with open(file, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count < 1:
                line_count += 1
                continue
            print(row[10])
            video_links.append(row[10])
    return video_links

def get_video_download_link(video_link):
    print(video_link)
    video_id = video_link.split("=")[-1]
    URL = "https://www.tubeoffline.com/downloadFrom.php?host=BrightCove&video=http://players.brightcove.net/2379864788001/default_default/index.html?videoId=%s" % video_id
    res = requests.get(url=URL).text
    soup = BeautifulSoup(res, 'html.parser')
    soup.find_all('tr')
    download_links = soup.find('div', {'id': 'videoDownload'})
    table = download_links.find('table')
    link = table.find_all('tr')[1].find('a')['href']
    print(link)
    return link

def remove_newline(file):
    if r'\n' in file:
        return remove_newline(file.rstrip("\\n"))
    return file

print("=================================Start================================")
if __name__ == "__main__":
    video_links = get_video_links()
    video_links = list(dict.fromkeys(video_links))
    for video_link in video_links:
        file = video_link.split("=")[-1]
        filename = remove_newline(file) + ".mp4"
        if os.path.isfile("videos/%s" % filename):
            print("This video was already downloaded!")
            continue
        download_link = get_video_download_link(video_link)
        download_video_series([download_link], filename)
    print("All videos were downloaded!")
print("=================================The End================================")
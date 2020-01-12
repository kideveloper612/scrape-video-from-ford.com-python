import csv

def video_from_file(path, filename, results):
    def write_csv(lines, filename):
        """
        Write lines to csv named as filename
        """
        import os
        import csv
        if not os.path.isdir('output'):
            os.mkdir("output")
        file_path = "output/%s" % filename
        with open(file_path, 'a', encoding='utf-8', newline='') as writeFile:
            writer = csv.writer(writeFile, delimiter=',')
            writer.writerows(lines)

    def dom_parser(URL):
        import requests
        res = requests.get(url=URL).text

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(res, 'html.parser')
        for item in soup.find_all():
            if "data-video-id" in item.attrs:
                return item["data-video-id"]
        return

    write_csv(lines=results, filename=filename)
    with open(path, "r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                print(line_count, row[8])
                video_id = dom_parser(URL=row[8])
                if video_id is not None:
                    video_download_url = "http://players.brightcove.net/2379864788001/B1eFuwPXkG_default/index.html?videoId=%s" % video_id
                    row.append(video_download_url)
                    print(row)
                    write_csv(lines=[row], filename=filename)
                    results.append(row)
                line_count += 1
    return results

results = [['YEAR', 'MAKE', 'MODEL', 'SECTION', 'SUB_SECTION', 'TITLE', 'DESCRIPTION', 'THUMBNAIL_URL', 'VIDEO_URL', 'VIDEO_DOWNLOAD_URL']]
file_path = 'test/Ford_how_to_video_Sorted.csv'
filename = "Ford_how_to_video_download_again.csv"
video_urls = video_from_file(path=file_path, filename=filename, results=results)
print(video_urls)

# def downloadVIDEO(url_link):
#     import urllib.request
#     import MediaInfo
#     urllib.request.urlretrieve(url_link, 'video_name')
#     fileInfo = MediaInfo.parse('video_name')
#     for track in fileInfo.tracks:
#         if track.track_type == "Video":
#             print("ok")
#
# url_link = "http://players.brightcove.net/2379864788001/B1eFuwPXkG_default/index.html?videoId=3569058990001"
# downloadVIDEO(url_link=url_link)


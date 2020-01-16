import requests
import os
import csv

sections = ['Dash & Interior', 'SYNC & Technology', 'Safety & Security', 'Under the Hood & Mechanics', 'Vehicle Care', 'Vehicle Exterior']
sub_sections = {
    'Dash & Interior': ['Comfort', 'Interior Features', 'Interior Technology'],
    'SYNC & Technology': ['Convenience', 'Entertainment', 'Mobile & Apps', 'SYNC', 'Safety'],
    'Safety & Security': ['Safety Equipment', 'Safety Features', 'Security'],
    'Under the Hood & Mechanics': ['Battery', 'Engine', 'Fluids', 'Mechanical'],
    'Vehicle Care': ['Exterior Care', 'Interior Care', 'Vehicle Health'],
    'Vehicle Exterior': ['Equipment', 'Lighting', 'Mechanical', 'Wheels']
}

def write_csv(lines, filename):
    """
    Write lines to csv named as filename
    """
    if not os.path.isdir('output'):
        os.mkdir("output")
    file_path = "output/%s" % filename
    with open(file_path, 'a', encoding='utf-8', newline='') as writeFile:
        writer = csv.writer(writeFile, delimiter=',')
        writer.writerows(lines)

def excute_each_request():
    csv_header = [['YEAR', 'MAKE', 'MODEL', 'SECTION', 'SUB_SECTION', 'SYNC_VERSION', 'TITLE', 'DESCRIPTION', 'THUMBNAIL_URL', 'VIDEO_URL']]
    filename = "Ford_how_to_video.csv"
    write_csv(csv_header, filename)
    def get_section_url(section):
        if '&' in section:
            sub_names = section.split(" ")
            sub_url = ''
            for sub_name in sub_names:
                if sub_name is '&':
                    sub_url = sub_url + '-' + 'and'
                else:
                    sub_url = sub_url + '-' + sub_name.lower()
        else:
            sub_names = section.split(" ")
            sub_url = ''
            for sub_name in sub_names:
                sub_url = sub_url + '-' + sub_name.lower()
        return sub_url

    def get_subsection_url(subsection):
        sub_names = subsection.split(" ")
        sub_url = ''
        for sub_name in sub_names:
            if sub_name is '&':
                sub_name = 'and'
            sub_url = "%s-%s" % (sub_url, sub_name.lower())
        return sub_url

    def json_request(url):
        res = requests.get(url=url).json()
        return res

    make = 'Ford'
    results = []
    for section in sections:
        section_url = get_section_url(section)
        for sub_section in sub_sections[section]:
            sub_section_url = get_subsection_url(sub_section)
            url = "https://owner.ford.com/support/ford/_jcr_content.cxht" + section_url + sub_section_url + '.json'
            print(url.strip())
            json_data = json_request(url)
            records = json_data['results']
            for record in records:
                title = record['title']
                description = ''
                if 'description' in record:
                    description = record['description']
                video_url = "https://owner.ford.com" + record['contentPath'] + '.html'
                thumbnail_url = "https://owner.ford.com" + record['pageThumbnail']
                tags = record['tags']
                for tag in tags:
                    vehicle_specify = tag.split("/")
                    print(vehicle_specify)
                    if (len(vehicle_specify) != 4):
                        try:
                            int(vehicle_specify[1])
                            year = vehicle_specify[1]
                            model = vehicle_specify[3]
                            sync_version = vehicle_specify[4]
                            line = [year, make, model, section, sub_section, sync_version, title, description, thumbnail_url, video_url]
                            print(line)
                            results.append(line)
                            write_csv([line], filename)
                        except:
                            year = ''
                            model = ''
                            sync_version = ''
                            line = [year, make, model, section, sub_section, sync_version, title, description, thumbnail_url, video_url]
                            print(line)
                            results.append(line)
                            write_csv([line], filename)
                    if (len(vehicle_specify) == 4):
                        try:
                            int(vehicle_specify[1])
                            year = vehicle_specify[1]
                            model = vehicle_specify[3]
                            sync_version = ''
                            line = [year, make, model, section, sub_section, sync_version, title, description, thumbnail_url, video_url]
                            print(line)
                            results.append(line)
                            write_csv([line], filename)
                        except:
                            year = ''
                            model = ''
                            sync_version = ''
                            line = [year, make, model, section, sub_section, sync_version, title, description, thumbnail_url, video_url]
                            print(line)
                            results.append(line)
                            write_csv([line], filename)
                    elif (vehicle_specify[1] == 'all'):
                        continue

    sorted_result = sorted(results, key=lambda x: (x[0], x[2]), reverse=True)
    write_csv([['YEAR', 'MAKE', 'MODEL', 'SECTION', 'SUB_SECTION', 'SYNC_VERSION' 'TITLE', 'DESCRIPTION', 'THUMBNAIL_URL', 'VIDEO_URL']], "Ford_how_to_video_Sorted.csv")
    write_csv(sorted_result, "Ford_how_to_video_Sorted.csv")

print('------------------------------Start------------------------------------')
excute_each_request()
print('------------------------------The End----------------------------------')
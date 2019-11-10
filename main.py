import pandas as pd
from configparser import ConfigParser
import xml.etree.cElementTree as ET


def add_track(data, vlc_id, root_element):
    track_element = ET.SubElement(root_element[1], "track")
    ET.SubElement(track_element, "location").text = f'dvb-t://frequency={data["frequency"]}:bandwidth=8'
    ET.SubElement(track_element, "title").text = f'{data["service_name"]}'
    extension = ET.SubElement(track_element, "extension", attrib={'application': 'http://www.videolan.org/vlc/playlist/0'})
    ET.SubElement(extension, "vlc:id").text = f'{vlc_id}'
    ET.SubElement(extension, "vlc:option").text = 'dvb_adapter=0'
    ET.SubElement(extension, "vlc:option").text = 'live-caching=300'
    ET.SubElement(extension, "vlc:option").text = 'sout=#display'
    ET.SubElement(extension, "vlc:option").text = 'no-sout-all'
    ET.SubElement(extension, "vlc:option").text = 'sout-keep'
    ET.SubElement(extension, "vlc:option").text = f'program={data["service_id"]}'
    formatted_tree = ET.ElementTree(root)
    formatted_tree.write("filename.xspf", xml_declaration=True, encoding="UTF-8")


config = ConfigParser()
config.read('channels_1.conf')
info = {}
for section in config.sections():
    info[section] = {k: v for k, v in config.items(section)}

df = pd.DataFrame(info)
# print(df)

ET.register_namespace('', 'http://xspf.org/ns/0/')
ET.register_namespace('vlc', 'http://www.videolan.org/vlc/playlist/ns/0/')

tree = ET.parse('mine.xspf')
root = tree.getroot()
# tracklist = root.find("trackList")
# for track in root[1]:
#     print(track.tag)
#     for track_attr in track.iter():
#         print(track_attr, track_attr.text)

for idx, column in enumerate(df):
    add_track(df[column], idx, root)

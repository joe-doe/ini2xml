import pandas as pd
from configparser import ConfigParser
import xml.etree.cElementTree as ET


config = ConfigParser()
config.read('channels_1.conf')
info = {}
for section in config.sections():
    info[section] = {k: v for k, v in config.items(section)}

df = pd.DataFrame(info)
print(df)

ET.register_namespace('', 'http://xspf.org/ns/0/')
ET.register_namespace('vlc', 'http://www.videolan.org/vlc/playlist/ns/0/')

tree = ET.parse('mine.xspf')
root = tree.getroot()
tracklist = root.find("trackList")
for track in root[1]:
    print(track.tag)
    for track_attr in track.iter():
        print(track_attr, track_attr.text)

track = ET.SubElement(root[1], "track")
location = ET.SubElement(track, "location").text = 'AAA'
title = ET.SubElement(track, "title").text = 'BBB'
extension = ET.SubElement(track, "extension", attrib={'application': 'http://www.videolan.org/vlc/playlist/0'})
id = ET.SubElement(extension, "vlc:id").text = '9999'
dvb_adapter = ET.SubElement(extension, "vlc:option").text = 'dvb_adapter=0'
live_caching = ET.SubElement(extension, "vlc:option").text = 'live-caching=300'
sout = ET.SubElement(extension, "vlc:option").text = 'sout=#display'
no_sout_all = ET.SubElement(extension, "vlc:option").text = 'no-sout-all'
sout_keep = ET.SubElement(extension, "vlc:option").text = 'sout-keep'
program = ET.SubElement(extension, "vlc:option").text = 'program=3066'

root = ET.tostring(root)
tree.write("filename.xml")

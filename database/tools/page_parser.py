from typing import Dict
from webbrowser import get
from bs4 import BeautifulSoup
import time
import re
import json

# 直接用 html 转 json 实在是太慢了
# 这边 parse 出来的另外一个 Link 会变成 Link(CoF)

get_ds = None

def get_data_from_div(div, link_searched):
    form = div.find(name="form")
    type_img = div.find(name="img", recursive=False)
    if type_img.attrs['src'].find("standard") != -1:
        type_ = "SD"
    else:
        type_ = "DX"
    def get_level_index(src: str):
        if src.find("remaster") != -1:
            return 4
        elif src.find("master") != -1:
            return 3
        elif src.find("expert") != -1:
            return 2
        elif src.find("advanced") != -1:
            return 1
        elif src.find("basic") != -1:
            return 0
    def get_music_icon(src: str):
        re = "https://maimai.wahlap.com/maimai-mobile/img/music_icon_"
        v = src.replace(re, "").replace(".png", "")
        return v if v != "back" else ""
    title = form.contents[7].string
    if title == "Link":
        link_searched = True
        title = "Link(CoF)"
    if len(form.contents) == 23:
        data = {
            "title": title,
            "level": form.contents[5].string,
            "level_index": get_level_index(form.contents[1].attrs['src']),
            "type": type_,
            "achievements": float(form.contents[9].string[:-1]),
            "dxScore": int(form.contents[11].string.strip().replace(',', '')),
            "rate": get_music_icon(form.contents[17].attrs['src']),
            "fc": get_music_icon(form.contents[15].attrs['src']),
            "fs": get_music_icon(form.contents[13].attrs['src']),
            "ds": 0
        }
        if get_ds is not None:
            data["ds"] = get_ds(data)
        return data, link_searched
    return None, link_searched

def html2json(html: str) -> Dict:
    soup = BeautifulSoup(html, "html.parser")
    link_searched = False
    j = []
    for div in soup.find_all(class_="w_450 m_15 p_r f_0"):
        v, link_searched = get_data_from_div(div, link_searched)
        if v is not None:
            j.append(v)
    return j

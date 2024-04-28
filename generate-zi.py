#!/usr/bin/env python3

import argparse
import glob
import numpy as np
import os
import pypdf

hanzi = [
    "藍紅黃粉黑白紫綠",
    "耳鼻目口手頭足齒舌肚屁皮身眉",
    "鼠牛虎兔龍蛇馬羊猴雞狗豬魚鳥蟲貓",
    "上下左右中東南西北",
    "春夏秋冬年月日",
    "爸媽爺奶公婆哥弟姐妹兒女子家",
    "大小高矮重輕",
    "天地人水雨雪山田雲電冰海",
    "做吃汏寫睏玩",
    "床卓燈門椅桶",
    "香臭好快樂老冷熱新尖遠近",
    "了不也的我你他",
    "木林竹葉花草石",
    "傘筷筆碗衣刀車書",
    "飛學笑看坐回畫",
    "米肉蘋果瓜糖",
    "出入有來去過",
    "金木水火土行",
]


parser = argparse.ArgumentParser(prog="30zi")
parser.add_argument(
    "-n", "--n_days", type=int, help="日數，即幾張題目", default=10,
)
parser.add_argument(
    "-m", "--name", type=str, help="學生的名字", default="",
)
args = parser.parse_args()
n_days = args.n_days
name = args.name

with open("30zi.tex", "r") as f_in:
    base = f_in.read()

def pick_zis():
    p = np.array([len(z) for z in hanzi])
    theme_id = np.random.choice(
        [i for i in range(len(hanzi))],
        1,
        p=p/np.sum(p),
    ).squeeze()
    theme = hanzi[theme_id]
    zi_ids = np.random.choice(np.arange(len(theme)), 6, replace=False)
    return [theme[i] for i in zi_ids]

def make_sheet():
    zis = pick_zis()
    sheet = base
    numerals = ["一", "二", "三", "四", "五", "六"]
    for i, zi in enumerate(zis):
        sheet = sheet.replace(numerals[i], zi)
    sheet = sheet.replace("〇〇〇", name)
    return sheet

for n in range(n_days):
    sheet = make_sheet()
    with open(f"30zi{n}.tex", "w") as f_out:
        f_out.write(sheet)

    os.system(f"xelatex 30zi{n}.tex")

merger = pypdf.PdfWriter()

for i in range(n_days):
    filename = f"30zi{i}.pdf"
    merger.append(filename)
    old_files = glob.glob(f"30zi{i}.*")
    for f in old_files:
        os.remove(f)

merger.write(f"30zi.pdf")
merger.close()
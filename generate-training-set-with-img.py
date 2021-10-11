"""
生成 ./data/training-set-with-img.json
格式如下:
[
    {
        'patient ID': 字符串,

        'gender', 'age', 'diagnosis', 'anti-VEGF',
        'preCST', 'preIRF', 'preSRF', 'prePED', 'preHRF',
        'continue injection', 'CST', 'IRF', 'SRF', 'PED',
        'HRF': 整数,

        'preVA', 'VA': 浮点数,

        // 该病人眼睛的 治疗前 OCT
        'img_before': [
            "./data/training-set-img/0000-0000L_1000.jpg",
            ......
        ],

        // 该病人眼睛的 治疗后 OCT
        'img_after': [
            "./data/training-set-img/0000-0000L_2000.jpg",
            ......
        ]
    },
    ......
]
"""

import os
from util import read_csv, write_json

data_json = []
fieldnames, row_list = read_csv("./data/training-set.csv")
all_img_name = []


def main():
    fill_all_img_name()
    fill_data_json()
    write_json(data_json, './data/training-set-with-img.json', indent=4)


def fill_all_img_name():
    for root, dirs, files in os.walk('./data/training-set-img'):
        for filename in files:
            name, ext = filename.split('.')
            if ext != 'jpg':
                continue
            
            all_img_name.append(name)


def fill_data_json():
    for row in row_list:
        for field in [
            "gender", "age", "diagnosis", "anti-VEGF", "preCST",
            "preIRF", "preSRF", "prePED", "preHRF", "continue injection",
            "CST", "IRF", "SRF", "PED", "HRF",
        ]:
            row[field] = int(row[field])
        
        row["preVA"] = float(row["preVA"])
        row["VA"] = float(row["VA"])

        row["img_before"], row["img_after"] = find(row["patient ID"])

        data_json.append(row)


def find(pid: str):
    before = []
    after = []
    pid_len = len(pid)

    for i, img_name in enumerate(all_img_name):
        if img_name == None:
            continue
        
        if not img_name.startswith(pid):
            continue

        is_before = img_name[pid_len+1:pid_len+2] == '1'
        if is_before:
            before.append(f'./data/training-set-img/{img_name}.jpg')
        else:
            after.append(f'./data/training-set-img/{img_name}.jpg')
        
        all_img_name[i] = None
    
    return before, after

main()

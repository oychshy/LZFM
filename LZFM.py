# coding:utf-8
import string
import time
import json

import requests,os,json

import datetime

header = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1"}

def getInfo(id):
    url = 'https://m.lizhi.fm/vodapi/voice/info/%s' % str(id)

    data = requests.get(url, verify=False).json()
    imageUrl = data["data"]["userVoice"]["voiceInfo"]["imageUrl"]
    arr = imageUrl.split('/') 

    # trackUrl = data["data"]["userVoice"]["voicePlayProperty"]["trackUrl"]
    # arr = trackUrl.split('/')
    # trackUrl = "http://cdn101.mlychee.com/audio/%s/%s/%s/%s_hd" % (arr[4], arr[5], arr[6], str(id))
    trackUrl = "http://cdn101.lizhi.fm/audio/%s/%s/%s/%s_hd" % (arr[4], arr[5], arr[6], str(id))
    # print(trackUrl)
    # http://cdn5.lizhi.fm/audio/2023/06/28/3016633883001578502_hd.mp3
    # https://cdnimg103.lizhi.fm/audio_cover/2023/06/28/3016633884842672647_320x320.jpg
    return trackUrl



def download():
    url = "http://cdn101.mlychee.com/audio/2022/12/31/2983421190812067846_hd"
    data = requests.get(url, verify=False).content
    m4a_path = '/Users/apple/Downloads/utils/xmly/downloadFiles/黑水/'
    if not os.path.exists(m4a_path):
        os.makedirs(m4a_path)
    filename = os.path.join(m4a_path, 'test.m4a')
    with open(filename,'wb') as f:
        f.write(data)
    print("end")


def search():
    # 超游 5328759026536678444
    # 怡乐 2513816802261356588
    # 四维 5042636793579506220
    # 黑水 2510677374229703724
    # 天才 2520458120928849452
    # 黑猫 5192049244676804652
    # 春典 5301798855332851756
    # 毛嗑 6246399
    uid = 5328759026536678444
    page = 1
    audios = []
    currentCount = 0

    while 1:
        url = "https://www.lizhi.fm/api/user/audios/%s/%s" % (str(uid),str(page))
        data = requests.get(url, verify=False, headers=header).json()
        total = data[u"total"]
        if currentCount >= total:
            break
        getDatas = data["audios"]
        currentCount += len(getDatas)
        print(currentCount,"/",total)

        for audioInfo in getDatas:
            payFlag = audioInfo["payFlag"]

            if payFlag == 1:
                dataInfo = {}
                dataInfo["name"] = audioInfo["name"]
                dataInfo["id"] = audioInfo["id"]

                id = dataInfo["id"]
                trackUrl = getInfo(id)
                audioInfo['url'] = trackUrl
                print(audioInfo)
            else:
                print(audioInfo)

        time.sleep(1)
        page += 1

    print(audios)

def checkUrl(trackUrl,sid):
    ret = False
    newtrackUrl = ''

    arr = trackUrl.split('/')
    year = int(arr[4])
    mon = int(arr[5])
    day = int(arr[6])

    end = datetime.date(year, mon, day)
    first = end.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    begin = datetime.date(last_month.year, last_month.month, 1)

    delta = datetime.timedelta(days=1)

    d = end
    while d >= begin:
        # getMon = ''
        # getDay = ''
        if len(str(d.month)) == 1:
             getMon = "0%s"%(d.month)
        else:
            getMon = d.month
        if len(str(d.day)) == 1:
            getDay = "0%s" % (d.day)
        else:
            getDay = d.day

        newtrackUrl = "http://cdn101.lizhi.fm/audio/%s/%s/%s/%s_hd" % (d.year, getMon, getDay, str(sid))
        html = requests.head(newtrackUrl)
        re = html.status_code
        # print(re)
        if re == 200:
            ret = True
            break
        # else:
        #     print("false:",newtrackUrl)
        d -= delta

    return ret,newtrackUrl




if __name__ == '__main__':

    search()
    



#记得修改42，58，65行为自己的信息

from requests import get
import json 
import os
import mail

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
}

#bv解码部分
table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
    tr[table[i]]=i
s=[11,10,3,8,4,6,2,9,5,7]
xor=177451812
add=100618342136696320
#bv2av
def dec(x):
    r=0
    for i in range(10):
        r+=tr[x[s[i]]]*58**i
    return (r-add)^xor


def getp(bvid):
    pjson = get("http://api.bilibili.com/x/player/pagelist?bvid={bvid}".format(bvid=bvid))
    pinfo = json.loads(pjson.text)
    pnum = len(pinfo["data"])
    return pnum


# 视频下载并持久化函数
def down(k):
    global v_dic
    dir = v_dic[k]
    old_dir = os.getcwd()
    new_dir = r"onedrive的挂载地址{dir}".format(dir=dir.replace("/","|"))
    p = getp(k)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    os.chdir(new_dir)
    print("正在下载{k}".format(k=v_dic[k]))
    if p == 1:
        command = r"you-get --format=flv https://www.bilibili.com/video/av{k}".format(k=dec(k))
        r = os.system(command)
    else:
        for i in range(p):
            command = r"you-get --format=flv --playlist https://www.bilibili.com/video/av{k}?p={p}".format(k=dec(k),p=i+1)
            r = os.system(command)
    if  r == 0:
        print(k+"下载成功")
        #如不需要邮件提醒功能，请删除下面一行。
        mail.sendmail("通知的邮件地址","BiliDown任务通知","「{k}」下载成功，请打开onedrive查看".format(k=v_dic[k]))
        os.chdir(old_dir)
    else:
        print(k+"下载失败")


#获取收藏列表
down_list_url = "收藏夹接口地址"
down_urls = json.loads(get(url=down_list_url,headers=headers).text)
medias = down_urls["data"]["medias"]
v_dic ={}
for i in medias:
    v_dic[i["bvid"]] = i['title']

#下载不在json列表中的视频。
os.chdir("/home/python")
with open("v_list.json","r") as f:
    v_list_old = json.loads(f.read())
    for k in v_dic.keys():
        if not k in v_list_old.keys():
            down(k)
        with open("/home/python/v_list.json","w") as f:
            f.write(json.dumps(v_dic))

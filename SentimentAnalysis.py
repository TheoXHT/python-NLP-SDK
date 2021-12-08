# 调用腾讯SDK
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.nlp.v20190408 import nlp_client, models

# 窗口GUI库
from tkinter import *
import tkinter.messagebox

# 调用者设置
# SecretId = "AKIDoU0OchdOzRggbN7oLl3DE9uTr56vUoun"
# SecretKey = "jSCuX6au1ulXEl6C7qMoDWr7I2hM2e8c"

# 获取识别结果
def get_res(text,flag,mode,SecretId,SecretKey):
    try:
        # 设置签名串SecretId和SecretKey
        cred = credential.Credential(SecretId, SecretKey)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "nlp.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = nlp_client.NlpClient(cred, "ap-guangzhou", clientProfile)

        req = models.SentimentAnalysisRequest()
        params = {
            "Text": text,
            "Flag": flag,
            "Mode": mode
        }
        req.from_json_string(json.dumps(params))

        resp = client.SentimentAnalysis(req)
        # print(resp.to_json_string())

        return resp.to_json_string()
    except TencentCloudSDKException as err:
        print(err)
        return None


# 展示分析内容
def show_content(dict):
    text.delete('1.0', 'end')
    for key, value in dict.items():
        text_value = str(key) + " : " + str(value)
        text.insert(INSERT,text_value + '\n')


def check(text,flag,mode,SecretId,SecretKey):

    if(text == ""):
        check_empty = tkinter.messagebox.askokcancel(title='Error', message='输入内容不能为空！')
        return False
    # 参数输入检查
    if(flag not in [1,2,3,4]):
        check_empty = tkinter.messagebox.askokcancel(title='Error', message='Flag参数有误')
        return False
    if(mode not in ["2class","3class"]):
        check_empty = tkinter.messagebox.askokcancel(title='Error', message='Mode参数有误')
        return False

    if(SecretId == "" or SecretKey == ""):
        check_empty = tkinter.messagebox.askokcancel(title='Error', message='用户签名串不能为空')
        return False

    return True

# 获取输入信息并展示
def getter_and_shower():
    # 获取输入框信息
    texts = aim_text.get()
    flag = int(Flag.get())
    mode = Mode.get()
    id = SecretId.get()
    key = SecretKey.get()
    print("检测内容：%s\t\tFlag参数：%d\t\tMode参数：%s"%(texts,flag,mode))
    # 参数输入正确性检查
    if(check(texts,flag,mode,SecretId,SecretKey) == False):
        return
    # 调用腾讯API获取结果
    res = get_res(texts,flag,mode,id,key)
    print(type(res))
    if(res == None):
        print("调用API失败，返回NONE")
        check_empty = tkinter.messagebox.askokcancel(title='Error', message='调用失败，请检查您的ID,KEY是否正确')
        return
    # 打印结果
    print(res)
    # 将结果转为dict字典形式
    dict_res = json.loads(res)
    # 结果打印到窗口上
    for key, value in dict_res.items():
        print(key," : ",value)
    show_content(dict_res)


def setinfo():
    print("设置用户ID和KEY")


# 创建窗口
win = Tk()
# 设置窗口标题
win.title('情感分析0.1.0')
# 设置窗口宽度和高度
win.geometry('720x480')
# 不允许改变宽和高
win.wm_resizable(False, False)


# 身份识别
id = StringVar()
id.set("")
key = StringVar()
key.set("")
Label(text="SecretId:").place(x=50, y=10)
Label(text="SecretKey:").place(x=50, y=40)
SecretId = Entry(win, textvariable=id, justify='center')
SecretId.place(x=158, y=10, width=405)
SecretKey = Entry(win, textvariable=key, justify='center',show='*')
SecretKey.place(x=158, y=40, width=405)

# 分析内容
Label(text="分析内容:").place(x=50, y=35+40)
aim_text = Entry(win, width=50)
aim_text.place(relx=0.5, rely=0.18, anchor=CENTER)
# 结果内容
text = Text(win, width=45, height=5, font=('Arial', 13), fg='blue')
text.place(relx=0.5, rely=0.7, anchor=CENTER)
# 参数设置
Label(text="Flag:").place(x=50, y=75+40)
Label(text="Mode:").place(x=50, y=150+40)
# Flag = Entry(win)
# Flag.place(x=100,y=75,width=50)
# 参数输入框
t1 = StringVar()
t1.set(4)
t2 = StringVar()
t2.set("2class")
Flag = Entry(win, textvariable=t1, justify='center')
Flag.place(x=100, y=76+40, width=50)
Mode = Entry(win, textvariable=t2, justify='center')
Mode.place(x=100, y=150+40, width=50)
# 提示
Label(text="(Flag输入 Integer类型):1、商品评论类 2、社交类 3、美食酒店类 4、通用领域类").place(x=50, y=100+40)
Label(text="注：待分析文本所属的类型，仅当输入参数Mode取值为2class时有效（默认值取4）").place(x=50, y=125+40)
Label(text="(Mode输入 String类型):1、2class：返回正负面二分类情感结果 2、3class：返回正负面及中性三分类情感结果").place(x=50, y=175+40)
Label(text="注：情感分类模式选项，可取2class或3class（默认值为2class）").place(x=50, y=200+40)
# 按钮
B = Button(win, text="确认", command=getter_and_shower, font=('Increase font', 10), fg='black'
           , width=10).place(x=600, y=36+38)

# select_info = Button(win, text="设置ID和KEY", command=setinfo, font=('Increase font', 10), fg='black'
#            , width=15).place(x=580, y=86+38)

# 主程序
win.mainloop()




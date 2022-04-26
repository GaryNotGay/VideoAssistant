# @Author  :  lijishi
# @Contact :  lijishi@163.com
# @Software:  Pycharm & Python 3.9.5
# @EditTime:  Apr 26, 2022
# @Version :  1.0
# @Describe:  Video Transcode Based On FFMPEG
# @LICENSE :  GNU GENERAL PUBLIC LICENSE Version 3

import os
import sys
import time
import base64
import tkinter
import webbrowser
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import END
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext

GUI_VER = "1.0"


def SelectPath_In():
    path_ = tkinter.filedialog.askopenfilename()
    #print(path_)
    path_ = path_.replace("/", "\\\\")
    path_in.set(path_)
    string = path_
    i = string.rfind("\\\\")
    string = string[:i+2]
    path_out.set(string)

def SelectPath_Out():
    path_ = tkinter.filedialog.askdirectory()
    path_ = path_.replace("/", "\\\\")
    path_out.set(path_)

def Selectsubtitle():
    path_ = tkinter.filedialog.askopenfilename()
    path_ = path_.replace("/", "\\\\")
    if JudgeFileType("subtitle", path_):
        add_subtitle_path.set(path_)
    else:
        tk.messagebox.showerror("Error!!!", "字幕格式错误，当前仅支持.srt/.ass格式")

def JudgeFileType(type, file):
    format = file.split(".")[-1]
    videoarr = ["mp4", "mkv", "ts", "flv"]
    subtitlearr = ["srt", "ass"]
    if type == "subtitle":
        if format in subtitlearr:
            return True
    elif type == "video":
        if format in videoarr:
            return True
    return False

def getCurPath():
    curpath = os.getcwd()
    return curpath

def getTime():
    return str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))

def About():
    # window centered
    about_window = Toplevel()
    screen_width = about_window.winfo_screenwidth()
    screen_heigh = about_window.winfo_screenheight()
    about_window_width = 350
    about_window_heigh = 210
    x = (screen_width - about_window_width) / 2
    y = (screen_heigh - about_window_heigh) / 2
    about_window.geometry("%dx%d+%d+%d" % (about_window_width, about_window_heigh, x, y))

    # window layout
    about_window.title('About')
    about_window.iconbitmap('va128.ico')
    global va_png
    va_png = tk.PhotoImage(file="va64.png")
    software_frame = ttk.LabelFrame(about_window, text='Software Info')
    software_frame.grid(row=0, column=0, rowspan=5, columnspan=4, padx=50, pady=5)
    ttk.Label(software_frame, image=va_png, compound='left').grid(row=0, rowspan=3, column=0)
    ttk.Label(software_frame, text="Video Assistant V{ver}".format(ver=GUI_VER)).grid(row=0, column=1, sticky = W)
    ttk.Label(software_frame, text="@Author    :   lijishi").grid(row=1, column=1, sticky = W)
    ttk.Label(software_frame, text="@EditTime  :   Apr 26, 2022").grid(row=2, column=1, sticky = W)

    copyright_frame = ttk.LabelFrame(about_window, text='LICENSE Info')
    copyright_frame.grid(row=5, column=0, rowspan=3, columnspan=4, padx=50, pady=5)
    ttk.Label(copyright_frame, text = "Github @ VideoAssistant").grid(row=5, column=0)
    ttk.Label(copyright_frame, text="GNU GENERAL PUBLIC LICENSE Version 3").grid(row=6, column=0)

    ttk.Button(about_window, text="更新日志", command=Renew_Log).grid(row=8, column=0, pady=5, sticky = E)
    ttk.Button(about_window, text="官方主页", command=Software_Web).grid(row=8, column=3, pady=5, sticky = W)

def Renew_Log():
    tk.messagebox.showinfo("更新日志", "V1.0 更新日期：20220426\n首次发布！欢迎下载使用，多提意见多交流！\n官方主页：https://github.com/GaryNotGay/VideoAssistant")

def Software_Web():
    url = "https://github.com/GaryNotGay/VideoAssistant"
    webbrowser.open_new(url)

def Main_Tip():
    tk.messagebox.showinfo("Tip", "一款基于FFmpeg的开源视频操作软件\n目前支持单视频的转码等基础操作\n更多帮助详见使用文档：https://github.com/GaryNotGay/VideoAssistant")

def FinalGo():
    #cmdpath = "cd \"getCurPath()\" "
    os.environ["WORKON_HOME"] = getCurPath()
    cmd = Command()
    os.system(cmd)
    return True

def CommandPreview():
    scr.delete(1.0, END)
    scr.insert("end", Command())
    return True

def Command():
    commandstr = "ffmpeg.exe -y -i \"" + str(path_in.get()) + "\""

    if vencode_change_status.get():
        vencode_change_formatarr = ["h264", "libx264", "hevc", "", "h264_nvenc", "hevc_nvenc"]
        if not vencode_change_todoformat.get() == 3:
            commandstr += " -vcodec " + vencode_change_formatarr[vencode_change_todoformat.get()]
        else:
            commandstr += " -vcodec " + vencode_change_otherformat.get()

    if ratio_change_status.get():
        ratio_change_formatarr = ["1280x720", "1920x1080", "2560x1440", "3840x2160", ""]
        if not ratio_change_todoformat.get() == 4:
            commandstr += " -s " + ratio_change_formatarr[ratio_change_todoformat.get()]
        else:
            commandstr += " -s " + ratio_change_otherformat.get()

    if not (vencode_change_status.get() or ratio_change_status.get()):
        commandstr += " -vcodec copy"

    if aencode_change_status.get():
        aencode_change_formatarr = ["aac", "ac3", "eac3", "", "mp3", "flac", "pcm_s16le"]
        if not aencode_change_todoformat.get() == 3:
            commandstr += " -acodec " + aencode_change_formatarr[aencode_change_todoformat.get()]
        else:
            commandstr += " -acodec " + aencode_change_otherformat.get()
    else:
        commandstr += " -acodec copy"

    if vbitrate_change_status.get():
        vbitrate_change_formatarr = ["2000", "3000", "4000"]
        if not  vbitrate_change_todoformat.get() == 3:
            commandstr += " -b:v " + vbitrate_change_formatarr[vbitrate_change_todoformat.get()]
        else:
            ommandstr += " -b:v " + vbitrate_change_otherformat.get()

    if abitrate_change_status.get():
        abitrate_change_formatarr = ["128", "320", "640"]
        if not abitrate_change_todoformat.get() == 3:
            commandstr += " -b:a " + abitrate_change_formatarr[abitrate_change_todoformat.get()]
        else:
            commandstr += " -b:a " + abitrate_change_otherformat.get()

    if add_subtitle_status.get():
        commandstr += " -vf subtitle=" + add_subtitle_path

    if hdr2sdr_status.get():
        if add_subtitle_status.get():
            commandstr += " zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv -pix_fmt yuv420p"
        else:
            commandstr += " -vf zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv -pix_fmt yuv420p"

    if format_change_status.get():
        outformatarr = ["mp4", "mkv", "mp3", "flac"]
        if not format_change_todoformat.get() == 4:
            outformat = outformatarr[format_change_todoformat.get()]
        else:
            outformat = format_change_otherformat.get()
    else:
        outformat = str(path_in.get()).split("\\")[-1].split(".")[-1]

    '''
    if vencode_change_status.get():
        outformat = str(path_in.get()).split("\\")[-1].split(".")[-1]
    '''

    videoname = str(path_in.get()).split("\\")[-1][:str(path_in.get()).split("\\")[-1].rfind(".")] + "_convert" + getTime() + "."
    commandstr += " \"" + str(path_out.get()) + videoname + outformat + "\""

    return commandstr


# window centered
main_window=tk.Tk()
screen_width = main_window.winfo_screenwidth()
screen_heigh = main_window.winfo_screenheight()
main_window_width = 610
main_window_heigh = 660
x = (screen_width-main_window_width) / 2
y = (screen_heigh-main_window_heigh) / 2
main_window.geometry("%dx%d+%d+%d" %(main_window_width,main_window_heigh,x,y))

main_window.title("Video Assistant V{ver}".format(ver=GUI_VER))
main_window.iconbitmap('va128.ico')
#ttk.Button(width = 15, text = "关于", command = About).grid(row = 7, column = 2, padx=10, pady=5)

path_frame = ttk.LabelFrame(main_window, text = '路径选择')
path_frame.grid(row = 0, column = 0, rowspan = 2, columnspan = 2, padx=5, pady=5)
path_in = tk.StringVar()
path_out = tk.StringVar()
path_in.set("请选择源视频位置，也可在框中键入")
path_out.set("请选择输出视频位置，默认为源视频路径")
ttk.Label(path_frame, text = "源视频位置").grid(row = 0, column = 0, padx=5)
ttk.Entry(path_frame, width = 40, textvariable = path_in).grid(row = 0, column = 1, padx=5)
ttk.Button(path_frame, text = "选择", command = SelectPath_In).grid(row = 0, column = 2, padx=5)
ttk.Label(path_frame, text = "输出视频位置").grid(row = 1, column = 0, padx=5)
ttk.Entry(path_frame, width = 40, textvariable = path_out).grid(row = 1, column = 1, padx=5)
ttk.Button(path_frame, text = "选择", command = SelectPath_Out).grid(row = 1, column = 2, padx = 5, pady = 5)

help_frame = ttk.LabelFrame(main_window, text = '使用帮助')
help_frame.grid(row = 0, column = 3, rowspan = 2, columnspan = 1, padx=5, pady=5)
ttk.Button(help_frame, text = "提示", command = Main_Tip).grid(row = 0, column = 3, padx = 5)
ttk.Button(help_frame, text = "关于", command = About).grid(row = 1, column = 3, padx = 5, pady = 5)

base_frame = ttk.LabelFrame(main_window, text = '基础功能设置')
base_frame.grid(row = 5, column = 0, columnspan = 4, padx=5, pady=5)

# 格式转换
format_change_status = tk.IntVar()
format_change_status.set(0)
format_change = ttk.Checkbutton(base_frame, text='格式转换', variable=format_change_status).grid(row=6, column=0, padx=5, pady=5)
ttk.Label(base_frame, text = "目标格式").grid(row=6, column=1, padx=5, pady=5)
format_change_todoformat = tk.IntVar()
format_change_otherformat = tk.StringVar()
format_change_todoformat.set(0)
tk.Radiobutton(base_frame, text="mp4", variable=format_change_todoformat, value=0).grid(row=6, column=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="mkv", variable=format_change_todoformat, value=1).grid(row=6, column=3, padx=5, pady=5)
tk.Radiobutton(base_frame, text="mp3", variable=format_change_todoformat, value=2).grid(row=6, column=4, padx=5, pady=5)
tk.Radiobutton(base_frame, text="flac", variable=format_change_todoformat, value=3).grid(row=6, column=5, padx=5, pady=5)
tk.Radiobutton(base_frame, text="其他", variable=format_change_todoformat, value=4).grid(row=6, column=6, pady=5)
ttk.Entry(base_frame, width=10, textvariable=format_change_otherformat).grid(row=6, column=7, padx=5, pady=5)

# 分辨率转换
ratio_change_status = tk.IntVar()
ratio_change_status.set(0)
ratio_change = ttk.Checkbutton(base_frame, text='分辨率转换', variable=ratio_change_status).grid(row=7, column=0, padx=5, pady=5)
ttk.Label(base_frame, text = "目标分辨率").grid(row=7, column=1, padx=5, pady=5)
ratio_change_todoformat = tk.IntVar()
ratio_change_otherformat = tk.StringVar()
ratio_change_todoformat.set(0)
tk.Radiobutton(base_frame, text="1280x720(720P)", variable=ratio_change_todoformat, value=0).grid(row=7, column=2, columnspan=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="1920x1080(1080P)", variable=ratio_change_todoformat, value=1).grid(row=7, column=4, columnspan=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="2560x1440(2K)", variable=ratio_change_todoformat, value=2).grid(row=7, column=6, columnspan=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="3840x2160(4K)", variable=ratio_change_todoformat, value=3).grid(row=8, column=2, columnspan=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="自定义分辨率(宽x高)", variable=ratio_change_todoformat, value=4).grid(row=8, column=4, columnspan=2, pady=5)
ttk.Entry(base_frame, width=15, textvariable=ratio_change_otherformat).grid(row=8, column=6, columnspan=4, padx=5, pady=5)

# 视频重编码
vencode_change_status = tk.IntVar()
vencode_change_status.set(0)
vencode_change = ttk.Checkbutton(base_frame, text='视频编码', variable=vencode_change_status).grid(row=9, column=0, padx=5, pady=5)
ttk.Label(base_frame, text = "目标编码").grid(row=9, column=1, padx=5, pady=5)
vencode_change_todoformat = tk.IntVar()
vencode_change_otherformat = tk.StringVar()
tk.Radiobutton(base_frame, text="h264", variable=vencode_change_todoformat, value=0).grid(row=9, column=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="libx264", variable=vencode_change_todoformat, value=1).grid(row=9, column=3, padx=5, pady=5)
tk.Radiobutton(base_frame, text="hevc", variable=vencode_change_todoformat, value=3).grid(row=9, column=4, padx=5, pady=5)
tk.Radiobutton(base_frame, text="其他", variable=vencode_change_todoformat, value=4).grid(row=9, column=5, pady=5)
ttk.Entry(base_frame, width=15, textvariable=vencode_change_otherformat).grid(row=9, column=6, columnspan=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="h264_nvenc(N卡)", variable=vencode_change_todoformat, value=5).grid(row=10, column=2, columnspan=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="hevc_nvenc(N卡)", variable=vencode_change_todoformat, value=6).grid(row=10, column=4, columnspan=2, padx=5, pady=5)
ttk.Label(base_frame, text = "<-确认支持硬件编码").grid(row=10, column=6, columnspan=2, padx=5, pady=5)

# 视频码率
vbitrate_change_status = tk.IntVar()
vbitrate_change_status.set(0)
vbitrate_change = ttk.Checkbutton(base_frame, text='视频码率', variable=vbitrate_change_status).grid(row=11, column=0, padx=5, pady=5)
ttk.Label(base_frame, text = "目标码率").grid(row=11, column=1, padx=5, pady=5)
vbitrate_change_todoformat = tk.IntVar()
vbitrate_change_otherformat = tk.StringVar()
vbitrate_change_otherformat.set("单位kb/s 无需填写")
tk.Radiobutton(base_frame, text="2000", variable=vbitrate_change_todoformat, value=0).grid(row=11, column=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="3000", variable=vbitrate_change_todoformat, value=1).grid(row=11, column=3, padx=5, pady=5)
tk.Radiobutton(base_frame, text="4000", variable=vbitrate_change_todoformat, value=2).grid(row=11, column=4, padx=5, pady=5)
tk.Radiobutton(base_frame, text="其他", variable=vbitrate_change_todoformat, value=3).grid(row=11, column=5, pady=5)
ttk.Entry(base_frame, width=15, textvariable=vbitrate_change_otherformat).grid(row=11, column=6, columnspan=2, padx=5, pady=5)
#ttk.Label(base_frame, text = "kb/s").grid(row=11, column=7, padx=5, pady=5)


# 音频重编码
aencode_change_status = tk.IntVar()
aencode_change_status.set(0)
vencode_change = ttk.Checkbutton(base_frame, text='音频编码', variable=aencode_change_status).grid(row=12, column=0, padx=5, pady=5)
ttk.Label(base_frame, text = "目标编码").grid(row=12, column=1, padx=5, pady=5)
aencode_change_todoformat = tk.IntVar()
aencode_change_otherformat = tk.StringVar()
abitrate_change_todoformat = tk.IntVar()
abitrate_change_otherformat = tk.StringVar()
tk.Radiobutton(base_frame, text="aac", variable=aencode_change_todoformat, value=0).grid(row=12, column=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="ac3", variable=aencode_change_todoformat, value=1).grid(row=12, column=3, padx=5, pady=5)
tk.Radiobutton(base_frame, text="eac3", variable=aencode_change_todoformat, value=2).grid(row=12, column=4, padx=5, pady=5)
tk.Radiobutton(base_frame, text="其他", variable=abitrate_change_todoformat, value=3).grid(row=12, column=5, pady=5)
ttk.Entry(base_frame, width=15, textvariable=abitrate_change_otherformat).grid(row=12, column=6, columnspan=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="mp3", variable=aencode_change_todoformat, value=4).grid(row=13, column=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="flac", variable=aencode_change_todoformat, value=5).grid(row=13, column=3, padx=5, pady=5)
tk.Radiobutton(base_frame, text="wav(pcm_s16le)", variable=aencode_change_todoformat, value=6).grid(row=13, column=4, columnspan=2, padx=5, pady=5)
ttk.Label(base_frame, text = "<-选择输出对应格式").grid(row=13, column=6, columnspan=2, padx=5, pady=5)

# 音频码率
abitrate_change_status = tk.IntVar()
abitrate_change_status.set(0)
abitrate_change = ttk.Checkbutton(base_frame, text='音频码率', variable=abitrate_change_status).grid(row=14, column=0, padx=5, pady=5)
ttk.Label(base_frame, text = "目标码率").grid(row=14, column=1, padx=5, pady=5)
abitrate_change_todoformat = tk.IntVar()
abitrate_change_otherformat = tk.StringVar()
abitrate_change_otherformat.set("单位kb/s 无需填写")
tk.Radiobutton(base_frame, text="128", variable=abitrate_change_todoformat, value=0).grid(row=14, column=2, padx=5, pady=5)
tk.Radiobutton(base_frame, text="320", variable=abitrate_change_todoformat, value=1).grid(row=14, column=3, padx=5, pady=5)
tk.Radiobutton(base_frame, text="640", variable=abitrate_change_todoformat, value=2).grid(row=14, column=4, padx=5, pady=5)
tk.Radiobutton(base_frame, text="其他", variable=abitrate_change_todoformat, value=3).grid(row=14, column=5, padx=5, pady=5)
ttk.Entry(base_frame, width=15, textvariable=abitrate_change_otherformat).grid(row=14, column=6, columnspan=2, padx=5, pady=5)
#ttk.Label(base_frame, text = "kb/s").grid(row=11, column=7, padx=5, pady=5)


pro_frame =  ttk.LabelFrame(main_window, text = '高级功能设置')
pro_frame.grid(row=15, column=0, columnspan=4, padx=5, pady=5)

# 添加字幕
add_subtitle_status = tk.IntVar()
add_subtitle_status.set(0)
ttk.Checkbutton(pro_frame, text='添加字幕', variable=add_subtitle_status).grid(row=16, column=1, columnspan=1, padx=5, pady=5)
add_subtitle_path = tk.StringVar()
add_subtitle_path.set("请选择字幕位置，也可在框中键入")
ttk.Label(pro_frame, text="字幕文件位置").grid(row=16, column=2, padx=5)
ttk.Entry(pro_frame, width=45, textvariable=add_subtitle_path).grid(row=16, column=3, columnspan=4, padx=5)
ttk.Button(pro_frame, text="选择", command=Selectsubtitle).grid(row=16, column=7, padx=5)

# HDR转SDR
hdr2sdr_status = tk.IntVar()
hdr2sdr_status.set(0)
ttk.Checkbutton(pro_frame, text='转SDR', variable=hdr2sdr_status).grid(row=17, column=1, columnspan=1, padx=5, pady=5)
hdr2sdr_path = tk.StringVar()
hdr2sdr_path.set("-pix_fmt yuv420p -vf zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv")
ttk.Label(pro_frame, text="转码参数").grid(row=17, column=2)
ttk.Entry(pro_frame, width=45, textvariable=hdr2sdr_path).grid(row=17, column=3, columnspan=4)
ttk.Label(pro_frame, text="<-小白末改").grid(row=17, column=7)


scr = scrolledtext.ScrolledText(main_window, width=80, height=4)
scr.insert("end", "可点击[命令预览]按钮，查看生成的FFmpeg命令行参数，亦可根据个人需求，在此修改参数")
scr.grid(row=18, column=0, columnspan=5, pady=5)
ttk.Button(main_window, text="一键开始", width=50, command=FinalGo).grid(row=19, column=0, padx=5, pady=5, sticky=E)
ttk.Button(main_window, text="命令预览", width=30, command=CommandPreview).grid(row=19, column=1, columnspan=3, padx=5, pady=5)
main_window.mainloop()

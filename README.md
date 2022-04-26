# Video Assistant Powerd By FFmpeg

Author  :  lijishi  
Contact :  lijishi@163.com  
Software:  Pycharm & Python 3.9.5   
License :  GNU GENERAL PUBLIC LICENSE Version 3   

## 1、软件下载 & 代码开源 

#### Github: https://github.com/GaryNotGay/VideoAssistan
#### Gitee: https://gitee.com/garynotgay/VideoAssistant
#### CDN: https://tencentcloud-bj-1252747136.cos.ap-beijing.myqcloud.com/software/VideoAssistant_V1.0.zip   

## 2、开发文档

| 功能设置 | 对应命令 | 可选项 |
| --- | --- | --- |
| 格式转换 | output.xxx | mp4/mkv/…… |
| 分辨率转换 | -s width x height  | 1920x1080/3840x2160/…… |
| 视频编码 | -vcodec xxx | h264/hevc/…… | 
| 视频码率 | -b:v xxxk | 2000k/3000k/…… |
| 音频编码 | -acodec xxx | aac/ac3/…… |
| 音频码率 | -b:a xxxk | 128k/320k/…… |
| 添加字幕 | -vf subtitle=xxx | srt/ass/…… |
| HDR2SDR | -pix_fmt yuv420p …… | 无，大神可手动调整 |

## 3、注意事项
##### 字幕格式已开启校验，目前仅支持srt/ass格式
##### 源视频格式暂未开启校验，正在调试中，后期上线
##### 选择格式转换时，需匹配相应编码格式，否则会执行失败
##### 分辨率转换功能采用硬转换方式，切记参数为宽x高，否则容易产生比例不一致的问题，后期考虑增加软转换方式
##### 视频编码可选择_nvenc的硬件编码，前提是确认设备支持，后期尝试实现软件内检测
##### 选择mp3/flac/wav等音频编码只能输出为对应的音频格式，若选择错误对应的转换格式会导致执行失败
##### HDR转SDR功能属于实验阶段，参数来自B站某篇教程，亲测可实现基本功能，小白可直接开启，大神可以依据自己需求更改参数

## 4、更新日志

### V1.0
更新日期：20220426   
更新内容：首次发布！欢迎下载使用，多提意见多交流！   

## 5、ToDoList
> 欢迎提交Issue，别忘了点个Star，亦可邮件沟通，欢迎交流   

##### 增加软件稳定性，修复软件bug，完善软件文档，优化界面UI
##### 增加多视频批量处理功能
##### 增加视频剪切/合并功能
##### 增加音视频智能识别字幕等功能（基于云平台）


## 6、已知问题
暂无

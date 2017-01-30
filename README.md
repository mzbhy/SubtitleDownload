# SubtitleDownload

利用[射手API](https://www.shooter.cn/api/subapi.php)，自动下载字幕文件。

脚本用python2.7.10编写，利用urllib和urllib2获取URLs(Uniform Resource Locators)数据，利用json解析API返回数据，利用hashlib计算文件哈希值，利用docopt提供CLI接口。

## 使用方法

1. 安装依赖项（按需）

```bash
sudo pip install docopt
```

2. 下载脚本（以Linux为例）

```bash
git clone https://github.com/lxalxy/SubtitleDownload.git
cd SubtitleDownload
```

3. 运行脚本下载字幕

```bash
python shooter_download.py D:\test.avi
```

## 参数说明

* -h,--help        显示帮助菜单
* -c                    中文字幕(默认)
* -e                   英文字幕


## Windows下添加到右键菜单

将WindowsRightClickMenu\SubtitleDownload.bat以及WindowsRightClickMenu\SubtitleDownload.reg文件中的路径修改为自己的路径，保存后双击SubtitleDownload.reg即可。

## 更新历史

### 2017.1.30

1. 修正Linux系统下字幕文件与脚本文件同目录的问题
2. Windows下快捷操作方式由“发送到”改为“鼠标右键菜单”，并修正包含特殊字符的文件名问题

## To do

1. 检测文件夹中所有视频文件并下载字幕
2. 迭代检测文件夹
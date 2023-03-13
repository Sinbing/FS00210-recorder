## 给FC00210传感器用的数据解析器

我用的FS00210传感器+usb转TTLCP2102串口模块，理论上FS00210传感器都可以用

在微博上看到大佬 [@**特浓拿铁可可**](https://weibo.com/u/5249617408) 分享的材料清单，但先用logger记录，然后人工读数据这方法用起来不够直观好用，所以自己写了个小解析器用。

## 功能

1. ### 方便的查看数据

    直接监听串口数据，解析原始数据后以十进制显示

    ![show2](https://github.com/Sinbing/FS00210-recorder/blob/main/png/Usage2.png)

    

2. ### 输出CVS数据表

    老版本使用Excel输出，但发现关闭程序时有小概率损坏文件（半天白测）

    新版本使用CVS输出数据表，关闭程序时不会损坏文件（最多丢最后一次数据）

    ![cvs1](https://github.com/Sinbing/FS00210-recorder/blob/main/png/cvs1.png)
    

## 使用方法Usage:

### 	windows：

​		windows下可以直接运行打包好的的exe程序，程序可以在releases中下载。

​		你也可以直接运行.py文件，详见**Linux章节**（就在下一行）

### 	Linux：

​		程序需要先安装Python才能运行，但既然都用Linux了我相信你肯定有（没有随便搜都能找到大把教程）。

​		然后执行此命令以安装运行程序所需的包，安装完成后即可运行。

```
# 安装程序所需运行库
pip install serial
pip install pyserial
# 运行程序
python FS00210-recorder.py
```

### 	使用程序：

​		程序打开后是一个黑色框框，但不用担心！这不会让你输入任何指令。

​		你只需输入 **0/1** 来确定你是否需要保存CVS数据表。

![Usage1](https://github.com/Sinbing/FS00210-recorder/blob/main/png/Usage1.png)

​		输入 0 - 传感器结果将直接输出在黑框框（终端）内

​		输入 1 - 传感器除了输出在终端内，还会保存一份CVS数据表。

### 注意！

​		如果你运行程序后刷屏报错 **“数据校验失败，弃用此次数据”** 请重新运行程序。程序以字节数切割传感器结果，如打开程序时传感器正在发送数据，会因为切割位置错误出现这个错误。

![Error1](https://github.com/Sinbing/FS00210-recorder/blob/main/png/error1.png)

## 常见问题Q&A

### 运行程序报错  AttributeError: module 'serial' has no attribute 'Serial'

​		这是因为 pyserial 模块没有正确安装，我自己换了一台电脑就遇到了这个问题，不知道其他人会不会碰到。我的环境是Python3.8.10 +serial==0.0.97 +pyserial==3.5，能正常运行。

​		解决方法：运行以下命令重新安装该模块

```
pip uninstall pyserial
pip install pyserial
```



### 	运行程序后没任何输出

​		把USB拔了重新插一下试试，程序也要记得关掉重新启动，亲测有效。

### 	我有多个串口设备怎么办

​		写程序时考虑到了，存在多个设备时将由用户手动输入监听的设备。你可以按下Win+X - 设备管理器 - 端口（COM和TPL）查看这个传感器是哪个端口（打开设备管理器后拔插USB，看看新增）。

### 	其他传感器可以使用吗

​		同是福申家的传感器也许可以，你需要确定他们的UART数据定义是否相同，我是根据数据位数确定这是什么数据的。碰到不兼容的传感器可能会报错或者得到错误数据。

### 	我碰到了你没说的其他问题

​		发个Issues，我看到时也许能帮你解决，我很菜，所以不能保证100%能处理（看代码就知道我多菜了）。
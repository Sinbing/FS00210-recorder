## 给传感器用的数据解析器

我用的FS00210传感器+usb转TTLCP2102串口模块，理论上FS00210传感器都可以用

在微博上看到大佬 [@**特浓拿铁可可**](https://weibo.com/u/5249617408) 分享的材料清单，但先用logger记录，然后人工读数据这方法用起来不够直观好用，所以自己写了个小解析器用。

## 功能

1. ### 方便的查看数据

    直接用程序处理数据，每秒刷新一次，以十进制打印

    ![show1](https://github.com/Sinbing/FS00210-recorder/blob/main/png/show1.png)

    

2. ### 输出Excel数据表

    可以将读取的数据以Excel输出，还能顺便画个图

    ![excel1](https://github.com/Sinbing/FS00210-recorder/blob/main/png/excel1.png)

    ![excel2](https://github.com/Sinbing/FS00210-recorder/blob/main/png/excel2.png)

## 用法

### 	windows：

​		windows下可以直接运行打包好的的exe程序，程序可以在[releases](https://github.com/Sinbing/FS00210-recorder/releases/tag/FS00210)中下载。

​		你也可以直接运行py程序，详见**Linux章节**（就在下一行）

### 	Linux：

​		程序需要先安装Python才能运行，但既然都用Linux了我相信你肯定有（没有随便搜都能找到大把教程）。

​		然后执行此命令以安装运行程序所需的包，安装完成后即可运行。

```
pip install -r requirements.txt
python FS00210-recorder.py
```

### 	使用程序：

​		程序打开后是一个黑色框框，但不用担心！这不会让你输入任何指令。

​		你只需输入 0/1 来确定你是否需要保存Excel文件。

![Usage1](https://github.com/Sinbing/FS00210-recorder/blob/main/png/Usage1.png)

​		输入 0 - 传感器结果将直接输出在黑框框（终端）内

​		输入 1 - 传感器除了输出在终端内，还会保存一份Excel文件。

## 常见问题Q&A

### 	运行程序后没任何输出

​		把USB拔了重新插一下试试，程序也要记得关掉重新启动，亲测有效。

### 	我有多个串口设备怎么办

​		写程序时考虑到了，存在多个设备时将由用户手动输入监听的设备。你可以按下Win+X - 设备管理器 - 端口（COM和TPL）查看这个传感器是哪个端口（打开设备管理器后拔插USB，看看新增）。

### 	其他传感器可以使用吗

​		同是福申家的传感器也许可以，你需要确定他们的UART数据定义是否相同，我是根据数据位数确定这是什么数据的。碰到不兼容的传感器可能会报错或者得到错误数据。

### 	我碰到了你没说的其他问题

​		发个Issues，我看到时也许能帮你解决，我很菜，所以不能保证100%能处理（看代码就知道我多菜了）。

#  导语

应学校要求，餐后要去小程序进行光盘打卡，起初想做这个脚本很久的了，但是考虑到学时问题就搁置了，直到这两天得知，可以有学时，因此，就去把这个脚本搞出来并使用了，使用方法比较简单，接下来会一一教学

# 准备工作

windows 系统 (mac 考虑到不够大众话就不弄了)、fiddler、python3.7+、电脑版微信最新版 (可以启动小程序的就行)

文末会附上所需要的文件

# 安装和配置

安装 python 教程

[![步骤1](https://image.i286.com/images/20211115/1.png)]()

务必勾选 Add Python 3.7 to PATH

不然你要自己去配置环境变量了

[![步骤2](https://image.i286.com/images/20211115/2.png)](https://image.i286.com/images/20211115/2.png)

[![步骤3](https://image.i286.com/images/20211115/3.png)](https://image.i286.com/images/20211115/3.png)

安装 requests 模块依赖

[![步骤4](https://image.i286.com/images/20211115/4.png)](https://image.i286.com/images/20211115/4.png)

在控制台输入

```
pip install requests
```

[![步骤5](https://image.i286.com/images/20211115/5.png)](https://image.i286.com/images/20211115/5.png)

安装 Fiddler

[![步骤6](https://image.i286.com/images/20211115/6.png)](https://image.i286.com/images/20211115/6.png)

[![步骤7](https://image.i286.com/images/20211115/7.png)](https://image.i286.com/images/20211115/7.png)

[![步骤8](https://image.i286.com/images/20211115/8.png)](https://image.i286.com/images/20211115/8.png)

配置 Fiddler 配置 HTTPS 证书

[![步骤9](https://image.i286.com/images/20211115/9.png)](https://image.i286.com/images/20211115/9.png)

[![步骤10](https://image.i286.com/images/20211115/10.png)](https://image.i286.com/images/20211115/10.png)

[![步骤11](https://image.i286.com/images/20211115/11.png)](https://image.i286.com/images/20211115/11.png)

[![步骤12](https://image.i286.com/images/20211115/12.png)](https://image.i286.com/images/20211115/12.png)

[![步骤13](https://image.i286.com/images/20211115/13.png)](https://image.i286.com/images/20211115/13.png)

ok 之后关闭 Fiddler 重新打开

# 开始抓取数据 获取 token

登录电脑微信，务必把电脑版微信更新到最新版

建议先在手机上打开一次光盘打卡小程序， 这样就可以在微信电脑短打开了

如果遇到打不开小程序，可以试试退出电脑微信再次登录打开

[![步骤14](https://image.i286.com/images/20211115/14.png)](https://image.i286.com/images/20211115/14.png)

打开小程序后回到 Fiddler

[![步骤15](https://image.i286.com/images/20211115/15.png)](https://image.i286.com/images/20211115/15.png)

随便选一个即可，根据图示操作

[![步骤16](https://image.i286.com/images/20211115/16.png)](https://image.i286.com/images/20211115/16.png)

务必复制好那串 32 位 token 哦

# 修改 plate.py

修改打卡脚本，右键 plate.py 按图示选择

[![步骤17](https://image.i286.com/images/20211115/17.png)](https://image.i286.com/images/20211115/17.png)

打开后拉到最低 更换 token 即可

[![步骤18](https://image.i286.com/images/20211115/18.png)](https://image.i286.com/images/20211115/18.png)

最后按 Ctrl+S 保存 或者点左上角 File->save 保存

# 验证脚本是否可用

双击我们修改好的脚本文件即可

脚本窗口最小化即可，已经设定成每两小时自动打卡一次

[![步骤19](https://image.i286.com/images/20211115/19.png)](https://image.i286.com/images/20211115/19.png)

# 功能介绍

由于时间有限，匆忙赶出来的，目前实现的功能有：

1. 打卡光盘
2. 喂食小光（可以领取能量）
3. 领取小光能量
4. 领取打卡红包

# 所需文件

1. python3.7 安装包 [点我下载](https://wwa.lanzoui.com/iY0Vdwjkbeb)
2. Fiddler [点我下载](https://wwa.lanzoui.com/isCEzwjkbob)
3. [plate.py](http://plate.py/) [点我下载](https://github.com/poboll/palte/blob/main/plate.py)
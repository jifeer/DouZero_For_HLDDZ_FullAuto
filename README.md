# DouZero_For_HLDDZ_FullAuto: 将DouZero用于欢乐斗地主自动化
* 本项目基于[DouZero](https://github.com/kwai/DouZero) 和  [DouZero_For_Happy_DouDiZhu](https://github.com/tianqiraf/DouZero_For_HappyDouDiZhu) 

* 环境配置请移步项目DouZero

* 模型默认为ADP，更换模型请修改main.py中的模型路径，如果需要加载Resnet新模型，请保证游戏路径或文件名中存在关键词 "resnet"

  ```python
  self.card_play_model_path_dict = {
      'landlord': "baselines/resnet_landlord.ckpt",
      'landlord_up': "baselines/resnet_landlord_up.ckpt",
      'landlord_down': "baselines/resnet_landlord_down.ckpt"
  }
  ```

* 

* 运行main.py即可

* 在原 [DouZero_For_Happy_DouDiZhu](https://github.com/tianqiraf/DouZero_For_HappyDouDiZhu) 的基础上加入了自动出牌，基于手牌自动叫牌，加倍，同时修改截屏方式为窗口区域截屏，游戏原窗口遮挡不影响游戏进行。

*   **请勿把游戏界面最小化，否则无法使用**

## 说明
*   欢乐斗地主使用 **窗口** 模式运行
*   **如果觉得这个项目有用，请给一个Star谢谢！**
*   **本项目仅供学习以及技术交流，请勿用于其它目的，否则后果自负。**

## 使用步骤
1. 先使用 `debug_screenshot.py`  确认自己的屏幕缩放比

2. 修改 `main.py` 中屏幕缩放比为自己屏幕的缩放比

3. 点击游戏中开始游戏后点击程序的 `自动开始`

4. 如果需要自动继续下一把，点击单局按钮，使其变为自动

## 自动叫牌/加倍原理

用DouZero自我博弈N局，对于随机到的每种手牌，随机生成若干种对手手牌，把该牌型和赢的局数扔进一个简单的全连接网络进行训练，得到手牌与胜率之间的关系，最后根据预期胜率，以一定阈值进行叫牌和加倍。

## 潜在Bug
*   有较低几率把王炸识别为不出


## 鸣谢
*   本项目基于[DouZero](https://github.com/kwai/DouZero)  [DouZero_For_Happy_DouDiZhu](https://github.com/tianqiraf/DouZero_For_HappyDouDiZhu) 

## 其他
解决速度：pip3 install xxx  -i https://pypi.tuna.tsinghua.edu.cn/simple

解决python "No module named pip"的问题
python 升级后导致不能使用原来的pip命令
windows平台
cmd中敲命令：python -m ensurepip

欢迎加入QQ群交流自动化相关：565142377  密码 douzero

## GPU 安装
### nvidia 11.8

1. cuda环境安装： https://blog.csdn.net/m0_45447650/article/details/123704930
   1. 设置path
      1. 
2. cudnn下载部署： cudnn-windows-x86_64-8.5.0.96_cuda11-archive
   pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116

## 基础环境安装
1. pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
2. python.exe -m pip install --upgrade pip
3. pip3 install douzero
4. pip3 install ujson
5. pip3 install uvicorn
6. pip3 install fastapi
7. pip3 install pyinstaller
8. 打包：pyinstaller -D -i D:\e-projects\DouZero_For_HLDDZ_FullAuto\output\favicon.ico -p D:\e-projects\DouZero_For_HLDDZ_FullAuto -n dou-zero-server  --add-data ".\baselines;.\baselines"  douFacade.py

9. python 安装console色彩包：pip3 install colorama


## 错误处理

数据量太大出现Memory Error问题，扩大虚拟内存的方法：
1、打开 控制面板；
2、找到 系统 这一项；
3、找到 高级系统设置 这一项；
4、点击 性能 模块的 设置 按钮；
5、选择 高级面板，在 虚拟内存 模块点击更改；
6、记得 不要 选中“自动管理所有驱动器的分页文件大小”，然后选择一个驱动器，也就是一个盘，选中自定义大小，手动输入初始大小和最大值，当然，最好不要太大，更改之后能在查看盘的使用情况，不要丢掉太多空间。
7、都设置好之后，记得点击 “设置”， 然后再确定，否则无效，最后 重启电脑 就可以了。

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
   1. 设置path, 执行setEnvParams.bat
2. cudnn下载部署： cudnn-windows-x86_64-8.5.0.96_cuda11-archive
   解压释放到C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8目录下

3. 
   1. pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
   2. pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116

## 基础环境安装
1. pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
2. python.exe -m pip install --upgrade pip
3. pip3 install douzero
4. pip3 install ujson
5. pip3 install uvicorn
6. pip3 install fastapi
7. pip3 install pyinstaller
8. 打包：pyinstaller -D -i D:\e-projects\DouZero_For_HLDDZ_FullAuto\output\favicon.ico -p D:\e-projects\DouZero_For_HLDDZ_FullAuto -n portal  --add-data ".\baselines;.\baselines"  portal.py
9. EXE 发布：
   1. 安装python 3.8
   2. 把业务py文件直接拷贝到打包结果目录下，即和exe同一目录
   3. 执行命令：start "模拟器-7" cmd /k portal.exe  7
10. python 安装console色彩包：pip3 install colorama


## 错误处理

数据量太大出现Memory Error问题，扩大虚拟内存的方法：
1、打开 控制面板；
2、找到 系统 这一项；
3、找到 高级系统设置 这一项；
4、点击 性能 模块的 设置 按钮；
5、选择 高级面板，在 虚拟内存 模块点击更改；
6、记得 不要 选中“自动管理所有驱动器的分页文件大小”，然后选择一个驱动器，也就是一个盘，选中自定义大小，手动输入初始大小和最大值，当然，最好不要太大，更改之后能在查看盘的使用情况，不要丢掉太多空间。
7、都设置好之后，记得点击 “设置”， 然后再确定，否则无效，最后 重启电脑 就可以了。

## 单个项目创建虚拟环境
1. 安装第三方包：virtualenv
   pip install --ignore-installed virtualenv
   1
2. 创建虚拟环境
   想要创建虚拟环境，需要先用cmd 进入指定文件夹（指定文件夹：就是你想把虚拟环境的文件放在哪里；），运行：
   virtualenv 环境名称 --python=python3.8
3. 在cmd中，进入虚拟环境文件夹 --> 进入scripts子文件夹 -->输入：activate
4. 选择解析器，新增sdkpath：D:\e-projects\XXXX项目根目录\venv\Scripts\python.exe
5. 退出虚拟环境
      在任何路径下，输入：deactivate 
6. 删除虚拟环境
      只需要把虚拟环境文件夹删除就可以了

## system path
C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Windows\System32\OpenSSH\;D:\Program Files (x86)\jdk-18.0.1.1\bin;D:\Program Files (x86)\jdk-18.0.1.1\bin;D:\Program Files (x86)\jdk-18.0.1.1\jre\bin;D:\Program Files (x86)\TDM-GCC-64\bin;C:\Program Files (x86)\Lua\5.1;C:\Program Files (x86)\Lua\5.1\clibs;C:\Program Files\Git\cmd;C:\Program Files\Microsoft SQL Server\130\Tools\Binn\;D:\Program Files\Java\bin;D:\Windows Kits\10\Windows Performance Toolkit\;D:\ProgramData\py38\Scripts\;D:\ProgramData\py38\;C:\Users\duoduo\AppData\Local\Microsoft\WindowsApps;D:\Program Files (x86)\IntelliJ IDEA Community Edition 2022.1.3\bin;;C:\Windows\SysNative;C:\Windows\SysWOW64;D:\e-projects\DouZero_For_HLDDZ_FullAuto\

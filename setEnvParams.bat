@echo off
chcp 65001
if exist "%SystemRoot%\SysWOW64" path %path%;%windir%\SysNative;%SystemRoot%\SysWOW64;%~dp0
bcdedit >nul
if '%errorlevel%' NEQ '0' (goto UACPrompt) else (goto UACAdmin)
:UACPrompt
%1 start "" mshta vbscript:createobject("shell.application").shellexecute("""%~0""","::",,"runas",1)(window.close)&exit
exit /B
:UACAdmin
cd /d "%~dp0"
echo current Path=：%CD%
echo 已获取管理员权限

:: TODO:设置MC平台环境变量
color 02
:: 解压pathon文件目录创建

::设置CUDA/path的安装路径
set CUDA_PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8
set CUDA_PATH_V11_8=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8

:: 系统级环境变量注册表项
set regpath=HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment
set cuda_bin=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\bin
set cuda_lib=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\lib
set cuda_include=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\include
set cuda_libvnnp=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.8\libvnnp
set python_script=D:\Programs\Python\Python38\Scripts
set python_home=D:\Programs\Python\Python38
:: 添加环境变量
reg add "%regpath%" /v CUDA_PATH /d "%CUDA_PATH%" /t REG_SZ /f
reg add "%regpath%" /v CUDA_PATH_V11_8 /d "%CUDA_PATH_V11_8%" /t REG_SZ /f
reg add "%regpath%" /v python_script /d "%python_script%" /t REG_SZ /f
reg add "%regpath%" /v python_home /d "%python_home%" /t REG_SZ /f

:: 追加环境变量^%systemroot^
::set PATH=
@echo %PATH%
::reg add "%regpath%" /v Path /t REG_EXPAND_SZ  /d "%PATH%" /f
::只能执行一遍，否则会出错
setx /M "Path" "%python_home%;%python_script%;%cuda_bin%;%cuda_lib%;%cuda_include%;%cuda_libvnnp%;%path%"

set ENV_PATH=%PATH%
::@echo %ENV_PATH%

::设置虚拟内存到D盘，大小为1024-1024，并且删除C盘pagefile.sys'
wmic PageFileSet create name="D:\\pagefile.sys",InitialSize="50000",MaximumSize="80000"
wmic PageFileSet where "name='C:\\pagefile.sys'" delete

cd d:
d:
mkdir d:/
start winrar x 要解压的压缩文件 [要解压的文件] 解压目录
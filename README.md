# ddns_for_dnspod.cn
DNSPOD中国站DDNS简易客户端
# 编译环境说明：

源码编译请自行准备python2.7 32位编译环境。

## 依赖包（均为32位，请勿下载64位）：
- pywin32
- py2exe
- pyqt（源码中已含安装包，路径/uilistpod/PyQt4-4.10.3-gpl-Py2.7-Qt4.8.5-x32.exe）
其它理论上python应该自带，如果没有，请自行pip下。

# 文件说明：
-  pylistpod.py  　命令行版获取指定token下的域ID以及记录ID，仅供测试用
-  pypod.py       命令行版DDNS手动提交客户端，仅供测试用（可能有BUG）
-  pypod_service.py     windows服务的源代码
-  release_2_service.cmd      用于发布整个工程的批处理
-  runme2installservice.cmd   用于手动安装并启动服务的批处理，需要系统管理员权限
-  runme2stop.cmd             用于手动停止并删除服务的批处理，需要系统管理员权限
-  setup.py                   已废弃。用于将pypod.py发布为exe，由于已封装了服务版，需要的童鞋可以自行发布。
-  setup_pylistpod.py         命令行版获取指定token下的域ID以及记录ID的发布配置文件，用于py2exe发布为exe
-  setup_service.py           windows服务的发布配置文件，用于py2exe发布为exe
-  setup_uilistpod.py         GUI界面的发布配置文件，用于py2exe发布为exe
-  site.ini                   记录设定的记录的DDNS历史外网IP，请勿删除，建议不要自行修改。
-  uilistpod.py               GUI界面主体（主体功能均通过它实现）
-  uilistpod_core.py          GUI界面的处理函数（主体的所有按钮功能均通过它实现）
-  user.tpl.ini               服务启动的依赖文件。用户配置文件模板，可根据需要自行编辑。请勿修改里面各个域名称，否则会导致服务异常。该文件编辑完成后，请将其更名为user.ini。
-  uilistpod
      -  Core.py              界面核心代码，基本不用动啥。定义界面的各种行为以及界面内容初始化。
      -  PyQt4-4.10.3-gpl-Py2.7-Qt4.8.5-x32.exe      
      -  ui2py.cmd            将ui转换为py
      -  uilistpod.py         界面布局代码，不用修改，通过UI生成
      -  uilistpod.ui         界面布局的qt源码，请使用pyqt自带工具进行修改（有童鞋愿意直接改源代码也行啦……）
      -  __init__.py          保持默认



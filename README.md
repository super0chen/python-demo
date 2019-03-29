# 1、本项目要可以实现的功能：
> - A、那种在后台默默运行的定时器（比较适合数据采集）
> - B、搭建restful接口的web服务器（spring boot）
> - C、项目基于python 模块 flask 搭建 （有兴趣可以看看Django的使用）

# 2、app.common包下面有一些公共类
> -  BaseDao.py ：对DBUtils.PersistentDB 包进行了二次封装，简化了操作mysql的步骤，使用例子参照test_mysql_001.py
> -  logger.py：日志打印，类似于java 的logback
> -  RedisDao.py: 操作redis的类

# 3、requestsA.py：列出了发送http请求的常用使用方式（类似于java里的OKHttpUtils）

# 4、restful：目录提供了对外暴露的接口
 > - A、启动项目，访问接口：localhost:8000/test/t

# 5、cron：目录下提供了定时器相关的使用方法，于spring boot的 @Scheduled(cron = "0 */10 * * * ? ") 功能一模一样
> - A、@Scheduled注解的实现方式，参照app.cron.__init__.py类

# 6、微信机器人：app.wx.wx_test.py 简单的列出了python怎样去发送微信消息

# 7、settings: 目录提供了全局配置，如果数据库用户秘密。。。

# 8、.env：文件是控制项目的环境（本地：dev  测试：test  正式：product）
> - A、修改.env文件内容：在jenkins发布时，使用命令sed -i 's/ENVSTATUS=dev/ENVSTATUS=${CENV}/g' .env 去修改

# 9、Pipfile：是基于pipen创建的，是项目相关的一些第三方依赖，类似于nodejs里的包

# 10、Pipfile.lock：是根据Pipfile生成的sha256码（该文件不需要提交到git上）

# 11、项目运行 (在项目根目录执行下面命令)
> - A、创建虚拟环境：pipenv --python 3.6
> - B、下载依赖包：pipenv install
> - C、启动项目
        1）IDEA里
            右键 run.py 运行 （可以debug运行）

        2）命令行运行
            nohup pipenv run python manager.py server >> ../run.log &

# 12、pipenv使用
```
注意：下面所有的pipenv操作都是在当前虚拟环境下执行的

A、pipenv升级
python -m pip  install --upgrade pip
python -m pip uninstall pip
pipenv version 2018.7.1 支持完美的pip版本是pip 18.0
解决办法：
A、单个项目解决：pipenv run pip install pip==18.0
B、全局解决：python3 -m pip install pip==10.0.1 或 python -m pip install pip==10.0.1 （该方法不行）

B、linux源码安装python3.6，用于pipenv使用3.6创建虚拟环境
yum install -y gcc gcc-c++ zlib zlib-devel
tar -zvx -f Python-3.6.1.tgz
cd Python-3.6.1
./configure --prefix=/usr/local/python3
make && make install
cd /usr/local/python3/bin
./python3.6 -m pip  install --upgrade pip
cd /usr/local/bin
ln -s /usr/local/python3/bin/python3 python3

然后就可以使用pipenv --python 3.6安装3.6的虚拟环境了

1、常用（pip install pipenv：安装pipenv）
A、pipenv install：将当前目录转换为虚拟环境
B、pipenv install -r path/to/requirements.txt：导入指定目录下的requirements.txt文件
      pipenv install -r requirements.txt
C、pipenv install requests --dev： 安装requests模块到dev环境
D、pipenv shell： 激活并进入当前项目的虚拟环境（项目根路径下有.env文件，会自动加载环境变量，pipenv run也是）===该命令只在linux下生效
      exit：退出环境

2、打包
A、pipenv lock -r：反向生成requirements.txt文件
B、pipenv lock -r -d：生成dev-packages的requirements.txt文件
C、pipenv install requests==2.13.0：安装指定版本的依赖模块
D、pipenv install -e . ：安装本地py模块到虚拟环境(setup.py)
      pipenv install xxx.whl
E、说明：修改成阿里云镜像源依然在项目发布的时pipenv install操作缓慢，可以按照下面操作执行
pipenv install --skip-lock：跳过lock操作
pipenv install requests --skip-lock: 跳过lock操作，在安装requests模块时
pipenv lock：统一执行lock操作

3、更新或删除
A、pipenv update：更新所有的依赖（有时会因为网络原因失败，多执行几次即可）
      pipenv update requests：只更新requests依赖
B、pipenv --rm： 删除虚拟环境
C、pipenv uninstall --all： 删除所有的安装包
pipenv uninstall requests: 删除指定依赖

4、不常用
pipenv --envs： 输出当前的环境变量
pipenv --rm:  删除虚拟环境
pipenv --where： 获取项目路径
pipenv --venv： 获取虚拟文件路径
pipenv --py：获取python解释器的路径
pipenv lock --pre：创建一个预发版本的锁文件(lockfile)
pipenv graph：图形显示包依赖关系
pipenv check：检查当前安装的依赖是否有漏洞
pipenv --python 3.6：创建一个新项目使用python3.6（linux下会用到，因为linux下默认安装的python2.7）
pipenv open requests：用编辑器打开requests模块（包括[packages]和[dev-packages]）

5、创建2.7的虚拟环境（安装python2.7）
 pipenv --python E:\Python27\python.exe


6、web框架
pipenv install flask
pipenv install flask flask-wtf
pipenv install flask_script flask_bootstrap  flask_session


7、关于虚拟环境的部署
A、说明：虚拟环境下面有Pipfile、Pipfile.lock这两个文件，在代码提交时，只需要提交Pipfile文件，
         然后再服务器上打包，运行时执行pipenv install会自动将Pipfile中依赖的包安装到虚拟环境

B、默认Pipfile文件
[[source]]
#url = "https://pypi.org/simple"  #默认镜像源，国内不翻墙可能无法安装镜像
url = "https://mirrors.aliyun.com/pypi/simple #阿里云镜像源
verify_ssl = true
name = "pypi"

[packages]

[dev-packages]

[requires]
python_version = "3.6"

C、pipenv install安装模块说明
pipenv install：根据Pipfile配置将所有Pipfile中[packages]的模块安装的服务器，在项目创建和发布时会用到
pipenv install requests：安装requests模块到Pipfile的[packages]下
pipenv install --dev：一键安装开发依赖，根据Pipfile的[packages]
pipenv install requests --dev：安装requests模块到Pipfile的[dev-packages]下

D、自定义虚拟环境文件路径
1）默认路径
windows：C:\Users\Administrator\.virtualenvs\
linux：~/.local/share/virtualenvs/
2）修改环境变量到当前项目运行路径根目录
windows设置环境变量:
PIPENV_VENV_IN_PROJECT：project/.venv
linux设置环境变量()：
vi  ~/.bash_profile
export PIPENV_VENV_IN_PROJECT=1

下面操作跳过========可以不看
mkdir  /path/to/
git clone https://github.com/RobertDeRose/virtualenv-autodetect.git
source /path/to/virtualenv-autodetect.sh

3）修改idea python虚拟环境路径:
venv-*;venv*;
build;*.classpath;*.hprof;*.idea;*.iml;*.project;*.pyc;*.pyo;*.rbc;*.releaseBackup;*.settings;*.yarb;*~;.DS_Store;.git;.hg;.svn;CVS;__pycache__;_svn;node_modules;pid;release.properties;vssver.scc;vssver2.scc;*$py.class;*.hprof;*.pyc;*.pyo;*.rbc;*.yarb;*~;.DS_Store;.git;.hg;.svn;CVS;__pycache__;_svn;vssver.scc;vssver2.scc;

在项目根路径下面新建文件.gitignore，添加内容.venv

8、Pipfile文件扩展
[[source]]
url = "https://mirrors.aliyun.com/pypi/simple"
verify_ssl = true
name = "pypi"

[[source]]
url = "http://pypi.home.kennethreitz.org/simple"
verify_ssl = false
name = "home"

[dev-packages]

[packages]
requests = {version="*", index="home"}  #requests 使用 http://pypi.home.kennethreitz.org/simple的源
maya = {version="*", index="pypi"} #maya 使用aliyun源
records = "*"

9、linux命令行虚拟环境运行python脚本
alias prp="pipenv run python"
pipenv run python my_project.py #使用虚拟环境运行my_project.py文件
或
prp my_project.py

10、linux下pipenv自动补全设置（由于 pipenv 的命令行程序是基于 Click 库，因此自带了 Bash 补全功能）
vi  ~/.bash_profile
eval "$(_FOO_BAR_COMPLETE=source foo-bar)"

11、.env环境变量文件说明
A、位置：项目根路径
B、pipenv shell可以加载环境变量，但只在linux上生效，windows无效
C、pipenv run python xxx.py 该命令windows和linux上都可以加载.env文件
D、读取环境变量
import os
env_dist = os.environ
env_dist.get("FOO")
# 遍历环境变量
# for k, v in env_dist.items():
#     print("%s=%s" % (k, v))

12、idea 安装2018.2(该版本目前是一个不稳定的版本，可能在使用中会有部分问题)
idea 2018.2下载地址：https://download-cf.jetbrains.com/python/pycharm-professional-182.3569.5.exe
jetbrains-toolbox下载地址：https://download-cf.jetbrains.com/toolbox/jetbrains-toolbox-1.9.3935.exe
jetbrains-toolbox介绍：（每当idea有更新时，该工具会自动下载补丁文件，不需要我们手动下载）
chrome插件地址：https://chrome.google.com/webstore/detail/jetbrains-toolbox/offnedcbhjldheanlbojaefbfbllddna
firefox插件地址：https://addons.mozilla.org/en-US/firefox/addon/jetbrains-toolbox/

13、常用包
pipenv install flask flask-wtf --skip-lock
pipenv install attr --skip-lock
pipenv install arrow --skip-lock
pipenv install DBUtils --skip-lock
pipenv install redis --skip-lock
pipenv install logbook --skip-lock
pipenv install gevent --skip-lock

pipenv install grequests --skip-lock
pipenv install requests --skip-lock
pipenv install requests_html  --skip-lock

pipenv install pytesser3 --skip-lock
pipenv install Pillow --skip-lock #PIL依赖在Pillow模块里

pipenv install progressbar --skip-lock
pipenv install urllib3 --skip-lock
pipenv install MyQR --skip-lock

pipenv install qqbot --skip-lock
pipenv install qrcode --skip-lock
pipenv install wxpy --skip-lock


14、windows 安装Scrapy
安装教程：https://www.cnblogs.com/liuliliuli2017/p/6746440.html
使用教程：https://scrapy-chs.readthedocs.io/zh_CN/latest/intro/tutorial.html


https://www.linuxidc.com/Linux/2017-03/141419.htm

15、常见错误：
A、错误1：pkg_resources.DistributionNotFound: The 'cffi>=1.11.5; sys_platform == "win32" and platform_python_implementation == "CPython"'...
      解决办法：
pip install --upgrade setuptools
pipenv install cffi

```

# 13、pipenv包大全
```
python库大全：https://github.com/jobbole/awesome-python-cn.git
伯乐在线：http://www.jobbole.com/

关键词：
0：attrs：getter setter方法：http://developer.51cto.com/art/201612/525507.htm#_motw_
1、pipenv: 替代pip来管理依赖：
官方文档：https://github.com/pypa/pipenv
第三方文档：https://crazygit.wiseturtles.com/2018/01/08/pipenv-tour/
2、爬取网络站点的库（requests）（requests_html 是基于现有的框架 pyquery、requests、lxml 等库进行了二次封装，更加方便开发者调用）
3、使用 HTTP 的库（requests【同步】、grequests【异步，基于gevent】）
4、并发和并行（gevent：一个基于协程的 Python 网络库）
5、日志库：logbook
6、redis模块：redis、hiredis，需要redis这两个模块都要安装，文档地址：https://github.com/andymccurdy/redis-py
7、gevent:基于协程的并发库：https://blog.csdn.net/freeking101/article/details/53097420
      requests使用：https://blog.csdn.net/qq_41144008/article/details/78808588
8、cProfile：打印方法各个地方的执行时间，方法效率检查：https://yq.aliyun.com/articles/96808/
9、HyperLPRLite:车牌号识别：https://github.com/zeusees/HyperLPR
10、wxpy、wechat_sender：微信机器人库：http://wxpy.readthedocs.io/zh/latest/messages.html
11、qqbot、pillow 、wcwidth ：qq机器人库:  https://github.com/pandolia/qqbot
12、python定时器实现方式：https://lz5z.com/Python定时任务的实现方式/
13、pyinstaller打包：pyinstaller xxx.py
14、progressbar一个进度条库：
15、Arrow时间处理库：
16、telnetlib校验IP代理是否可用：
17、ujson比json快N倍


=============具体使用===================
1：attrs：getter setter方法：http://developer.51cto.com/art/201612/525507.htm#_motw_
import attr
from attr.validators import instance_of
@attr.s
class User(object):
    x = attr.ib()
    y = attr.ib()
    z = attr.ib()
    f1 = attr.ib(default=attr.Factory(list), validator=instance_of(list))
    f = attr.ib(default=42, validator=instance_of(int))
    z1 = attr.ib(default=0.1, validator=instance_of(float))
print(User(1, 2, 3) == User(1, 2, 3))
print(User(1, 2, 3) == User(1, 3, 2))
print(User(3, 2, 3) == User(1, 2, 3))
print(attr.asdict(User(1, 2, 3, [1, 2])))
print(User(1, 2, 3, [1, 2]).f1)

2、Arrow时间处理库：
t = arrow.now() # Arrow ——>2018-07-01T11:32:45.135800+08:00
arrow.now().timestamp #int ——> 1530416098
arrow.now().format() #str ——> 2018-07-01 11:36:19+08:00
arrow.now().format('YYYY-MM-DD HH:mm:ss') #str ——> 2018-07-01 11:37:49
arrow.now().format('YYYY-MM-DD HH:mm:ss:SS') #str ——> 2018-07-01 11:37:49:32
arrow.get("2018-07-01 11:39:47", "YYYY-MM-DD HH:mm") # Arrow ——>2018-07-01T11:39:00+00:00

# get方法有问题，转换timestamp为具体时间时，相差8小时，底层用的是Arrow.utcfromtimestamp方法转换的
arrow.get(arrow.now().timestamp)  # Arrow ——>2018-07-01T04:38:52+00:00  import arrow
Arrow.fromtimestamp(arrow.now().timestamp)  # Arrow ——>2018-07-01T12:38:52+08:00  from arrow import Arrow

# 记住字符串转时间对象，一定设置时区（tzinfo='Asia/Shanghai'）
t1 = arrow.get("2019-03-25 17:22:47", format_str, tzinfo='Asia/Shanghai')
t1.timestamp  # 这样输出的秒数才是正确的，否则比北京时间多8小时


3、telnetlib校验IP代理是否可用：
import telnetlib
start = arrow.now().timestamp
try:
    telnetlib.Telnet('223.145.229.22', port='6666', timeout=1) #超时时间1s
    print('success')
except:
    print('connect failed')

end = arrow.now().timestamp - start
print('耗时：%d' % end)

4、progressbar一个进度条库：
from progressbar import ProgressBar
import time
pbar = ProgressBar(maxval=10)
for i in range(1, 11):
    pbar.update(i)
    time.sleep(1)
pbar.finish()
# 60% |########################################################

网络
Scapy, Scapy3k: 发送，嗅探，分析和伪造网络数据包。可用作交互式包处理程序或单独作为一个库。
pypcap, Pcapy, pylibpcap: 几个不同 libpcap 捆绑的python库
libdnet: 低级网络路由，包括端口查看和以太网帧的转发
dpkt: 快速，轻量数据包创建和分析，面向基本的 TCP/IP 协议
Impacket: 伪造和解码网络数据包，支持高级协议如 NMB 和 SMB
pynids: libnids 封装提供网络嗅探，IP 包碎片重组，TCP 流重组和端口扫描侦查
Dirtbags py-pcap: 无需 libpcap 库支持读取 pcap 文件
flowgrep: 通过正则表达式查找数据包中的 Payloads
Knock Subdomain Scan: 通过字典枚举目标子域名
SubBrute: 快速的子域名枚举工具
Mallory: 可扩展的 TCP/UDP 中间人代理工具，可以实时修改非标准协议
Pytbull: 灵活的 IDS/IPS 测试框架（附带超过300个测试样例）
调试和逆向工程
Paimei: 逆向工程框架，包含 PyDBG, PIDA,pGRAPH
Immunity Debugger: 脚本 GUI 和命令行调试器
mona.py: Immunity Debugger 中的扩展，用于代替 pvefindaddr
IDAPython: IDA pro 中的插件，集成 Python 编程语言，允许脚本在 IDA Pro 中执行
PyEMU: 全脚本实现的英特尔32位仿真器，用于恶意软件分析
pefile: 读取并处理 PE 文件
pydasm: Python 封装的 libdasm
PyDbgEng: Python 封装的微软 Windows 调试引擎
uhooker: 截获 DLL 或内存中任意地址可执行文件的 API 调用
diStorm: AMD64 下的反汇编库
python-ptrace: Python 写的使用 ptrace 的调试器
vdb/vtrace: vtrace 是用 Python 实现的跨平台调试 API, vdb 是使用它的调试器
Androguard: 安卓应用程序的逆向分析工具
Capstone: 一个轻量级的多平台多架构支持的反汇编框架。支持包括ARM,ARM64,MIPS和x86/x64平台。
PyBFD: GNU 二进制文件描述(BFD)库的 Python 接口
Fuzzing
Sulley: 一个模糊器开发和模糊测试的框架，由多个可扩展的构件组成的
Peach Fuzzing Platform: 可扩展的模糊测试框架(v2版本 是用 Python 语言编写的)
antiparser: 模糊测试和故障注入的 API
TAOF: (The Art of Fuzzing, 模糊的艺术)包含 ProxyFuzz, 一个中间人网络模糊测试工具
untidy: 针对 XML 模糊测试工具
Powerfuzzer: 高度自动化和可完全定制的 Web 模糊测试工具
SMUDGE: 纯 Python 实现的网络协议模糊测试
Mistress: 基于预设模式，侦测实时文件格式和侦测畸形数据中的协议
Fuzzbox: 媒体多编码器的模糊测试
Forensic Fuzzing Tools: 通过生成模糊测试用的文件，文件系统和包含模糊测试文件的文件系统，来测试取证工具的鲁棒性
Windows IPC Fuzzing Tools: 使用 Windows 进程间通信机制进行模糊测试的工具
WSBang: 基于 Web 服务自动化测试 SOAP 安全性
Construct: 用于解析和构建数据格式(二进制或文本)的库
fuzzer.py(feliam): 由 Felipe Andres Manzano 编写的简单模糊测试工具
Fusil: 用于编写模糊测试程序的 Python 库
Web
Requests: 优雅，简单，人性化的 HTTP 库
HTTPie: 人性化的类似 cURL 命令行的 HTTP 客户端
ProxMon: 处理代理日志和报告发现的问题
WSMap: 寻找 Web 服务器和发现文件
Twill: 从命令行界面浏览网页。支持自动化网络测试
Ghost.py: Python 写的 WebKit Web 客户端
Windmill: Web 测试工具帮助你轻松实现自动化调试 Web 应用
FunkLoad: Web 功能和负载测试
spynner: Python 写的 Web浏览模块支持 Javascript/AJAX
python-spidermonkey: 是 Mozilla JS 引擎在 Python 上的移植，允许调用 Javascript 脚本和函数
mitmproxy: 支持 SSL 的 HTTP 代理。可以在控制台接口实时检查和编辑网络流量
pathod/pathoc: 变态的 HTTP/S 守护进程，用于测试和折磨 HTTP 客户端
取证
Volatility: 从 RAM 中提取数据
Rekall: Google 开发的内存分析框架
LibForensics: 数字取证应用程序库
TrIDLib: Python 实现的从二进制签名中识别文件类型
aft: 安卓取证工具集恶意软件分析
pyew: 命令行十六进制编辑器和反汇编工具，主要用于分析恶意软件
Exefilter: 过滤 E-mail，网页和文件中的特定文件格式。可以检测很多常见文件格式，也可以移除文档内容。
pyClamAV: 增加你 Python 软件的病毒检测能力
jsunpack-n: 通用 JavaScript 解释器，通过模仿浏览器功能来检测针对目标浏览器和浏览器插件的漏洞利用
yara-python: 对恶意软件样本进行识别和分类
phoneyc: 纯 Python 实现的蜜罐
CapTipper: 分析，研究和重放 PCAP 文件中的 HTTP 恶意流量
PDF
peepdf: Python 编写的PDF文件分析工具，可以帮助检测恶意的PDF文件
Didier Stevens’ PDF tools: 分析，识别和创建 PDF 文件(包含PDFiD，pdf-parser，make-pdf 和 mPDF)
Opaf: 开放 PDF 分析框架，可以将 PDF 转化为 XML 树从而进行分析和修改。
Origapy: Ruby 工具 Origami 的 Python 接口，用于审查 PDF 文件
pyPDF2: Python PDF 工具包包含：信息提取，拆分，合并，制作，加密和解密等等
PDFMiner: 从 PDF 文件中提取文本
python-poppler-qt4: Python 写的 Poppler PDF 库，支持 Qt4
杂项
InlineEgg: 使用 Python 编写的具有一系列小功能的工具箱
Exomind: 是一个利用社交网络进行钓鱼攻击的工具
RevHosts: 枚举指定 IP 地址包含的虚拟主句
simplejson: JSON 编码和解码器，例如使用 Google’s AJAX API
PyMangle: 命令行工具和一个创建用于渗透测试使用字典的库
Hachoir: 查看和编辑二进制流
其他有用的库和工具
IPython: 增强的交互式 Python shell
Beautiful Soup: HTML 解析器
matplotlib: 制作二维图
Mayavi: 三维科学数据的可视化与绘图
RTGraph3D: 在三维空间中创建动态图
Twisted: Python 语言编写的事件驱动的网络框架
Suds: 一个轻量级的基于SOAP的python客户端
M2Crypto: Python 语言对 OpenSSL 的封装
NetworkX: 图库(边, 节点)
Pandas: 基于 Numpy 构建的含有更高级数据结构和工具的数据分析包
pyparsing: 通用解析模块
lxml: 使用 Python 编写的库，可以迅速、灵活地处理 XML
Whoosh: 纯python实现的全文搜索组件
Pexpect: 控制和自动化程序
Sikuli: 使用 Jython 脚本自动化基于截图进行视觉搜索
PyQt 和PySide: Python 捆绑的 Qt 应用程序框架和 GUI 库
```
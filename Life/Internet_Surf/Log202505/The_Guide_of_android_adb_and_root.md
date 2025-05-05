# ADB小白入门指南以及Root入门教程

## 目录

- [前言](#前言)
- [第一部分：ADB入门](#第一部分adb入门)
  - [什么是ADB](#什么是adb)
  - [ADB的安装与配置](#adb的安装与配置)
  - [ADB常用命令](#adb常用命令)
  - [ADB使用实例](#adb使用实例)
- [第二部分：Root硬核折腾指南-3种提取原版boot镜像的技巧](#Root硬核折腾指南-3种提取原版boot镜像的技巧)
  - [引言](#引言)
  - [方法](#方法)
    - [深刷提取法](#深刷提取法)
    - [GSI提取法](#GSI提取法)
    - [侧载提取法](#侧载提取法)
- [注意事项与风险提示](#注意事项与风险提示)
- [参考资料](#参考资料)

## 前言

随着智能手机的普及，越来越多的用户希望能够更深入地控制自己的设备，无论是为了卸载预装软件、优化系统性能，还是为了实现更多高级功能。本教程旨在为小白用户提供一个简单易懂的指南，介绍如何使用ADB工具以及如何获取Root权限，让你的手机使用更加得心应手。

## 第一部分：ADB入门

### 什么是ADB

ADB（Android Debug Bridge，安卓调试桥）是一个versatile命令行工具，它允许用户通过电脑与安卓设备进行通信。通过ADB，用户可以在不需要Root权限的情况下，实现对手机的高级控制。

大约十年前，国内的智能手机大多是运营商定制机，预装了大量无法卸载的软件，这些软件会在后台自启动，导致手机卡顿和耗电。虽然Root是一种解决方案，但它有一定风险且不是所有品牌都支持，因此ADB成为了一个更安全的替代方案。

### ADB的安装与配置

#### 下载ADB工具包

1. 访问Google官方的Android SDK Platform Tools页面下载最新版本的ADB工具包
2. 或者使用第三方整合工具包，如本教程所在目录中的platform-tools文件夹

#### 安装步骤

1. 解压下载的工具包到一个方便访问的位置
2. 将ADB工具所在目录添加到系统环境变量（可选，但推荐）
   - 右键「此电脑」→「属性」→「高级系统设置」→「环境变量」
   - 在「系统变量」中找到「Path」→「编辑」→「新建」
   - 添加ADB工具所在的完整路径，如`F:\Software\SystemManager\Tools\AboutAndroid\platform-tools`
   - 点击「确定」保存设置

#### 在手机上启用USB调试

1. 进入手机「设置」→「关于手机」
2. 连续点击「版本号」7次，启用开发者选项
3. 返回设置，进入新出现的「开发者选项」
4. 开启「USB调试」选项
5. 将手机通过USB连接到电脑
6. 在手机上允许USB调试授权

#### 验证ADB连接

打开命令提示符（CMD）或PowerShell，输入以下命令：

```bash
adb devices
```

如果显示设备序列号，则表示连接成功。

### ADB常用命令

#### 基础命令

```bash
# 查看已连接的设备
adb devices

# 重启ADB服务
adb kill-server
adb start-server

# 重启手机
adb reboot

# 进入手机shell
adb shell

# 安装应用
adb install path/to/app.apk

# 卸载应用
adb uninstall package.name
```

#### 文件传输命令

```bash
# 从电脑复制文件到手机
adb push local_file /sdcard/remote_path

# 从手机复制文件到电脑
adb pull /sdcard/remote_file local_path
```

#### 应用管理命令

```bash
# 列出所有已安装的应用包名
adb shell pm list packages

# 列出系统应用包名
adb shell pm list packages -s

# 列出第三方应用包名
adb shell pm list packages -3

# 禁用应用（不需要Root）
adb shell pm disable-user --user 0 package.name

# 启用应用
adb shell pm enable package.name
```

#### 无线ADB连接

```bash
# 确保手机和电脑在同一WiFi网络下，先用USB连接
adb tcpip 5555

# 断开USB，使用无线连接（替换IP为手机的实际IP地址）
adb connect 192.168.x.x:5555

# 断开无线连接
adb disconnect 192.168.x.x:5555
```

### ADB使用实例

#### 卸载或禁用预装应用

1. 查找要卸载的应用包名

   ```bash
   adb shell pm list packages | findstr keyword
   ```

2. 禁用应用（无需Root权限）

   ```bash
   adb shell pm disable-user --user 0 com.example.bloatware
   ```

3. 卸载系统应用（需要Root权限）

   ```bash
   adb shell
   su
   pm uninstall --user 0 com.example.bloatware
   ```

#### 修改系统设置

```bash
# 修改动画速度（加快系统动画）
adb shell settings put global animator_duration_scale 0.5
adb shell settings put global transition_animation_scale 0.5
adb shell settings put global window_animation_scale 0.5

# 完全关闭动画
adb shell settings put global animator_duration_scale 0
adb shell settings put global transition_animation_scale 0
adb shell settings put global window_animation_scale 0
```

#### 截图和录屏

```bash
# 截图并保存到电脑
adb shell screencap /sdcard/screenshot.png
adb pull /sdcard/screenshot.png .

# 录制屏幕（按Ctrl+C停止）
adb shell screenrecord /sdcard/video.mp4
adb pull /sdcard/video.mp4 .
```

## Root硬核折腾指南-[3种提取原版boot镜像的技巧](https://www.bilibili.com/video/BV1m6421c7sb/)

### 〇、引言

目前安卓手机获取root的3种方案

1. magisk（原理：对boot镜像中的ramdisk进行修补）
   目前最主流ROOT管理工具操作简单，支持挂载各种模块来修改系统文件最大的缺陷是运行在用户空间(userspace)，容易被软件检测到

2. KernelSu（内核空间root，理论上是可以下载通用镜像直接刷入，但部分厂商可能对系统底层进行了修改，不一定支持通用镜像。官方的回复是：最好是通过原版boot手动修补一次后再刷入）
   运行在内核空间（kernelspace）相比Magisk拥有更好的隐蔽性与更高权限但目前对模块支持不如Magisk全面，虽然提供了通用内核，但部分机型仍需手动修补boot
3. Apatch（内容空间root，在保留了KernelSu内核root优点的同时，减少了手动修补的难度，但依然需要boot镜像）
   目前最新一种ROOT方案，运行在内核空间。相比KernelSU，APatch修补boot过程更容易可像Magisk一样导入boot.img后自动修补

以上3种方案，几乎都是需要先拿到boot镜像（理论上）



> 引出问题：[!CAUTION]
>
> 从哪里找boot镜像？

对于xiaomi、oneplus等较为方便，市面上有许多刷机包，但是对于奇奇怪怪的设备，就很找到原版镜像。

从而有了一条新的路：

> 最终路径
>
> 从手机原本的系统中提取boot

---

==新的难题==

手机在开机状态下，提取boot镜像需要root权限

```shell
android:/ $ dd if=/dev/block/mmcblk0p8 of=/sdcard/boot.img 
dd:/dev/block/mmcb1k0p8: Permission denied
1|android:/$
```

此篇文章，将介绍3种提供原版boot镜像的技巧。

### 一、方法

#### 1.1 深刷提取法

难度：★☆☆☆☆ 	有手就行，但比较看脸

**名词解释（简要版）**

深刷：手机在深度刷机模式下，可根据分区表来提取分区的方法适用于联发科，高通平台的老设备。对于联发科，建议使用[MTK client刷机工具](https://github.com/bkerler/mtkclient/)[^1] ；而高通的机型，建议使用[Qualcomm Premium Tool(QPT)](https://cloud.189.cn/web/share?code=BRzUvajquyUr%EF%BC%88%E8%AE%BF%E9%97%AE%E7%A0%81%EF%BC%9Aucs0%EF%BC%89)。

[^1 ]: [GUIDE] [MTK] How to use MTKClient and set it up! https://xdaforums.com/t/guide-mtk-how-to-use-mtkclient-and-set-it-up.4509245/

因此该方案更适用于使用联发科与高通主流soc的老设备。而一些冷门或新款soc可能没有内置的分区表，需自行搜索。

步骤：

*联发科和高通的方式不同。*

##### 【联发科】

①正确安装驱动，打开MTK Client；
②将手机关机，关机状态下按住`音量+/音量-`，再插上数据线连接电脑（连接过程不松手）
③连接成功后，MTK Client会自动读取手机信息，并跳转界面
④在`Read Partition`(读取分区)选项卡中，可以提取我们需要的分区（选中需要提取的分区*(例如boot)*，然后点击下方的`Read Partition`按钮即可，会弹出自定义保存路径`Select output Directory`）

###### ☛ 实战案例–联发科深刷提取

[联发科深刷提取法：我给山寨机刷了系统，超低配置居然如此流畅！](https://www.bilibili.com/video/BV1J94y1J736/) 

##### 【高通】

①进入深度刷机模式（即9008模式），有一些技巧
PlanA: 通过adb命令在开机状态下进入 。尝试命令`adb reboot edl`如果没有效果，那么*大概率*需要找主板的触点进行短接；或者通过刷机线（*淘宝店铺搜索*）进入9008模式。
PlanB: 通过短接主板触点进入。
PlanC: 通过9008工程线内部短接进入。
②进入后，Qualcomm Premium Tool(QPT)会根据soc的型号自动匹配分区表，
③点击想要提取的分区*(例如boot)*，再选择`backup`(备份)，然后点击`Do job`，就可以导出。

###### ☛ 实战案例–高通深刷

[高通深刷提取法：仅售32元的儿童手机不能上网？没关系，我会出手！](https://www.bilibili.com/video/BV19p4y1N7H8/) 



##### 【小结】

电脑安装对应驱动  →  手机进入深度刷机模式  →  打开并连接到深度刷机工具  →  选择分区并导出。





#### 1.2 GSI提取法

难度：★★★☆☆ 	大多机型适用，有一定难度

**名词解释**：Generic System Images（GSI 通用系统镜像）

类似不同品牌和形态的x86电脑都能刷同一个Windows镜像。而GSI则表示安卓平台的通用镜像。这种镜像，不分设备、不分品牌，只要手机支持相关的标准都可以刷，而这个标准叫做“Project Treble”，简称PT。
（*通用系统镜像属于第三方系统，刷之前必须先解锁引导加载器*）

适用于支持`Project Treble`的设备（一般为设备出厂搭载了安卓9系统以上），通过刷入GSI获取命令行下的Root权限来提取分区。

*所谓命令行下的root，它只适用于命令行，并不能给其他APP授权。多见于userdebug版本系统（一般标注在设备信息的版本号中，带有userdebug关键词），用于调试设备。*

```shell
D:\1Flash>adb shell
android:/ $ su
:/data/data #
```



==如何判断自己设备是否支持Project Treble？==

答：可以先在手机上安装`Treble Check`软件来检查。[Link1](https://github.com/kevintresuelo/treble) [Link2](https://apkpure.com/treble-check/com.kevintresuelo.treble) [Link3](https://treble-check-treble-compatibility-checking-app.en.softonic.com/android) [Link4](https://f-droid.org/en/packages/tk.hack5.treblecheck/)

- [x] 对于支持Project Treble的设备，还存在两种情况：
  - [ ] 是否支持`**无缝系统更新 AB System Update**`

<u>支持无缝更新的设备可在开机状态下更新系统，更新后只要重启手机即可切到新系统。也可防止升级失败导致变砖。</u>

比如，以前传统的Aonly分区类型，是不支持`AB System Update`的。它在刷了GSI后会把System分区覆盖掉，从而丢失原版系统。

而从Android 10 开始，大多设备都支持AB分区；Android 12 还推出了VAB分区，解决了AB分区占用双倍空间的问题。

对于采用了`VAB分区`的设备（√`Project Treble`      √`AB System Update`）就满足了方法三（侧载提取法）。



> 【理论补充点：SAR，全称 System as root】
>
> 只要我们的设备支持SAR √（具体通过`Treble Check`软件查看即可），即使不支持AB分区，也需要下载带有AB格式的GSI刷机包



##### 步骤详解

###### Step01：获取命令行Root权限

①我们下载好GSI刷机包后，将其解压；
②手机重启到Bootloader；
③再使用`fastboot flash system `命令可以将GSI刷入system分区

```shell
D:\1Flash>fastboot flash system C:\Users\Name\Desktop\s32um\partition\1ineage-17.1-20210808-UN0FFICIAL-treble_arm_avS.img
Sending sparse'system'1/10 (131068KB) Writing	OKAY [	4.275s]
Writing 'system'		OKAY [	11.375s]
Sending sparse'system'2/10 (131068KB) Writing	OKAY [	4.143s]
Writing 'system'		OKAY [	10.787s]
…
…
Finished. Total time: 148.624s
```

④刷入完成后，通过命令`fastboot erase userdata`格式化data

```shell
D:\1Flash>fastboot erase userdata
```

⑤不出意外，便可进入 GSI （即，手机会重启进入设备）。然后我们打开设备的 USB 调试，在电脑上通过 adb 进入命令行。调用`su`若出现`#`即表示拥有命令行Root权限

```shell
D:\1Flash>adb shell
android:/ $ su 
:/data/data \#
```

###### Step02：提取分区→ 修补分区 → 刷入分区

①提取分区–找到路径

分区的类型与设备的闪存类型有关：

【eMMC闪存】

```shell
# 先进入shell，然后使用su
D:\1Flash>adb shell 
android:/ \$ su
# 使用 find /dev/block/platform/ -name 'by-name' -type d 找到路径
:/data/data \# find /dev/block/platform/ -name 'by-name' -type d
/dev/block/platform/mtk-msdc.0/11120000.msdc0/by-name

# 再通过cd导航至该路径
:/data/data \# cd /dev/block/platform/mtk-msdc.0/11120000.msdc0/by-name: :/dev/block/platform/mtk-msdc.0/11120000.msdc0/by-name \# 


# 再 通过`ls -l boot`命令，找boot的实际路径
# 注意：若手机支持无缝更新，需要提取boot_a与boot_b，而不是boot
:/dev/block/platform/mtk-msdc.0/11120000.msdc0/by-name \# ls -l boot
1rwxrwxrwx 1 root root 20 2024-03-11 21:37 boot -> /dev/block/mmcblk0p8
# 对于 【eMMC闪存】的机型，boot分区的名称通常以mmcblk开头
:/dev/block/platform/mtk-msdc.0/11120000.msdc0/by-name \#

```



【UFS闪存】

分区通常在`/dev/block/by-name/`路径下

```shell
D:\1Flash>adb shell
g2070nmt_t9921:/ \$ su
g2070nmt_t9921:/ \# cd /dev/block/by-name/ g2070nmt_t9921:/dev/block/by-name 

# 再 通过`ls -l boot`命令，找boot的实际路径
# 注意：若手机支持无缝更新，需要提取boot_a与boot_b，而不是boot
g2070nmt_t9921:/dev/block/by-name \# ls -l boot_a
lrwxrwxrwx 1 root root 16 2024-03-11 19:10 boot_a -> /dev/block/sdc29
# 对于 【UFS闪存】的机型，boot分区的名称通常以sd开头
g2070nmt_t9921:/dev/block/by-name \#
```



②提取分区，`dd`命令提取分区

`dd`命令格式：

dd if=分区实际位置 of=我们要保存的位置
	if(inputfile，输入文件）	of(outputfile，输出文件)

```shell
#【eMMC闪存】
:/dev/block/platform/mtk-msdc.0/11120000.msdc0/by-name \# ls -l boot
1rwxrwxrwx 1 root root 20 2024-03-11 21:37 boot -> /dev/block/mmcblk0p8
:/dev/block/platform/mtk-msdc.0/11120000.msdc0/by-name \# dd if=/dev/block/mmcblk0p8 of=/sdcard/boot.img


# 【UFS闪存】
g2070nmt_t9921:/dev/block/by-name \# ls -l boot_a
lrwxrwxrwx 1 root root 16 2024-03-11 19:10 boot_a -> /dev/block/sdc29
g2070nmt_t9921:/dev/block/by-name \# dd if=/dev/block/sdc29 of=/sdcard/boot_a.img
$ boot_b.img 提取同理 $
```



> 若手机是Aonly分区类型（不支持无缝更新）	
> 提取boot.img
>
> 
>
> 若手机是AB或VAB分区类型（支持无缝更新）
> 提取boot_a.img与boot_b.img
>
> 
>
> 若手机是AB或VAB分区类型（支持无缝更新，且出厂版本为Android13或以上，并且希望通过magisk来管理权限)
> 提取init_boot_a.img与init_boot_b.img



③修补分区（以magisk为例）
采用magisk进行修补的话，修补完成后，文件会自动保存至/Download路径下

④刷入分区
PlanA：fastboot模式-将修补后的镜像传到电脑，手机重启到bootloader后刷入

```cmd
# 对于Aonly分区机型，可使用
D:\1Flash>adb reboot bootloader
D:\1Flash>fastboot flash boot C:VUsers\Namez\Desktop\partition\magisk_patched-26400_8RQbE.img
target reported max download size of 134217728 bytes 
Sending boot' (16384 KB)..
OKAY [ 0.529s] Writing 'boot OKAY [ 1.333s]
Finished. Total time: 1.881s D: \1Flash>
D:\1Flash>

#对于AB分区机型，可使用
fastboot flash boot_a <修补后的boot_a.img> 
fastboot flash boot_b <修补后的boot_b.img>

# 对于AB分区，且出厂为安卓13的机型，可使用
fastboot flash init_boot_a <修补后的init_boot_a.img> 
fastboot flash init_boot_b <修补后的init_boot_b.img>

```



PlanB：命令行`dd`模式-通过dd命令将修补后的镜像刷回原始分区，无需fastboot 

```shell
android:/ \$ su
:/data/data \# dd if=/dev/block/mmcblk0p8 of=/sdcard/boot.img
32768+0 records in 
32768+0 records out
16777216 bytes (16 M) copied, 0.618426 s, 26 M/s
dd if=/sdcard/Download/magisk_patched-26400_8RQbE.img of=/dev/block/mmcblk0p8
```

dd if=修补后boot的位置 of=boot分区的实际位置
	if(inputfile，输入文件）	of(outputfile，输出文件)

简单理解，就是“从哪来，回哪去”，无论是boot，还是boot_a/boot_b，亦或是init_boot_a/init_boot_b

###### ☛ 实战案例–GSI提取法

[GSI提取法：山寨机的系统到底有多离谱？用奇特的方式挖掘真相！](https://www.bilibili.com/video/BV1ge411w7qq/)

##### GSI小结

1.安装TrebleCheck工具，判断手机是否支持PT

2.根据是否支持AB分区、是否支持SAR、处理器架构、Android版本来选择合适的GSI 

3.下载后解压，使用fastboot将GSi刷入System分区==（这一步会把手机原版的系统覆盖掉）==

4.进入GSI后打开开发者选项，获取命令行Shellroot权限

5.使用emmc闪存的手机需要先查找镜像位置，再进入。而UFS闪存的镜像位置一般固定 

6.使用ls -l命令确定boot分区实际位置

7.使用dd命令将boot分区提取到存储根目录下* 

8.使用Magisk修补boot分区

9.使用fastboot或dd命令刷写修补后的boot

10.重启手机，打开Magisk查看是否成功获取Root

*注意AB分区的手机需同时提取boot_a（b）或init_boot_a(b)*





#### 1.3 侧载提取法

难度：★★★★☆	 完美方案，不破坏原系统

通过DSU（动态系统更新)，可将GSI安装到另一个槽位。
重启系统后可进入临时的GSI，提取分区后再重启即可回到原版系统

条件：对于采用了`VAB分区`的设备（√`Project Treble`      √`AB System Update`），方可满足侧载提取法。



侧载提取法，需要安装`DSU Sideloader`工具 [Link1](https://github.com/VegaBobo/DSU-Sideloader) [Link2](https://f-droid.org/en/packages/vegabobo.dsusideloader/)

①安装至手机后，根据应用指示，放入我们下载好的GSI；
②通过一行adb命令即可开始部署（命令来自APP页面）；
③等待部署完成后，通知栏会弹出重启，点击重启；
④切换到GSI，builder number应该可能会有userdebug字样，接下来可进行前述提到的GSI方法（提取、修补、刷入）；
⑤刷入完成后，重启一次手机，就能自动回到原版系统
⑥最后，在原版系统中安装面具，即可管理权限。

###### ☛ 实战案例–侧载提取法

[侧载提取法：1000元的山寨机系统太难用？没关系，我会出手！](https://www.bilibili.com/video/BV1xa4y1c7t1/)

## 注意事项与风险提示

1. **数据备份**：在进行任何Root操作前，务必备份重要数据
2. **保修影响**：Root操作通常会导致设备保修失效
3. **安全风险**：Root后的设备安全性降低，某些应用可能获取过高权限
4. **系统稳定性**：不当的Root操作可能导致系统不稳定或无法启动
5. **银行应用兼容性**：部分银行和支付应用可能无法在Root设备上正常运行
6. **OTA更新**：Root设备通常无法接收OTA更新，需要手动更新

## 参考资料

1. [安卓玩机优化必备！小白也能看懂的ADB入门教程](https://www.bilibili.com/video/BV1V8411C71r/)
2. [手机硬核折腾指南：没刷机包也能获取Root权限？](https://www.bilibili.com/video/BV1m6421c7sb/)
3. [没有刷机包也能ROOT手机？一加与类原生全系通用，有手就会！](https://www.bilibili.com/video/BV1WbokYVEXC/)
4. [Android Developers - ADB Documentation](https://developer.android.com/studio/command-line/adb)
5. [Magisk官方GitHub仓库](https://github.com/topjohnwu/Magisk)
6. [XDA Developers论坛](https://forum.xda-developers.com/)
7. [KernelSU项目](https://github.com/tiann/KernelSU)
8. [联发科深刷提取法：我给山寨机刷了系统，超低配置居然如此流畅！](https://www.bilibili.com/video/BV1J94y1J736/) 
9. [高通深刷提取法：仅售32元的儿童手机不能上网？没关系，我会出手！](https://www.bilibili.com/video/BV19p4y1N7H8/) 
10. [GSI提取法：山寨机的系统到底有多离谱？用奇特的方式挖掘真相！](https://www.bilibili.com/video/BV1ge411w7qq/)
11. [侧载提取法：1000元的山寨机系统太难用？没关系，我会出手！](https://www.bilibili.com/video/BV1xa4y1c7t1/)
12. [手机硬核折腾指南：没刷机包也能获取Root权限？](https://www.bilibili.com/video/BV1m6421c7sb/)


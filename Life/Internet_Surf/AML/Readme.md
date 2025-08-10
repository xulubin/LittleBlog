# Read Me [ Be Careful ! ]

This toolset is designed for flashing and debugging Amlogic chip devices, such as TV boxes and development boards. It provides functionalities to read/write partitions, reboot the device, and obtain device information.

## Features

- Read and write device partitions
- Reboot device
- Enter Fastboot mode
- Obtain device information
- Open current directory in Windows Explorer

## Requirements

- Amlogic device in USB Boot mode
- Windows PC with USB connection

1. Connect your Amlogic device to your PC via USB and ensure it is in USB Boot mode.
2. Run the main executable (YourApp.exe).
3. You will be prompted to enter commands in the command prompt.

## Basic Commands


- `exit`: Exit the program.
- `fb`: Reboot the device into Fastboot mode.
- `btt`: Get device information (model, serial number, memory, etc.).
- `rb`: Reboot the device.
- `pwd`: Show the current directory.
- `open`: Open the current directory in Windows Explorer.

## Tips

- Always backup partitions before performing operations.
- Ensure the addresses match your device's partitions.
- Do not flash unknown `.img` files.
- It is recommended to perform operations in a virtual machine or on a test device to prevent damage to your main device.

## Additional Information

The toolset includes the following files:

- `btt.exe`: Boot Time Tool for device communication.
- `upe.exe`: Universal Programming Engine for flashing and partition operations.
- Various DLLs for ADB, USB drivers, and Cygwin runtime.

---


## Refer

### btt.exe

```bash
btt.exe --help
usage: fastboot [OPTION...] COMMAND...

flashing:
 update ZIP                 Flash all partitions from an update.zip package.
 flashall                   Flash all partitions from $ANDROID_PRODUCT_OUT.
                            On A/B devices, flashed slot is set as active.
                            Secondary images may be flashed to inactive slot.
 flash PARTITION [FILENAME] Flash given partition, using the image from
                            $ANDROID_PRODUCT_OUT if no filename is given.

basics:
 devices [-l]               List devices in bootloader (-l: with device paths).
 getvar NAME                Display given bootloader variable.
 reboot [bootloader]        Reboot device.

locking/unlocking:
 flashing lock|unlock       Lock/unlock partitions for flashing
 flashing lock_critical|unlock_critical
                            Lock/unlock 'critical' bootloader partitions.
 flashing get_unlock_ability
                            Check whether unlocking is allowed (1) or not(0).

advanced:
 erase PARTITION            Erase a flash partition.
 format[:FS_TYPE[:SIZE]] PARTITION
                            Format a flash partition.
 set_active SLOT            Set the active slot.
 oem [COMMAND...]           Execute OEM-specific command.
 gsi wipe|disable           Wipe or disable a GSI installation (fastbootd only).
 wipe-super [SUPER_EMPTY]   Wipe the super partition. This will reset it to
                            contain an empty set of default dynamic partitions.
 snapshot-update cancel     On devices that support snapshot-based updates, cancel
                            an in-progress update. This may make the device
                            unbootable until it is reflashed.
 snapshot-update merge      On devices that support snapshot-based updates, finish
                            an in-progress update if it is in the "merging"
                            phase.

boot image:
 boot KERNEL [RAMDISK [SECOND]]
                            Download and boot kernel from RAM.
 flash:raw PARTITION KERNEL [RAMDISK [SECOND]]
                            Create boot image and flash it.
 --dtb DTB                  Specify path to DTB for boot image header version 2.
 --cmdline CMDLINE          Override kernel command line.
 --base ADDRESS             Set kernel base address (default: 0x10000000).
 --kernel-offset            Set kernel offset (default: 0x00008000).
 --ramdisk-offset           Set ramdisk offset (default: 0x01000000).
 --tags-offset              Set tags offset (default: 0x00000100).
 --dtb-offset               Set dtb offset (default: 0x01100000).
 --page-size BYTES          Set flash page size (default: 2048).
 --header-version VERSION   Set boot image header version.
 --os-version MAJOR[.MINOR[.PATCH]]
                            Set boot image OS version (default: 0.0.0).
 --os-patch-level YYYY-MM-DD
                            Set boot image OS security patch level.

Android Things:
 stage IN_FILE              Sends given file to stage for the next command.
 get_staged OUT_FILE        Writes data staged by the last command to a file.

options:
 -w                         Wipe userdata.
 -s SERIAL                  Specify a USB device.
 -s tcp|udp:HOST[:PORT]     Specify a network device.
 -S SIZE[K|M|G]             Break into sparse files no larger than SIZE.
 --force                    Force a flash operation that may be unsafe.
 --slot SLOT                Use SLOT; 'all' for both slots, 'other' for
                            non-current slot (default: current active slot).
 --set-active[=SLOT]        Sets the active slot before rebooting.
 --skip-secondary           Don't flash secondary slots in flashall/update.
 --skip-reboot              Don't reboot device after flashing.
 --disable-verity           Sets disable-verity when flashing vbmeta.
 --disable-verification     Sets disable-verification when flashing vbmeta.
 --unbuffered               Don't buffer input or output.
 --verbose, -v              Verbose output.
 --version                  Display version.
 --help, -h                 Show this message.
```

### upe.exe

```bash
upe.exe --help
=====Amlogic upgrade firmware through USB(Ver 0.8.1)================
update  <command>       [option device name]    <arg0>  <arg1>  <arg2>  ...
update partition    [dev_no] <part_name>          <image_file_path>
update mwrite       [dev_no]> <image_file_path>    <media_type>     <part_name>      <file_type> [verify file]
update mread        [dev_no]> <media_type>         <part_name>      <file_type>      <image_file_path>
update write        [dev_no]> <media_type>         <part_name>      <file_type>      <image_file_path>
update read         [dev_no] <dump length>        <memory address>
update bulkcmd      [dev_no] <platform-cmd>
update bulkcmd      [dev_no] <platform-cmd>
update identify     [dev_no]
update reset        [dev_no]
update scan         [mptool/msdev]  scan devices and list them
update help
update boot     [dev_no]  <file> <addr> download file and run
update msdev    [dev_no]  get msdev disk_num
update msget    [dev_no]  get msdev state
update msset    [dev_no]  <cmd>         send cmd to msdev

Commands details:
update partition: Burn a partition with a partition image
update mwrite: Burn data to media or memory
update mread: Dump a data from media or memory to pc and save as a file
update tplcmd: like bulkcmd
update bulkcmd: pass and exec a command platform bootloader can support
update write: Down a file to memory
update run: Run code from memory address
update read: Dump data from memory:

Commands Examples:
for cmd partition
                to Burn a boot.img to partition boot: [update partition boot z:\a\b\boot.img]
for cmd bulkcmd
                to initial disk, use: [update bulkcmd "disk_intial 0"]
for cmd bulkcmd
                to run a uboot command printenv with usb console: [update bulkcmd "printenv"]
for cmd mread
                to Dump 2MB data of partition boot to pc and save as boot.dump: [update mread store boot normal 0x200000 boot.dump]
for cmd mwrite
                to Burn a boot.img to partition boot: [update mwrite z:\a\b\boot.img store boot normal]
for cmd write
                to down ddr_init.bin to sram of platform M6: [update write z:\u-boot\build\ddr_init.bin 0xd9000000]
for cmd run
                to run ddr_init.bin which already downed to 0xd9000000: [update run 0xd9000020]
for cmd read
                to read 4bytes meory data from addrss 0x80200000: [update read 4 0x80200000]
=====Amlogic upgrade firmware through USB(Ver 0.8.1)==================
```

---

## Usage[CN]

下面先给出一份中文版的 Readme（整合了 btt.exe 与 upe.exe 的主要用法），然后给出针对你这台 marconi 设备的完整备份方案，所有命令均可直接复制执行。

### 一、fastboot / btt.exe（Android 通用刷机工具）
1. 基本命令  
   ```bash
   btt devices -l        # 列出已连接设备（含路径）
   btt getvar 变量名      # 查看指定 bootloader 变量（如 getvar version）
   btt reboot            # 重启系统
   btt reboot bootloader  # 重启并停留在 bootloader
   ```

2. 刷机 / 擦写  
   ```bash
   btt flashall                    # 自动刷入 $ANDROID_PRODUCT_OUT 下所有镜像
   btt update update.zip           # 刷入完整 OTA 包
   btt flash boot boot.img         # 单独刷入 boot 分区
   btt flash system system.img     # 单独刷入 system 分区
   btt erase data                  # 清空 data 分区
   btt format ext4 data            # 格式化 data 为 ext4
   ```

3. 分区槽位（A/B 设备）  
   ```bash
   btt --slot all flashall         # 两个槽位都刷
   btt set_active a                # 把 a 槽设为活动槽
   ```

4. Boot 镜像高级参数  
   ```bash
   btt boot kernel [ramdisk] [second]   # 仅下载并引导，不刷入
   btt flash:raw boot kernel \
       --cmdline "xxx" --dtb dtb.img    # 打包并刷入 boot.img
   ```

5. 解锁 / 上锁  
   ```bash
   btt flashing unlock               # 解锁
   btt flashing lock                 # 上锁
   btt flashing get_unlock_ability   # 查看是否允许解锁（1=允许）
   ```

6. 常用选项  
   ```bash
   -w                  # 刷完后清空 userdata
   --skip-reboot       # 刷完不自动重启
   --disable-verity    # 禁用 dm-verity
   ```

### 二、upe.exe（Amlogic USB 刷机工具）
1. 扫描设备  
   ```bash
   update scan mptool     # 扫描当前已连接 Amlogic 设备
   update identify 0      # 查看 0 号设备信息
   ```

2. 烧录 / 备份  
   ```bash
   # 烧录
   update partition 0 boot boot.img
   update mwrite 0 boot.img store boot normal
   
   # 备份
   update mread 0 store boot normal 0x01000000 boot-backup.img
   ```

3. 调试命令  
   ```bash
   update bulkcmd 0 "printenv"        # 执行 U-Boot 命令
   update read 0 0x1000 0x01000000    # 从内存 0x01000000 读出 4 KB
   ```

------------------------------------------------
## `Demo.exe`

### 备份

需要处于烧录模式下（设备管理器识别为“**WorldCup Device**”）

打开`demo.exe`，使用`read`语法，需要**4个字段**。

```cmd
read,system,73c00000,system.img
read,vendor,25800000,vendor.img
read,odm,10000000,odm.img
read,vbmeta,1000,vbmeta.img
```

#### **如何获取各分区“十六进制大小”**

`fastboot`模式下获取

(adb连接后，可通过`adb reboot fastboot`进入该模式)

```cmd
>fastboot getvar all
(bootloader) version-baseband:N/A
(bootloader) version-bootloader:U-Boot 2015.01-g112266e3e9-dirty
(bootloader) version:0.4
(bootloader) hw-revision:EVT
(bootloader) max-download-size:0x08000000
(bootloader) serialno:1234567890
(bootloader) product:marconi
(bootloader) off-mode-charge:0
(bootloader) variant:US
(bootloader) battery-soc-ok:yes
(bootloader) battery-voltage:4.2V
(bootloader) partition-type:boot:raw
(bootloader) partition-size:boot:0000000001000000
(bootloader) partition-type:system:ext4
(bootloader) partition-size:system:0000000073c00000
(bootloader) partition-type:vendor:ext4
(bootloader) partition-size:vendor:0000000025800000
(bootloader) partition-type:odm:ext4
(bootloader) partition-size:odm:0000000010000000
(bootloader) partition-type:data:ext4
(bootloader) partition-size:data:00000000e6dfc000
(bootloader) erase-block-size:2000
(bootloader) logical-block-size:2000
(bootloader) secure:no
all: unlocked:yes
Finished. Total time: 0.198s
```

得到 **十六进制值** 直接照抄即可：

- boot   → 1000000
- system → 73c00000
- vendor → 25800000
- odm    → 10000000
- vbmeta → 1000



### 刷入

处于烧录模式下（设备管理器识别为“**WorldCup Device**”）

打开`demo.exe`,使用`write`语法，只需要**3个字段**。

```
write,boot,The\Path\Of\boot.img
```



### 从烧录模式直接切换至fastboot

```cmd
fb
```



---

## 原始参考

```bat
@shift /0
@echo off
chcp 437 >nul
setlocal enabledelayedexpansion

:input_loop
set /p input=Please enter parameters (type 'exit' to quit): 

if /i "%input%"=="exit" (
    goto end_script
) else if /i "%input%"=="fb" (
    upe bulkcmd "reboot fastboot"
) else if /i "%input%"=="btt" (
    btt getvar all
) else if /i "%input%"=="rb" (
    btt reboot
) else if /i "%input%"=="pwd" (
    echo Current directory: %cd%
) else if /i "%input%"=="open" (
    start %cd%
) else (
    for /f "tokens=1,2,3 delims=," %%a in ("%input%") do (
        set first_part=%%b
        set second_part=%%c
        set prefix=%%a
    )
    if /i "!prefix!"=="read" if defined first_part if defined second_part (
        upe mread store !first_part! normal 0x!second_part! !first_part!.img
    ) else (
        echo Incorrect input format. Please enter something like "read,boot,xxxx".
    )
    if /i "!prefix!"=="write" if defined first_part if defined second_part (
        upe partition !first_part! !second_part!
    ) else (
        echo Incorrect input format. Please enter something like "write,boot,xxxx".
    )
)

if %errorlevel% neq 0 (
    if /i "%input%"=="fb" (
        echo The fb failed. Please check the input parameters or relevant environment.
    ) else if /i "%input%"=="btt" (
        echo The btt failed. Please check the input parameters or relevant environment.
    ) else if /i "%input%"=="rb" (
        echo The reboot command failed. Please check the input parameters or relevant environment.
    ) else if /i "%input%"=="pwd" (
        echo Failed to display the current directory.
    ) else (
        if /i "!prefix!"=="up" if defined first_part if defined second_part (
            echo The upe command failed. Please check the input parameters or relevant environment.
        )
    )
) else (
    if /i not "%input%"=="pwd" (
        echo The command was executed successfully.
    )
)

goto input_loop

:end_script
endlocal
```













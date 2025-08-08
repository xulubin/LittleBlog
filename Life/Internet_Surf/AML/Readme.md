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

## Usage

1. Connect your Amlogic device to your PC via USB and ensure it is in USB Boot mode.
2. Run the main executable (YourApp.exe).
3. You will be prompted to enter commands in the command prompt.

## Commands

### Basic Commands

- `exit`: Exit the program.
- `fb`: Reboot the device into Fastboot mode.
- `btt`: Get device information (model, serial number, memory, etc.).
- `rb`: Reboot the device.
- `pwd`: Show the current directory.
- `open`: Open the current directory in Windows Explorer.

### Partition Commands (*Testing*)

- `read,partition,address`: Read the specified partition and save it as `partition.img`. Example: `read,boot,0x12345678`.
- `write,partition,address`: Write the `partition.img` file to the specified address. Example: `write,boot,0x12345678`.

## Advanced Usage

### Backup Partitions

*(Testing)*

To backup important partitions:

```bat
read,boot,0x12345678 
read,recovery,0x23456789 
read,system,0x34567890 
```



### Flash Modified Images

1. Modify the `boot.img` or `recovery.img` file.
2. Flash the modified image using the `write` command. Example: `write,boot,new_boot.img`.

### View Device Information

```bat
btt 
```

This will display information such as chip model, serial number, memory size, storage capacity, and firmware version.

### Reboot Device

```bat
rb
```

Use this to reboot the device after flashing to test if it boots properly.

### Enter Fastboot Mode

```bat
fb
```

This will reboot the device into Fastboot mode, allowing you to use ADB or Fastboot commands.

### Open Current Directory

```bat
pwd 
open 
```

These commands show the current directory path and open it in Windows Explorer for easy access to the `.img` files.

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


# ubuntu-autoinstall-iso
Generate custom Ubuntu ISOs with your own autoinstall YAML

This project is forked from https://github.com/c0dyhi11/ubuntu-20-04-autoinstall but re-written in python with support for more options.

Automated installation is achieved with Ubuntu's autoinstall: https://ubuntu.com/server/docs/install/autoinstall-reference

# Compatibility
This tool is capable of building custom desktop or live-server installer images for Ubuntu 20.04 or newer. 

# WARNING
**Booting an image generated with this tool could automatically wipe your computer's largest block device automatically**

DO NOT attach a bootable USB with this ISO to any computer which has important data on it.

# Usage
## Prepare the environment
This tool may require additional Python modules to function. Use the included `requirements.txt` to install the required modules.
You can do this in a Python virtual environment if you want to keep your system clean.
```
# (optional) Create a virtual environment for python
python3 -m venv my_virtual_environment
# (optional) Activate the virtual environment
source ./my_virtual_environment/bin/activate

# Install the required modules from requirements.txt
pip install -i ./requirements.txt
```

## Customization
To customize the image, you should provide an autoinstall YAML config for the installer to read and a grub.cfg file which points to it.
By default, the tool will copy the `./custom` directory along with the `./grub.cfg` file into the generated ISO.

To get started quickly create a `custom` directory and add two files to it: `meta-data` and `user-data`

The `custom/user-data` file should contain your autoinstall YAML. See the following for information on Ubuntu Autoinstall: https://ubuntu.com/server/docs/install/autoinstall-reference

The `custom/meta-data` file should remain blank. 

You also need to create a `grub.cfg` file which points to your autoinstall config. Below is a simple example which enables autoinstall.
```bash
set timeout=-1

loadfont unicode

set menu_color_normal=white/black
set menu_color_highlight=black/light-gray

menuentry "Ubuntu Autoinstall" {
	set gfxpayload=keep
	linux	/casper/vmlinuz autoinstall ds=nocloud\;s=/cdrom/custom/autoinstall/ ---
	initrd	/casper/initrd
}
menuentry "Ubuntu Manual Install" {
	set gfxpayload=keep
	linux	/casper/vmlinuz ---
	initrd	/casper/initrd
}
grub_platform
if [ "$grub_platform" = "efi" ]; then
menuentry 'Boot from next volume' {
	exit 1
}
menuentry 'UEFI Firmware Settings' {
	fwsetup
}
else
menuentry 'Test memory' {
	linux16 /boot/memtest86+.bin
}
fi
```
After doing the above, you should have the following folder structure.
```
./
├── custom
│   ├── meta-data
|   └── user-data
└── grub.cfg
```
## Build a custom ISO
With your autoinstall YAML and grub.cfg file created, you can build your ISO with the following command
```
/path/to/build_iso.py -v 22.04.3
```
By default this will download the Ubuntu 22.04.3 live-server ISO into your current working directory and will copy your `custom` directory and `grub.cfg` file to the ISO, before generating a new `autoinstall.iso` file.
## Build a custom ISO using the desktop installer
Note, automated installation for the desktop installer is only supported for Ubuntu 23.10+. Previous versions will fail.
```
/path/to/build_iso.py -v 23.10.1 --type desktop
```
## Complex build
The script assumes a number of defaults (live-server installer, amd64 architecture, etc), but you can override many options with cmdline arguments
```
/path/to/build_iso.py -v 23.10.1 --type desktop --import-dir /my_autoinstall_dir --grub-file /my_grub_file --out-file ./my_custom_autoinstall.iso
```
The above sources the autoinstall directory and grub.cfg files from alternative locations and specifies the output ISO filename/path
For an exhaustive list of cmdline options, view the built-in help function:
```
/path/to/build.py --help
```
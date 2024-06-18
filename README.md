# ubuntu-iso-generator
This project contains a simple python script for downloading and customizing Ubuntu ISO files.
This is useful for generating custom ISO images with [Ubuntu Autoinstall YAML](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html) baked-in.

# Getting Started
To get started using this script, first clone the repository, or simply download the `build_iso.py` script.

## Pre-requisites
This tool requires additional Python modules to function. Use the included `requirements.txt` to install the required modules.
You can do this in a Python virtual environment if you want to keep your system clean.
```
# (optional) Create a virtual environment for python
python3 -m venv my_virtual_environment
# (optional) Activate the virtual environment
source ./my_virtual_environment/bin/activate

# Install the required modules from requirements.txt
pip install -r ./requirements.txt
```
## Usage
The most basic usage of this script will simply download the requested ISO image.
```
./build_iso.py -v 22.04.4
```
By default, the live-server ISO is assumed. However, you can change the type, version and architecture to download.
```
./build_iso.py -v 23.10 --type desktop --architecture arm64
```
### Customization
To customize the ISO image, you need to provide a custom `grub.cfg` and/or a directory to import.
```
./build_iso.py -v 24.04 --type desktop --import-dir ./custom/autoinstall --grub-menu ./grub.cfg
```
This is useful for configuring autoinstall deployments. See [Ubuntu Autoinstall](https://canonical-subiquity.readthedocs-hosted.com/en/latest/intro-to-autoinstall.html) for more information.

## Help
The script is self-documented. Simply run `./build_iso.py --help` to get an overview of what arguments are available.
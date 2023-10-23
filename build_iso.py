#!/usr/bin/python3
import os
import sys
import argparse
import pycdlib
from urllib.request import urlretrieve

def build_iso(iso_file, import_dir, grub_file, out_file):
  iso=pycdlib.PyCdlib()
  iso.open(iso_file)
  # Customizations
  for root, dirnames, filenames in os.walk(import_dir):
    iso.add_directory(f"/{root.upper()}", joliet_path=f"/{root}", rr_name=root.split("/")[-1])
    for file in filenames:
      file_path=os.path.join(f"{root}", f"{file}")
      file_perms=os.stat(file_path).st_mode
      iso.add_file(file_path, iso_path=f"/{str.upper(file_path.replace('-','_'))};3", joliet_path=f"/{file_path}", rr_name=file, file_mode=file_perms)
  # GRUB Menu
  iso.rm_file("/BOOT/GRUB/GRUB.CFG;1") # Delete the existing GRUB config and replace
  iso.add_file("grub.cfg", "/BOOT/GRUB/GRUB.CFG;1", joliet_path="/boot/grub/grub.cfg", rr_name="grub.cfg")
  iso.write(out_file)
  iso.close()

def download_iso(iso_base_url, version_num, installer_type, installer_arch):
  iso_filename=f"ubuntu-{version_num}-{installer_type}-{installer_arch}.iso"
  iso_path=f"./{iso_filename}"
  iso_url=f"{iso_base_url}/{version_num}/{iso_filename}"
  if os.path.exists(iso_path):
    print(f"Using existing ISO file: {iso_path}")
  else:
    print(f"Downloading from: {iso_url}")
    urlretrieve(iso_url, iso_path)
  return iso_filename

def main():
  main_cmd=argparse.ArgumentParser(description="Build custom Ubuntu installer ISOs")
  main_cmd.add_argument("-v", "--version", dest="version", required=True, help="The Ubuntu version to download (e.g. 22.04.3)")
  main_cmd.add_argument("-i","--import-dir", dest="import_dir", default="custom", help="Import a directory to your custom ISO (e.g. ./custom)")
  main_cmd.add_argument("-g", "--grub-menu", dest="grub_file", default="grub.cfg", help="Location of the grub.cfg file to import into the ISO")
  main_cmd.add_argument("--iso_url", dest="iso_url", default="https://releases.ubuntu.com", help="The URL where Ubuntu ISOs are located (e.g. https://releases.ubuntu.com)")
  main_cmd.add_argument("-t", "--type", dest="installer_type", default="live-server", help="The installer type to use (e.g. live-server OR desktop)")
  main_cmd.add_argument("--arch", dest="installer_arch", default="amd64", help="The installer architecture to use (e.g. amd64)")
  main_cmd.add_argument("-o", "--out-file", dest="out_file", default="autoinstall.iso", help="The output filename/path of the generated ISO (e.g. ./autoinstall.iso)")
  args = main_cmd.parse_args()
  return args

# Start
runtime=main()
# Check if paths exist
if not os.path.isdir(runtime.import_dir):
  sys.exit(f"The provided import directory, '{runtime.import_dir}', does not exist.")
if not os.path.isfile(runtime.grub_file):
  sys.exit(f"The provided grub file, '{runtime.grub_file}', does not exist.")
# Download source ISO
iso_file=download_iso(iso_base_url=runtime.iso_url,
             version_num=runtime.version,
             installer_type=runtime.installer_type,
             installer_arch=runtime.installer_arch
            )
# Build custom ISO
build_iso(iso_file,
          runtime.import_dir,
          runtime.grub_file,
          runtime.out_file)
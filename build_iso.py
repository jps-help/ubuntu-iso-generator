#!/usr/bin/python3
import os
import sys
import argparse
import pycdlib
from urllib.request import urlretrieve

class ISO_Path():
  def __init__(self, path):
    self.path = path
  def iso_path(self):
    # Generate the ISO9660 filename
    _path = str.upper(self.path)
    _path = str.replace(_path, '-', '_')
    _path = f"/{_path}"
    return _path
  def joliet_path(self):
    # Generate the Joliet filename
    _path = str.upper(self.path)
    _path = f"/{_path}"
    return _path
  def rr_name(self):
    # generate the Rock Ridge filename
    _name = str.split(self.path, '/')
    _name = _name[-1]
    return _name

def build_iso(iso_file, import_dir, out_file, grub_file=None):
  import_dir = os.path.abspath(import_dir)
  import_dir_paths = os.path.split(import_dir)

  iso=pycdlib.PyCdlib()
  iso.open(iso_file)
  # Customizations
  # Each directory and filename require an ISO9660, Joliet, and Rock Ridge filename
  for root, dirnames, filenames in os.walk(import_dir):
    dir = f"{os.path.split(import_dir)[-1]}{str.split(root, import_dir)[-1]}"
    dir = ISO_Path(dir)
    iso.add_directory(iso_path=dir.iso_path(),
                      joliet_path=dir.joliet_path(),
                      rr_name=dir.rr_name())
    for file in filenames:
      src_file = os.path.join(import_dir_paths[0], dir.path, file)
      file_perms = os.stat(src_file).st_mode
      file_path = ISO_Path(os.path.join(dir.path, file))
      iso.add_file(src_file,
                   iso_path=file_path.iso_path(),
                   joliet_path=file_path.joliet_path(),
                   rr_name=file_path.rr_name(),
                   file_mode=file_perms)
  # GRUB Menu
  if grub_file:
    grub_file = os.path.abspath(grub_file)
    iso.rm_file("/BOOT/GRUB/GRUB.CFG;1") # Delete the existing GRUB config and replace
    iso.add_file(grub_file, "/BOOT/GRUB/GRUB.CFG;1", joliet_path="/boot/grub/grub.cfg", rr_name="grub.cfg")
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
  source_args = main_cmd.add_mutually_exclusive_group(required=True)
  source_args.add_argument("-s", "--source-iso", dest='source', help="Provide the path to a locally sourced ISO file to modify. Mutually exclusive with ISO download options.")
  source_args.add_argument("-v", "--version", dest="version", help="The Ubuntu version to download (e.g. 22.04.3)")
  download_args = main_cmd.add_argument_group('Download Arguments', 'Options for ISO downloads')
  download_args.add_argument("-t", "--type", dest="installer_type", default="live-server", help="The installer type to use (e.g. live-server OR desktop)")
  download_args.add_argument("--arch", dest="installer_arch", default="amd64", help="The installer architecture to use (e.g. amd64)")
  download_args.add_argument("--iso_url", dest="iso_url", default="https://releases.ubuntu.com", help="The URL where Ubuntu ISOs are located (e.g. https://releases.ubuntu.com)")
  main_cmd.add_argument("-i","--import-dir", dest="import_dir", help="Import a directory to your custom ISO (e.g. ./custom)")
  main_cmd.add_argument("-g", "--grub-menu", dest="grub_file", help="Location of the grub.cfg file to import into the ISO")
  main_cmd.add_argument("-o", "--out-file", dest="out_file", default="autoinstall.iso", help="The output filename/path of the generated ISO (e.g. ./autoinstall.iso)")
  args = main_cmd.parse_args()
  return args

# Start
runtime=main()
custom=False
if runtime.import_dir: 
  custom=True 
  # Check if path exist
  if not os.path.isdir(runtime.import_dir):
    sys.exit(f"The provided import directory, '{runtime.import_dir}', does not exist.")
if runtime.grub_file:
  custom=True
  # Check if path exists  
  if runtime.grub_file and not os.path.isfile(runtime.grub_file):
    sys.exit(f"The provided grub file, '{runtime.grub_file}', does not exist.")
# Get source ISO
if runtime.source:
  iso_file = os.path.abspath(runtime.source)
  if not os.path.isfile(iso_file):
    sys.exit(f"The provided ISO file, '{runtime.source}', does not exist.")
  print(f"Using source ISO file: '{runtime.source}'")
elif runtime.version:
  iso_file=download_iso(iso_base_url=runtime.iso_url,
               version_num=runtime.version,
               installer_type=runtime.installer_type,
               installer_arch=runtime.installer_arch
              )
else:
  sys.exit("Unknown error while acquiring the ISO file")

# Build custom ISO only if customizations provided.
if custom == False:
  print(f'No customizations provided. Exiting without making changes.')
  sys.exit(0)
else:
  print('Generating custom ISO...')  
  build_iso(iso_file,
            runtime.import_dir,
            runtime.out_file,
            runtime.grub_file)
  print('Done.')
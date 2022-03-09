# 036bootstrap

Bootstrap Scripts for Arch Linux/Debian and Oracle Linux Auto-Configuration Script

![Alt text](brandwhite.png?raw=true "Title")

## Prerequisites of use

- Medium understanding of GNU/Linux
- Some binaries, depending on the script
- For Python scripts, you need Python 3.5 or above

## Getting Started

- :bulb: **Features for bootstrap scripts**
  - [Xanmod Kernel](https://xanmod.org/): Best kernel for x86_64
  - [yay](https://github.com/Jguer/yay): AUR Helper (Only Arch Linux)
  - [OhMyZsh](https://ohmyz.sh/): Best Framework for zsh
  - XFCE, GNOME, KDE menu options for install
  - You can install has a VMware Guest
  - INTEL, NVIDIA, ATI, AMD menu options for install
  - Some Optimizations
  - Extra Software

- :warning: **Only Works in x86_64 Processors, UEFI Systems and GPT Disks**
  - MBR systems is not compatible here

- :warning: **These scripts use f2fs filesystem for SSD/NVMe devices**
  - Is the best filesystem for Linux and friendly for NAND like devices

- :warning: **Make a partition table before**
  - You would get some errors like EFI missing partition, etc. For example this GNU parted scripts for partitioning works well

```bash
#HDD 20 GB
parted --script /dev/sda \
    mklabel gpt \
    mkpart primary fat32 1MiB 200MiB \
    set 1 esp on \
    mkpart primary ext4 200MiB 19.0GiB \
    mkpart primary linux-swap 19.0GiB 100% \
    print

#SSD 20 GB
parted --script /dev/sda \
    mklabel gpt \
    mkpart primary fat32 1MiB 200MiB \
    set 1 esp on \
    primary f2fs 200MiB 100% \
    print
```

## Also Python?

- I recommend to use python scripts, works at 100% similar than bash scripts, the performance in python is better
- Static typing is enabled by default, please run your scripts with python3 only
- Ubuntu rolling is not available and suitable for python, only shell 
- Only one module is required, please install pythondialog locally

```bash
$ pip install pythondialog
```

## What About With Arch Linux Bootstrap

- :warning: **Only Works in Arch Linux Based Systems**
  - Other GNU/Linux systems may not work

- :heavy_check_mark: **Use in Arch Linux Live CD, Arch Linux installed systems or Manjaro**

If you are use Arch Linux Live CD you must update the repositories and install git, like this (run as superuser)

```bash
pacman -Sy
pacman -S git
git clone https://github.com/victor7w7r/036bootstrap/
cd ./036bootstrap/shell
chmod +x arch-bootstraper
./arch-bootstraper # If you are not superuser, use with sudo
```

If you are using python, please install python-pip and install pythondialog

```bash
pacman -Sy
pacman -S git python-pip
git clone https://github.com/victor7w7r/036bootstrap/
cd ./python/036bootstrap
pip install pythondialog
python3 arch-bootstraper.py # If you are not superuser, use with sudo
```


If you need to change to another timezone, use this order

- `ln -sf /usr/share/zoneinfo/REGION/CITY /etc/localtime"`

If you need to change to another locales, use this changes below, if you want more commands, please visit [Arch Linux Guide](https://wiki.archlinux.org/title/installation_guide)

```bash
#edit /etc/locale.gen 
vi /etc/locale.gen
#unmark your desired locale
#Save that file and use
locale-gen
```

## What About With Ubuntu Rolling

- :warning: **Please install this software**
  - This scripts works in all GNU/Linux distros but you need this binaries
    - `dialog debootstrap f2fs-tools`

- :warning: **Devel Repositories**
  - This script use Ubuntu Devel repositories for install, at this moment, i didn't have problems with devel packages while testing, but this repository is some unstable, if you have problems in system packages, wait some days and try to run the script again.

You must update the repositories of your GNU/Linux distro and install git, like this (run as superuser)

```bash
apt update
apt install git
git clone https://github.com/victor7w7r/036bootstrap/
cd ./036bootstrap/shell
chmod +x ubuntu-rollingdeb
./ubuntu-rollingdeb #(If you are not superuser, use with sudo)
```

If you want to change the locales and keyboard layout, use this commands

```bash
apt install locales
dpkg-reconfigure tzdata
dpkg-reconfigure locales
```

## What About With Oracle Linux Config

- :bulb: **Features**

  - [Cockpit](https://cockpit-project.org/): Web Control for your server
  - [OhMyZsh](https://ohmyz.sh/): Best Framework for zsh
  - XFCE as a default graphic environment with EPEL repository
  - KVM Hypervisor Suite
  - XRDP remote control
  - You can install has a VMware Guest

- :warning: **Only Works in Oracle Linux 8**
  - YUM commands don't work

- :warning: **This is not a bootstraper**
  - This script assumes that Oracle Linux is installed

You must update the repositories like this and install git, like this (run as superuser)

```bash
dnf update -y
dnf install git -y
git clone https://github.com/victor7w7r/036bootstrap/
cd ./036bootstrap/shell
chmod +x oraclelinux-config
./oraclelinux-config #(If you are not superuser, use with sudo)
```

:warning: For python please install these packages, and use like this

```bash
dnf update -y
dnf install git python39 python39-pip -y
python3.9 -m pip install pythondialog
git clone https://github.com/victor7w7r/036bootstrap/
cd ./036bootstrap/python
python3.9 oraclelinux-config.py
```

## TODO

- [ ] Code Optimization
- [ ] Fix Arch Linux NVME Install

## Development Suite

- Editor: [vscode](https://code.visualstudio.com/)
- Lint and Syntax Check: [ShellCheck](https://marketplace.visualstudio.com/items?itemName=timonwong.shellcheck)
- Operating Systems for tests: [Arch Linux ARM](https://archlinuxarm.org/), [Kali Linux](https://www.kali.org/)

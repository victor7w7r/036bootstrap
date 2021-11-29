# 036bootstrap

Bootstrap Scripts for Arch Linux/Debian and Oracle Linux Auto-Configuration Script

![Alt text](brandwhite.png?raw=true "Title")

## Prerequisites of use

- Medium understanding of GNU/Linux
- Some binaries, depending on the script

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

## What About With Arch Linux Bootstrap

- :warning: **Only Works in Arch Linux Based Systems**
  - Other GNU/Linux systems may not work

- :heavy_check_mark: **Use in Arch Linux Live CD, Arch Linux installed systems or Manjaro**

If you are use Arch Linux Live CD you must update the repositories and install git, like this (run as superuser)

```bash
pacman -Sy
pacman -S git
git clone https://github.com/victor7w7r/036bootstrap/
cd 036bootstrap
chmod +x arch-bootstraper
./arch-bootstraper #(If you are not superuser, use with sudo)
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

## What About With Debian Sid Bootstrap

- :warning: **Please install this software**
  - This scripts works in all GNU/Linux distros but you need this binaries
    - `dialog debootstrap f2fs-tools`

- :warning: **GRUB**
  - In some times, GRUB not works, i have this problem for a long time in the past and i don't have any response of research for fix this problem.

- :warning: **Sid Sid Sid**
  - This script use Debian Sid repositories for install, at this moment, i didn't have problems with Sid packages while testing, but this repository is some unstable, if you have problems in system packages, wait some days and try to run the script again

You must update the repositories of your GNU/Linux distro and install git, like this (run as superuser)

```bash
apt update
apt install git
git clone https://github.com/victor7w7r/036bootstrap/
cd 036bootstrap
chmod +x sid-debootstraper
./sid-debootstraper #(If you are not superuser, use with sudo)
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
cd 036bootstrap
chmod +x oraclelinux-config
./oraclelinux-config #(If you are not superuser, use with sudo)
```

## Spanish Folder?

I born and live in Ecuador, of course i made a spanish scripts version, sorry for my bad english. :blush:

## TODO

- [ ] Debian Sid GRUB
- [ ] Code Optimization

## Development Suite

- Editor: [vscode](https://code.visualstudio.com/)
- Lint and Syntax Check: [ShellCheck](https://marketplace.visualstudio.com/items?itemName=timonwong.shellcheck)
- Operating System Tests: [Arch Linux ARM](https://archlinuxarm.org/)

## Thanks at this repositories for code snippets

- [Desktopify](https://github.com/wimpysworld/desktopify) (Convert Ubuntu Server for Raspberry Pi to a Desktop.)
- [ZeroTierOne](https://github.com/zerotier/ZeroTierOne) (Free VPN)

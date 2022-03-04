from subprocess import call, PIPE, Popen
from sys import stdin, stdout, platform, version_info, argv
from platform import machine
from os import getuid, system, path
from re import search
from urllib.request import urlopen
from termios import tcgetattr, tcsetattr, TCSADRAIN
from time import sleep
from tty import setcbreak
from dialog import Dialog

d = Dialog(dialog="dialog")
d.set_background_title("036 Creative Studios")

DISKENVIRONMENT: str = ""
DISK: str = ""; ROOTPART: str = ""
EFIPART: str= " "; SWAPPART: str = ""
SUDOUSER: str = ""; LANGUAGE: int = 0

def main() -> None: 
    
    global DISKENVIRONMENT
    global LANGUAGE
    
    if(argv[0] == 'chroot'):
        DISKENVIRONMENT = argv[1]
        LANGUAGE = argv[2]
        corechroot()
    else: corelive()
    
def corelive() -> None: 
    utils.clear(); language(); cover(); verify(); diskenv(); 

def corechroot() -> None:
    debian(); configurator(); hostnamer(); localer(); newuser(); swapper()
    xanmod(); graphical(); ohmyzsh(); optimizations(); software(); finisher()
    
def printer(type: str, position: int, additional: str = "") -> None:
    
    GREEN = '\033[92m';  WARNING = '\033[93m'; FAIL = '\033[91m';  ENDC = '\033[0m';

    DICTIONARY_ENG=(
		"Your Operating System is not GNU/Linux, exiting",
		"This scripts only works in UEFI/EFI systems, consider change your PC or check your BIOS",
		"This script is only intended to run on x86_64 PCs.",
		"This PC doesn't have internet connection, please check",
		"f2fs-tools is not available in this system, please install it",
		"dialog is not available in this system, please install it",
		"debootstrap is not available in this system, please install it",
		"All dependencies is ok!",
		"The device has a DOS Label Type (MBR), this script only works with gpt",
		"You choose a SSD device, but this device is rotational, if is that not the case, that device is USB",
		"You choose a HDD device, but this device is not rotational, please check and run this script again",
		"The device doesn't have a EFI partition",
		"The device has the EFI partition in other side than "+additional+" 1",
		"There's not disks available in your system, please verify!!!",
		"All the partitions of the device are mounted in your system, please unmount the desired partition",
		"=============== FORMAT ROOT FILESYSTEM AND SWAP =============== \n",
		"=============== FORMAT ROOT FILESYSTEM =============== \n",
		"=============== FORMAT EFI AND MOUNT =============== \n",
		"unmounted filesystems succesfully",
		"=============== DEBOOTSTRAP: INSTALL DEBIAN SID CORE =============== \n",
		"=============== DEBIAN: UPDATE SID REPOSITORIES =============== \n",
		"=============== INSTALL CORE PACKAGES =============== \n",
		"=============== GENERATE FSTAB AND ROOT PASSWORD FOR YOUR SYSTEM =============== \n",
		"=============== CONFIGURE GRUB =============== \n",
		"=============== START NETWORKMANAGER AND SSH SERVICES =============== \n",
		"=============== ADD A USER TO A SUDO GROUP =============== \n",
		"We create a script called omz.sh in your home directory, after reboot, use chmod +x at omz.sh",
		"=============== OPTIMIZATIONS =============== \n",
		"Please reboot and remove your live media",
        "Your Python versión is less than 3.5, exiting",
        "You are not superuser, please run as root"
	)

    DICTIONARY_ESP=(
        "Este sistema no es GNU/Linux, saliendo",
		"Este script sólo trabaja en UEFI/EFI, considera cambiar tu PC o verifica tu BIOS",
		"Este script sólo se ejecuta en procesadores de x86_64.",
		"No tienes conexión a internet, por favor revisa e inténtalo de nuevo",
		"f2fs-tools no está disponible en tu sistema, por favor instálalo",
		"dialog no está disponible en tu sistema, por favor instálalo",
		"debootstrap no está disponible en tu sistema, por favor instálalo",
		"Todo ok!",
		"Este dispositivo tiene una tabla de tipo DOS (MBR), este script sólo trabaja con GPT",
		"Elegiste como SSD, pero este dispositivo es rotacional, si no es el caso, entonces este dispositivo es USB",
		"Elegiste como HDD, pero este dispositivo no es rotacional, por favor verifica y ejecuta este script otra vez",
		"Este dispositivo no tiene una partición EFI",
		"Este dispositivo tiene una partición EFI en otro lado que no sea "+additional+" 1",
		"No hay discos disponibles en tu sistema, por favor verifica!!!",
		"Todas las particiones de este dispositivo están montadas, por favor desmonta tu partición de elección",
		"=============== FORMATEAR PARTICIONES DE RAIZ E INTERCAMBIO =============== \n",
		"=============== FORMATEAR PARTICION DE RAIZ =============== \n",
		"=============== FORMATEAR EFI Y MONTARLO =============== \n",
		"Particiones desmontadas de manera exitosa",
		"=============== DEBOOTSTRAP: INSTALAR LA BASE DE DEBIAN SID =============== \n",
		"=============== DEBIAN: ACTUALIZAR REPOSITORIOS DE SID =============== \n",
		"=============== INSTALAR PAQUETES BASE =============== \n",
		"=============== GENERAR FSTAB Y ONTRASEÑA DE ROOT PARA EL SISTEMA =============== \n" 
		"=============== CONFIGURAR GRUB =============== \n",
		"=============== INICIAR NETWORKMANAGER Y SERVICIOS DE SSH =============== \n",
		"=============== AGREGAR UN USUARIO DE SUDO =============== \n",
		"Hemos creado un script llamado omz.sh en tu carpeta de home, después de reiniciar, usa chmod +x omz.sh",
		"=============== OPTIMIZACIONES =============== \n",
		"Por favor reinicia y quita tu medio de live",
        "Tu versión de Python es menor que 3.5, saliendo",
        "Tú no eres superusuario, por favor ejecuta como root"
	)

    if LANGUAGE == 1:
        if type == "print": print(f"{DICTIONARY_ENG[position]}")
        elif type == "info": print(f"[{GREEN}+{ENDC}] INFO: {DICTIONARY_ENG[position]}")
        elif type == "warn": print(f"[{WARNING}*{ENDC}] WARNING: {DICTIONARY_ENG[position]}")
        elif type == "error": print(f"[{FAIL}!{ENDC}] ERROR: {DICTIONARY_ENG[position]}")
        else: print(f"[?] UNKNOWN: {DICTIONARY_ENG[position]}")
    else:
        if type == "print": print(f"{DICTIONARY_ESP[position]}")
        elif type == "info": print(f"[{GREEN}+{ENDC}] INFO: {DICTIONARY_ESP[position]}")
        elif type == "warn": print(f"[{WARNING}*{ENDC}] WARNING: {DICTIONARY_ESP[position]}")
        elif type == "error": print(f"[{FAIL}!{ENDC}] ERROR: {DICTIONARY_ESP[position]}")
        else: print(f"[?] UNKNOWN: {DICTIONARY_ESP[position]}")

def reader(position: int) -> str:
    
    DICTIONARY_ENG=(
		"Disk Environment",
		"Please choose your disk type \n",
		"Hard Drive Disk",
		"Solid State Disk or NVMe",
		"DANGER!!!: Your destination device would be formatted and empty, formatting always cause data loss, PLEASE backup all your data before start",
		"Before installing, we recomend that your disk has the next partition scheme, before install\n\n",
		"GNU Parted script example for format a 20GB disk\n\n",
		"Choose a device",
		"Choose a device for install",
		"Select a root partition",
		"Please select a partition \n",
		"Select a swap partition",
		"Please select a swap partition \n",
		"DANGER ZONE!!!",
		"This partitions will be format Continue? \n",
		"Press Enter to continue...",
		"This PC is a Laptop?",
		"Please write your hostname (ex: A036-debian)",
		"America/Guayaquil is the timezone by default, if you want to change, here is the command\n\n ln -sf /usr/share/zoneinfo/REGION/CITY /etc/localtime",
		"Choose your locale, if you want to change to other locales, check the README of the Github of this project",
		"Write your new user: ",
		"Graphical Environment",
		"Choose a GUI, these are the common used, this script recommends XFCE",
		"More Sofware!!",
		"This script has a little pack of software, Do you like it?\n",
		'READY!!!, Your PC is succesfully installed with Debian Sid, if you have errors, please report at 036bootstraper in GitHub'
	)

    DICTIONARY_ESP=(
        "Entorno de Disco",
		"Seleccione su tipo de disco para la instalación \n",
		"Disco Duro",
		"Disco Sólido o NVMe",
		"CUIDADO!!!: Tu dispositivo debe estar vacío y formateado, formatear siempre mata tus datos, POR FAVOR haz una copia antes de continuar",
		"Antes de instalar, se recomienda que tu disco tenga esta tabla de particiones\n\n",
		"GNU Parted script, es un ejemplo para un disco de 20GB\n\n",
		"Elige un dispositivo",
		"Elige un dispositivo para instalar",
		"Partición de raíz",
		"Por favor seleccione su partición de raíz \n",
		"Seleccione la partición de swap",
		"Por favor seleccione una partición de intercambio \n",
		"ZONA DE PELIBRO!!!",
		"Estas particiones se van a formatear ¿Continuar?",
		"Presione Enter para continuar...",
		"¿Esta es una Laptop?",
		"Por favor escriba su hostname (ex: A036-debian)",
		"America/Guayaquil es el timezone por defecto, si quieres cambiarlo por algún otro, aquí está la orden\n\n ln -sf /usr/share/zoneinfo/REGION/CITY /etc/localtime",
		"Elige tu Locale, si quieres cambiar a otros, revisa el README dentro del GitHub de este proyecto",
		"Escribe tu nuevo usuario: ",
		"Entorno gráfico",
		"Selecciona un GUI, estos son los más usados, Este script recomienda XFCE",
		"Más Sofware!!",
		"Este script tiene un pequeño pack de software, ¿Te gusta?\n ",
		'LISTO!!!, Tu PC ya instalo de manera correcta a Debian Sid, si hubo errores, repórtalo en 036bootstrap / GitHub' 
	)

    if LANGUAGE == 1: return DICTIONARY_ENG[position]
    else: return DICTIONARY_ESP[position]
    
def commandverify(cmd: str) -> bool:
    return call("type " + cmd, shell=True, 
        stdout=PIPE, stderr=PIPE) == 0

def language() -> None:
    
    global LANGUAGE
    
    print("Bienvenido /  Welcome")
    print("Please, choose your language / Por favor selecciona tu idioma")
    print("1) English")
    print("2) Espanol")
    
    option: str = utils.char()

    if option == "1": LANGUAGE=1
    elif option == "2": LANGUAGE=2
    else: exit(1)

def cover() -> None:
    utils.clear()
    print(r'''                                     `"~>v??*^;rikD&MNBQku*;`                                           ''')
    print(r'''                                `!{wQNWWWWWWWWWWWWWWWNWWWWWWNdi^`                                       ''')
    print(r'''                              .v9NWWWWNRFmWWWWWWWWWWWWga?vs0pNWWWMw!                                    ''')
    print(r'''                            !9WWWWWWU>`>&WWWWWWUH!_JNWWWWWQz  ^EWWWWg|                                  ''')
    print(r'''                           _SWWWWWNe: /RWWWWWWNNHBRuyix&WWWWWg2?-"VNWWW6_                               ''')
    print(r'''                         "kWWWWWNz. .zNWWWWWWw=, ^NsLQNW**MWWWW&WQJuNWWWNr.                             ''')
    print(r'''                       .FNWWWWNu. rL&WWWWWWg!!*;^Jo!*BN0aFx)>|!;;;;;!~\r)xFwaao?|,                      ''')
    print(r'''                     .sNWWWWMi` -,#WWWWWWNi"` Siwu UWv  .;^|^;`               .!*lUSF*;                 ''')
    print(r'''                    )BWWWWWo.   9NWWWWWW0; ;PvLc*aU&^ |L=-``.;>*=                   ;)wmkL_             ''')
    print(r'''                  _QWWWWWq"   .aWWWWWWWs`  rF<>\^gQ, /i   ,;;.  !2                      ,*k0F\`         ''')
    print(r'''                 *NWWWWNv   ,/&WWWWWWNr "!SL92l)BU.  ^x   x. L,  I_                        `>P&F;       ''')
    print(r'''               `2WWWWWg;    !BWWWWWWD"   .s;!\xNa     /L,   !L`  P,                           .?&gr     ''')
    print(r'''              ,QWWWWWS`  >;LWWWWWWWk`_;!\u|  ^Ml        ;~!^,  `iv                              `?Ng^   ''')
    print(r'''             ^BWWWWWi   *i7NWWWWWWc "a;;?ii"~NV             `;?},                                 ,9WF  ''')
    print(r'''            >WWWWWB!  ` ;8WWWWWWM=  r>`;F/2wNc          .;||!,                                      oW#.''')
    print(r'''           ?WWWWW#"  `2;7NWWWWW&_ =_=u%ir`>Wi                                                        PW6''')
    print(r'''          rWWWWWc   `||>WWWWWWU.  r^?7;!v*W)                                                         ,WW|''')
    print(r'''         ^NWWWB!  ! \jrmWWWWWw  `vL.k*\vkW$>rr*r;`        ;rL{7)>!`                                   mWF''')
    print(r'''        .BWWW$,   ,u. PWWWWW) ,r`)|)!__LWv     `;L"     |s>:```._|JuL                                 qWE''')
    print(r'''        uWWWH` .vi"Fo*WWWWN>   ^v  r*`>W}                                                             &Ws ''')
    print(r'''       ;WWWP`  `=*ox_pWWWB; ^)i`9xr,#7W*            .     ,\*`                                       |WW! ''')
    print(r'''       SWWD` >LLr^_y*NWWQ"  ,<?P~|iF0W}            ~;   v_ `o;                                      .0WU''')
    print(r'''      ^WW0,.!F2xULFi5WW0` >7vr!!z_`*Wv             `|;;^!,~!`                                      .8W8.''')
    print(r'''      dWN;`>JyrkIr`!NWN! ,uFia!9?*2WI                                                             ;QWD.''')
    print(r'''     =WW7`_S)~Fxv| xWWi ;}drqa=;=uWRNmL,                                                         rWWt`  ''')
    print(r'''     DWP`;LiL;}c*rsWW&`,Po_e7L/ =Nc `>oD$aaw%ouic7)*r>=|^^~!;;;;;;;;;;;;;~^\>rvL{JctxiiiiuusoF2kgBS/  ''')
    print(r'''    ;WN\\Uy>*rF.,pWWWr-;?J"vov^^Nu         `.,"_;!~^\=>r*v?LL{}Jjjjjjj}}7?vr>\^!;____-""",,,..``    ''')
    print(r'''    iW?_**>^;>"~&EeWg=|liv*s!~?NL''')
    print(r'''    wWc*$>*~~L6Ni QW! \Uursx >WJ''')
    print(r'''    2M)o*_F "R0; .Wd~U7,``;*iN>''')
    print(r'''    xWe?vI7cMu`  ,W&>xssr~=PB|''')
    print(r'''    "W% ,cBZ_    `M2l\/i,,QQ,''')
    print(r'''     |U$di_       UBu>i)yBy`''')
    print(r'''                  ^Wx,rDR!''')
    print(r'''                   \ZUl^''')
    print(r'''.oPYo. .oPYo. .pPYo.   .oPYo.                       o   o                 .oPYo.   o              8  o                ''')
    print(r'''8  .o8     `8 8        8    8                       8                     8        8              8                   ''')
    print(r'''8 .P`8   .oP` 8oPYo.   8      oPYo. .oPYo. .oPYo.  o8P o8 o    o .oPYo.   `Yooo.  o8P o    o .oPYo8 o8 .oPYo. .oPYo.  ''')
    print(r'''8.d` 8    `b. 8`  `8   8      8  `` 8oooo8 .oooo8   8   8 Y.  .P 8oooo8       `8   8  8    8 8    8  8 8    8 Yb..   ''')
    print(r'''8o`  8     :8 8.  .P   8    8 8     8.     8    8   8   8 `b..d` 8.            8   8  8    8 8    8  8 8    8   `Yb. ''')
    print(r'''`YooP` `YooP` `YooP`   `YooP` 8     `Yooo` `YooP8   8   8  `YP`  `Yooo`   `YooP`   8  `YooP` `YooP`  8 `YooP` `YooP. ''')
    print(r''':.....::.....::.....::::.....:..:::::.....::.....:::..::..::...:::.....::::.....:::..::.....::.....::..:.....::.....:''')
    print(r''':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::''')
    print(r''':::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::''')

def verify() -> None:

    if version_info < (3, 5):
        utils.clear(); printer("error",29); exit(1)
    if platform != "linux":
        utils.clear(); printer("error",0); exit(1)
    if getuid() != 0:
        utils.clear(); printer("error",30); exit(1)
    if not path.exists('/sys/firmware/efi'):
        utils.clear(); printer("error",1); exit(1)
    if machine() != "x86_64":
        utils.clear(); printer("error",2); exit(1)
    try: urlopen('http://google.com')
    except: utils.clear(); printer("error",3); exit(1)
    if not commandverify("fsck.f2fs"):
        utils.clear(); printer("error",4); exit(1)
    if not commandverify("dialog"):
        utils.clear(); printer("error",5); exit(1)
    if not commandverify("debootstrap"):
        utils.clear(); printer("error",6); exit(1)
        
    printer("print",7)
    
    spinner = utils.spinning()
    for _ in range(15):
        stdout.write(next(spinner))
        stdout.flush(); sleep(0.1)  
        stdout.write('\b')

def diskenv() -> None:
    
    global DISKENVIRONMENT
        
    choices = [("HDD",reader(2)),("SSD-NVMe",reader(3))]
    response = d.menu(reader(1), 15, 50, 4, choices)
    if(response[0] == "ok" and response[1] == reader(2)):
        DISKENVIRONMENT="HDD"; disclaimer()
    elif(response[0] == "ok" and response[1] == reader(3)):
        DISKENVIRONMENT="SSD"; disclaimer()
    else: utils.clear(); exit(0)

def disclaimer() -> None:
    
    utils.clear(); d.msgbox(reader(4),8,70)
    
    if(DISKENVIRONMENT == "HDD"):
    
        d.msgbox(reader(5)+""" \n \n
                
            GPT -> \n
            1.	/dev/sdX1	EFI			200MB		fat32		esp\n
            2.	/dev/sdX2	archlinux	>20GB		ext4		primary\n
            3.	/dev/sdx3	linux-swap	2GB-4GB		swap		primary\n\n
    
            """+reader(6)+"""
                
            mklabel gpt \n 
            mkpart EFI fat32 1MiB 200MiB \n 
            set 1 esp on \n 
            mkpart ROOT ext4 200MiB 19.0GiB \n
            mkpart SWAP linux-swap 19.0GiB 100% \n """,8,70)
    
    elif(DISKENVIRONMENT == "SSD"):

        d.msgbox(reader(5)+""" \n \n
                
            GPT -> \n
            1.	/dev/sdX1	EFI			200MB		fat32		esp\n
            2.	/dev/sdX2	archlinux	>20GB		f2fs/ext4		primary\n

            """+reader(6)+"""
                
            mklabel gpt \n
            mkpart EFI fat32 1MiB 200MiB \n
            set 1 esp on \n
            mkpart ROOT f2fs 200MiB 100% \n """,8,70)

def diskverify(device: str) -> None:
    utils.clear()

    global DISK
    
    EFI: str = ""; EFIORDER: str = ""
    BLOCK: str = ""; ROTATIONAL: str = ""
    
    LABEL: str = Popen(r"""#!/bin/bash
                        blkid -o value -s PTTYPE """ +device
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
    
    if(LABEL == "dos"): printer("error",8); exit(1)
    if(search("sd[[:alpha:]]",device)):
        EFI = Popen(r"""#!/bin/bash
                        fdisk -l """+device+""" | sed -ne '/EFI/p' """ +device, 
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        EFIORDER = Popen(r"""#!/bin/bash
                            echo """+device+""" | sed -ne '/[[:alpha:]]1/p' 
                        """
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        
        if(DISKENVIRONMENT == "SSD"):
            BLOCK = Popen(r"""#!/bin/bash
                            echo """+device+""" | cut -d "/" -f3"""
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
            
            ROTATIONAL = Popen(r"""#!/bin/bash
                            cat /sys/block/+"""+BLOCK+"""+/queue/rotational"""
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
            
            if(ROTATIONAL == "1"): printer("error",9); exit(1)
            
        if(DISKENVIRONMENT == "HDD"):
            BLOCK = Popen(r"""#!/bin/bash
                            echo """+device+""" | cut -d "/" -f3"""
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
            
            ROTATIONAL = Popen(r"""#!/bin/bash
                            cat /sys/block/+"""+BLOCK+"""+/queue/rotational"""
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
            
            if(ROTATIONAL == "0"): printer("error",10); exit(1)
            
        if(EFI == ""): printer("error",11); exit(1)
        if(EFIORDER == ""): printer("error",12,device); exit(1)  
        
        DISK = device; rootpartmenu()
        
    elif(search("mmcblk[[:digit:]]",device)):
        EFI = Popen(r"""#!/bin/bash
                        fdisk -l """+device+""" | sed -ne '/EFI/p' """ +device, 
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        EFIORDER = Popen(r"""#!/bin/bash
                            echo """+device+""" | sed -ne '/[[:alpha:]]1/p' 
                        """
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        
        if(DISKENVIRONMENT == "HDD"): printer("error",10); exit(1)
        if(EFI == ""): printer("error",11); exit(1)
        if(EFIORDER == ""): printer("error",12,device); exit(1)  
        
        DISK = device; rootpartmenu()
        
    elif(search("nvme[[:digit:]]",device)):
        EFI = Popen(r"""#!/bin/bash
                        fdisk -l """+device+""" | sed -ne '/EFI/p' """ +device, 
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        EFIORDER = Popen(r"""#!/bin/bash
                            echo """+device+""" | sed -ne '/[[:alpha:]]1/p' 
                        """
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        
        if(DISKENVIRONMENT == "HDD"): printer("error",10); exit(1)
        if(EFI == ""): printer("error",11); exit(1)
        if(EFIORDER == ""): printer("error",12,device); exit(1)  
        
        DISK = device; rootpartmenu()

def diskmenu() -> None:
    utils.clear()    
    
    global ROOTPART
    
    COUNT: int = 0; BLOCK: list = []; DIRTYDEVS: list = []
    MODEL: int = 0; DEVICE: str = ""; ARRAY: list = []
    
    DEVICES: list = Popen(r"""find /dev/disk/by-path/ | sed 's/^\/dev\/disk\/by-path\///'
                            """, shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
    
    for DEVICETEMP in DEVICES:
        DIRTYDEVS.append(Popen('''#!/bin/bash
                                readlink "/dev/disk/by-id/''' +DEVICETEMP+'''"''', shell=True, 
                                stdout=PIPE).stdout.read().decode('utf-8')
                                    .rstrip().split("\n")[0]); COUNT += 1
        
    DIRTYDEVS = list(filter(('').__ne__, DIRTYDEVS)); 
    
    if(COUNT == 0): printer("error",13); exit(1)
    COUNT = 0
    
    for DEV in DIRTYDEVS:
        ABSOLUTEPARTS = Popen(r"""#!/bin/bash
                            echo """+DEV+""" | sed 's/^\.\.\/\.\.\//\/dev\//' | sed '/.*[[:alpha:]]$/d' | sed '/blk[[:digit:]]$/d' | sed '/nvme[[:digit:]]n[[:digit:]]$/d'""", 
                            shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        
        if ABSOLUTEPARTS == "":
            BLOCK.append(Popen(r"""#!/bin/bash
                                echo """+DEV+""" | sed 's/^\.\.\/\.\.\///'""", 
                                shell=True, stdout=PIPE).stdout.read()
                                .decode('utf-8').rstrip().split("\n")[0])
    for PART in BLOCK:
        DEVICE: str = "/dev/"+PART
        BLOCKSTAT: str = BLOCK[COUNT]
        SIZE: str = Popen(r'''#!/bin.bash
                    lsblk -no SIZE /dev/'''+PART+''' | head -1 | sed s/..//''',
                    shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        MODEL: str = Popen(r'''#!/bin.bash
                cat /sys/class/block/'''+BLOCKSTAT+'''/device/model''',
                shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        ARRAY.append([DEVICE, MODEL + " " + SIZE]); COUNT +=1
        
    response = d.menu(reader(8), 15, 50, 4, ARRAY)
    if(response[0] == "ok"): diskverify(response[1])
    else: utils.clear(); exit(0)

def rootpartmenu() -> None:
    utils.clear()
    VERIFY: list = []; TYPE: str = ""; EFIPART: str = ""
    COUNT: int = 0; COUNTMOUNT: int = 0
    ISMOUNTED: str = ""; ROOTPARTS: list = []
    
    EFIPART = Popen(r'''#!/bin/bash
                        fdisk -l '''+DISK+''' | sed -ne /EFI/p | cut -d " " -f1'''
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
    
    if(search("sd[[:alpha:]]",DISK)):
        VERIFY = Popen(r"""#!/bin/bash
                    find """+DISK+"""* | sed '/[[:alpha:]]$/d'"""
                ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
    elif(search("mmcblk[[:digit:]]",DISK)):
        VERIFY = Popen(r"""#!/bin/bash
                    find """+DISK+"""* | sed '/k[[:digit:]]$/d'"""
                ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
    elif(search("nvme[[:digit:]]n[[:digit:]]",DISK)):
        VERIFY = Popen(r"""#!/bin/bash
                    find """+DISK+"""* | sed '/e[[:digit:]]n[[:digit:]]$/d'"""
                ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
        
    for PART in VERIFY:
        if(PART != EFIPART):
            ISMOUNTED = Popen(r"""#!/bin/bash
                        lsblk """+PART+"""* |  sed -ne '/\//p'"""
                    ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
            if(ISMOUNTED != ""): COUNTMOUNT += 1
            else: ROOTPARTS.append([PART,TYPE])
            COUNT += 1
    if(COUNTMOUNT == COUNT): utils.clear(); printer("error", 14); exit(1)
    
    response = d.menu(reader(10), 15, 50, 4, ROOTPARTS)
    
    if(response[0] == "ok"):
        ROOTPART = response[1]; swapmenu(response[1])
    else: utils.clear(); exit(0)

def swapmenu(temp: str) -> None:
    if(temp == ""): utils.clear(); exit(0)
    utils.clear()
    if(DISKENVIRONMENT == "HDD"):
        VERIFY: str = ""; TYPE: str = ""
        COUNT: int = 0; COUNTMOUNT: int = 0
        ISMOUNTED: int = 0; SWAPPARTS: list = []
        
        if(search("sd[[:alpha:]]",DISK)):
            VERIFY = Popen(r"""#!/bin/bash
                        find """+DISK+"""* | sed '/[[:alpha:]]$/d'"""
                    ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
        elif(search("mmcblk[[:digit:]]",DISK)):
            VERIFY = Popen(r"""#!/bin/bash
                        find """+DISK+"""* | sed '/k[[:digit:]]$/d'"""
                    ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
        elif(search("nvme[[:alpha:]]",DISK)):
            VERIFY = Popen(r"""#!/bin/bash
                        find """+DISK+"""* | sed '/e[[:digit:]]$/d'"""
                    ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
            
        for PART in VERIFY:
            if(PART != EFIPART):
                if(PART != ROOTPART):
                    ISMOUNTED = Popen(r"""#!/bin/bash
                            lsblk """+PART+""" |  sed -ne '/\//p'"""
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
                if(ISMOUNTED != ""): COUNTMOUNT += 1
                else: SWAPPARTS.append([PART,TYPE])
                COUNT += 1
                
        if(COUNTMOUNT == COUNT): utils.clear(); printer("error", 14); exit(1)
        
        response = d.menu(reader(12), 15, 50, 4, SWAPPARTS)
        
        if(response[0] == "ok"):
            SWAPPART = response[1]; diskformat(response[1])
        else: utils.clear(); exit(0)
    elif(DISKENVIRONMENT == "SSD"): diskformat("pass")
    
def diskformat(temp: str) -> None:
    if(temp == ""): utils.clear(); exit(0)
    utils.clear()
    if(DISKENVIRONMENT == "HDD"):
        if d.yesno(reader(14)+"""\n"""+EFIPART+""" (EFI) \n
                    """+ROOTPART+""" (ROOT) \n """+SWAPPART+""" (SWAP)""",8,60) == d.OK:
            printer("print",19)
            print(Popen(r"""#!/bin/bash
                            mkfs.ext4 """ +ROOTPART+ """
                            mkswap """ +SWAPPART+ """
                            swapon """ +SWAPPART
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip())
            print(" ")
            print("=============== OK =============== \n")
            input(reader(15))
        else: utils.clear(); exit(0)
    elif(DISKENVIRONMENT == "SSD"):
        if d.yesno(reader(14)+"\n"+EFIPART+" (EFI) \n "+ROOTPART+" (ROOT)",7,60) == d.OK:
            printer("print",20)
            print(Popen(r"""#!/bin/bash
                            mkfs.f2fs """ +ROOTPART
                        ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip())
            print(" ")
            print("=============== OK =============== \n")
            input(reader(15))
        else: utils.clear(); exit(0)
        
    printer("print",21); 
    print(Popen(r"""#!/bin/bash
                    mkfs.fat -F32 """ +EFIPART
                ,shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip())  
    Popen("mount "+ROOTPART+" /mnt; mkdir /mnt/efi", shell=True)
    Popen("mount "+EFIPART+" /mnt/efi", shell=True)
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15)); debootstraper()

def unmounter() -> None:
    utils.clear()
    if(DISKENVIRONMENT == "HDD"):
        Popen(r"""
                #!/bin/bash
                umount /mnt/proc/
                umount /mnt/sys/
                umount /mnt/dev/
                umount """+ROOTPART+"""
                swapoff """+SWAPPART, shell=True)
    elif(DISKENVIRONMENT == "SSD"):
                Popen(r"""
                #!/bin/bash
                umount /mnt/proc/
                umount /mnt/sys/
                umount /mnt/dev/
                umount """+ROOTPART, shell=True)
    printer("print",18); exit(0)

def debootstraper() -> None:
    utils.clear(); printer("print",19)
    proc = Popen(r"""
                        #!/bin/bash
                        debootstrap --arch amd64 sid /mnt https://deb.debian.org/debian/
                        mount -t proc /proc /mnt/proc/
                        mount -t sysfs /sys /mnt/sys/
                        mount -o bind /dev /mnt/dev/
                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    for line in iter(proc.stdout.readline, b''):
        print(line.rstrip())

    Popen("genfstab -U /mnt >> /mnt/etc/fstab", shell=True)
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15)); toggler()

def toggler() -> None:
    Popen("cp " +__file__+ "/mnt/deb-setupper.py", shell=True) 
    Popen(r"""
            #!/bin/bash
            chroot /mnt /bin/bash  \
                pip install pythondialog && python3 ./arch-setupper.py chroot """ +DISKENVIRONMENT+""" """+LANGUAGE
        , shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

def debian() -> None:
    utils.clear(); printer("print",20)

    Popen('echo "deb http://deb.debian.org/debian sid main contrib non-free" > /etc/apt/sources.list', shell=True)
    Popen('echo "deb-src http://deb.debian.org/debian sid main contrib non-free" >> /etc/apt/sources.list', shell=True)
    
    proc = Popen(r"""
                    #!/bin/bash
                    apt update
                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    for line in iter(proc.stdout.readline, b''):
        print(line.rstrip())

    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))
    utils.clear(); printer("print",21)
    
    proc = Popen(r"""
                    #!/bin/bash
                    apt install -y sudo locales git wget aptitude grub-efi-amd64 vim \
                    grub-efi efibootmgr net-tools network-manager-gnome dialog \
                    openssh-server python rsync screen unrar p7zip zsh linux-image-amd64 \
                    firmware-linux firmware-linux-free firmware-linux-nonfree util-linux gnupg
                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    for line in iter(proc.stdout.readline, b''):
        print(line.rstrip())
        
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))
    utils.clear()

def configurator() -> None:
    
    if d.yesno(reader(16),8,60) == d.OK:
        proc = Popen(r"""
                    #!/bin/bash
                    tasksel install laptop
                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
    
    utils.clear(); printer("print",22)
    SDA1 = Popen(r"""#!/bin/bash
                    /usr/sbin/blkid -s UUID -o value """ + EFIPART, 
                shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
    
    SDA2 = Popen(r"""#!/bin/bash
                    /usr/sbin/blkid -s UUID -o value """ + ROOTPART, 
                shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
    
    if(DISKENVIRONMENT == "HDD"):
        SDA3 = Popen(r"""#!/bin/bash
                /usr/sbin/blkid -s UUID -o value """ + SWAPPART, 
            shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        Popen('echo "UUID='+SDA2+'         /             ext4      defaults              1      1" > /etc/fstab', shell=True)
        Popen('echo "UUID='+SDA1+'         /boot/efi     vfat      defaults              0      0" > /etc/fstab', shell=True)
        Popen('echo "UUID='+SDA3+'         none          swap      sw                    0      0" > /etc/fstab', shell=True)
    
    if(DISKENVIRONMENT == "SSD"):
        Popen('echo "UUID='+SDA2+'         /             f2fs      discard              1      1" > /etc/fstab', shell=True)
        Popen('echo "UUID='+SDA1+'         /boot/efi     vfat      defaults              0      0" > /etc/fstab', shell=True)
    
    call("passwd",shell=True)
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))

def hostnamer() -> None:
    response = d.inputbox(reader(17), 8, 80)
    if(response[0] == "ok" ):
        Popen(r"""
            #!/bin/bash
            echo """+response[1]+""" > /etc/hostname
            echo 127.0.1.1 """+response[1]+"""  >> /etc/hosts
            """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        
    elif(response[0] == "cancel" ): exit(0)

def localer() -> None:
    utils.clear(); d.msgbox(reader(18))
    Popen(r"""
            #!/bin/bash
        ln -sf /usr/share/zoneinfo/America/Guayaquil /etc/localtime
        hwclock --systohc
        """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    choices = [("Spanish/Español","es_ES"),("English","en_US")]
    response = d.menu(reader(19), 12, 50, 4, choices)
    if(response[0] == "ok" and response[1] == "Spanish/Español"):
        Popen("sed -i 's/^#es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen &> /dev/null", shell=True)
        Popen("echo 'LANG=\"es_ES.UTF-8\"' > /etc/default/locale", shell=True)
        Popen("echo 'LC_TIME=\"es_ES.UTF-8\"' >> /etc/default/locale", shell=True)
        Popen("echo 'LANGUAGE=\"es_EC:es_ES:es\"' >> /etc/default/locale", shell=True)
    elif(response[0] == "ok" and response[1] == "English"):
        Popen("sed -i 's/^#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen &> /dev/null", shell=True)
        Popen("echo 'LANG=\"en_US.UTF-8\"' > /etc/default/locale", shell=True)
        Popen("echo 'LC_TIME=\"en_US.UTF-8\"' >> /etc/default/locale", shell=True)
        Popen("echo 'LANGUAGE=\"es_US:en\"' >> /etc/default/locale", shell=True)
    else: utils.clear(); exit(0)

def newuser() -> None:
    
    global SUDOUSER
    
    utils.clear(); print("print",25)
    SUDOUSER = input(reader(20))
    call("/usr/sbin/adduser "+SUDOUSER,shell=True)
    call("/usr/sbin/usermod -aG sudo  "+SUDOUSER,shell=True)
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))

def swapper() -> None:
    utils.clear()
    print("=============== SWAPPING =============== \n")
    
    if(DISKENVIRONMENT == "HDD"):
        Popen("echo \"vm.swappiness=60\" >> /etc/sysctl.conf", shell=True)
    if(DISKENVIRONMENT == "SSD"):
        pass
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))

def xanmod() -> None:
    utils.clear()
    print( "=============== XANMOD KERNEL =============== \n" )
    
    Popen("echo 'deb http://deb.xanmod.org releases main' | tee /etc/apt/sources.list.d/xanmod-kernel.list", shell=True)
    Popen("wget -qO - https://dl.xanmod.org/gpg.key | apt-key --keyring /etc/apt/trusted.gpg.d/xanmod-kernel.gpg add -", shell=True)
    Popen("apt update && apt install linux-xanmod -y", shell=True)
    Popen("apt remove linux-image-amd64 -y", shell=True)
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))
    
def graphical() -> None:
    utils.clear()
    choices = [
        ("XFCE","Xfce Desktop Environment"),
        ("GNOME","GNOME Desktop Environment"),
        ("KDE","KDE Desktop Environment"),
        ("XORG","Minimal xorg Desktop"),
        ("CUTEFISH","Cutefish Desktop (Beta)"),
        ("NOGUI","No GUI")
    ]
    response = d.menu(reader(22), 15, 50, 4, choices)
    
    if(response[0] == "ok" and response[1] == "XFCE"):
        utils.clear()
        print("=============== XFCE =============== \n")
        proc = Popen(r"""
                    #!/bin/bash
                    apt install -y xserver-xorg xfce4 xfce4-goodies xfce4-indicator-plugin \
                    ttf-ubuntu-font-family firefox gdm3 grub-customizer nemo cinnamon-l10n
                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
        
    elif(response[0] == "ok" and response[1] == "GNOME"):
        utils.clear()
        print("=============== GNOME =============== \n")
        proc = Popen(r"""
                    #!/bin/bash
                    apt install -y task-gnome-desktop \
                    ttf-ubuntu-font-family firefox grub-customizer nemo cinnamon-l10n
                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    elif(response[0] == "ok" and response[1] == "KDE"):
        utils.clear()
        print("=============== KDE =============== \n")
        proc = Popen(r"""
                    #!/bin/bash
                    apt install -y task-kde-desktop ttf-ubuntu-font-family firefox \
                    grub-customizer nemo cinnamon-l10n
                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    elif(response[0] == "ok" and response[1] == "XORG"):
        utils.clear()
        print("=============== XORG ONLY =============== \n")
        proc = Popen(r"""
                    #!/bin/bash
                    apt install -y xserver-xorg
                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
        
    elif(response[0] == "ok" and response[1] == "NOGUI"): return
    else: exit(0)

def ohmyzsh() -> None:
    
    utils.clear()
    print("=============== OMZ =============== \n")
    Popen("touch /home/"+SUDOUSER+"/omz.sh", shell=True)
    Popen("echo '#!/bin/bash' > /home/"+SUDOUSER+"/omz.sh", shell=True)
    Popen(r'echo \'sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"\' >> /home/'+SUDOUSER+'/omz.sh', shell=True)
    Popen(r'echo \'sed -i -e "s/ZSH_THEME=.*/ZSH_THEME=\"pmcgee\"/" .zshrc\' >> /home/'+SUDOUSER+'/omz.sh', shell=True)
    Popen(r'echo \'sed -i -e "/^source $ZSH.*/i ZSH_DISABLE_COMPFIX=true" .zshrc\' >> /home/'+SUDOUSER+'/omz.sh', shell=True)
    Popen(r'echo \'git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting\' >> /home/'+SUDOUSER+'/omz.sh', shell=True)
    Popen(r'echo \'git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions\' >> /home/'+SUDOUSER+'/omz.sh', shell=True)
    Popen(r'echo \'sed -i -e "s/plugins=(.*/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/" .zshrc\' >> /home/'+SUDOUSER+'/omz.sh', shell=True)
    Popen('chown '+SUDOUSER+' /home/'+SUDOUSER+'/omz.sh', shell=True)
    Popen('chmod +x /home/'+SUDOUSER+'/omz.sh', shell=True)
    
    Popen("touch /root/omz.sh", shell=True)
    Popen("echo '#!/bin/bash' > /root/omz.sh", shell=True)
    Popen(r'echo \'sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"\' >> /root/omz.sh', shell=True)
    Popen(r'echo \'sed -i -e "s/ZSH_THEME=.*/ZSH_THEME=\"pmcgee\"/" .zshrc\' >> /root/omz.sh', shell=True)
    Popen(r'echo \'sed -i -e "/^source $ZSH.*/i ZSH_DISABLE_COMPFIX=true" .zshrc\' >> /root/omz.sh', shell=True)
    Popen(r'echo \'git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting\' >> /root/omz.sh', shell=True)
    Popen(r'echo \'git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions\' >> /root/omz.sh', shell=True)
    Popen(r'echo \'sed -i -e "s/plugins=(.*/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/" .zshrc\' >> /root/omz.sh', shell=True)
    Popen('chmod +x /root/omz.sh', shell=True)
    
    printer("print",31)

    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))

def optimizations() -> None:
    utils.clear(); printer("print",27)
    proc = Popen(r"""
                    #!/bin/bash
                    sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT=".*"/GRUB_CMDLINE_LINUX_DEFAULT="loglevel=0 nowatchdog"/' \
                    /etc/default/grub &> /dev/null
                    /usr/sbin/grub-mkconfig -o /boot/grub/grub.cfg
                    systemctl mask lvm2-monitor
                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    for line in iter(proc.stdout.readline, b''):
        print(line.rstrip())
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))

def software() -> None:
    utils.clear()

    if d.yesno(reader("24")+"""\n -> gdebi \n -> synaptic \n 
			-> aptitude \n -> libwnck-common \n -> libwnck22 \n 
			-> baobab \n ->hfsutils \n -> hfsprogs \n 
			-> ntfs-3g \n -> exfat-fuse \n -> exfat-utils \n
            -> gparted \n -> xarchiver \n -> wine \n
            -> playonlinux \n ->preload \n -> xrdp """ ,20,65) == d.OK:
        
        utils.clear()
        print("=============== SOFTWARE =============== \n")
        
        proc = Popen(r"""
                    #!/bin/bash
                    apt install -y gdebi synaptic aptitude libwnck-common \
                    libwnck22 baobab hfsutils hfsprogs ntfs-3g \
                    exfat-fuse exfat-utils gparted xarchiver wine playonlinux xrdp preload \
                    numix-gtk-theme numix-icon-theme-circle
                    
                adduser xrdp ssl-cert
                systemctl enable xrdp
                systemctl enable xrdp-sesman
                systemctl enable preload
                systemctl mask lvm2-monitor

                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
    
        print("=============== OK =============== \n")
        input(reader(15))
    else: utils.clear(); return

def finisher() -> None:
    
    utils.clear(); d.msgbox(reader(25),7,50)
    Popen("rm -f /deb-setupper.py &> /dev/null", shell=True)
    utils.clear()
    Popen("umount /boot/efi &> /dev/null", shell=True)
    utils.clear(); printer("print", 28); exit(0)
    

class utils:
    
    def clear() -> None: system('clear')
    
    def char() -> str:
        fd = stdin.fileno()
        oldSettings = tcgetattr(fd)
        try:
            setcbreak(fd)
            answer = stdin.read(1)
        finally:
            tcsetattr(fd, TCSADRAIN, oldSettings)
        return answer
    
    def spinning():
        while True:
            for cursor in '|/-\\':
                yield cursor

if __name__ == "__main__":
    main()
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
    
    if argv[0] == 'chroot':
        DISKENVIRONMENT = argv[1]
        LANGUAGE = argv[2]
        corechroot()
    else: corelive()
    
def corelive() -> None: 
    utils.clear(); language(); cover(); verify(); diskenv(); disclaimer(); diskmenu()

def corechroot() -> None:
    configurator(); hostnamer(); localer(); newuser(); liquorix()
    graphical(); drivers(); aur(); ohmyzsh(); swapper(); optimizations()
    software(); finisher()

def printer(type: str, position: int, additional: str = "") -> None:
    
    GREEN = '\033[92m';  WARNING = '\033[93m'; FAIL = '\033[91m';  ENDC = '\033[0m'

    DICTIONARY_ENG=(
		"Your Operating System is not GNU/Linux, exiting",
		"This scripts only works in UEFI/EFI systems, consider change your PC or check your BIOS",
		"This script is only intended to run on x86_64 PCs.",
		"Arch Linux pacman is not available in this system, this system isn't Arch Linux?",
		"This PC doesn't have internet connection, please check",
		"Updating Arch Repositories...",
		"lsb_release is not available in this system, installing",
		"Your Operating System is not Arch Linux, exiting",
		"f2fs.tools is not available in this system, installing",
		"dialog is not available in this system, installing",
		"pacstrap is not available in this system, installing",
		"All dependencies is ok!",
		"The device has a DOS Label Type (MBR), this script only works with GPT",
		"You choose a SSD device, but this device is rotational, if is that not the case, that device is USB",
		"You choose a HDD device, but this device is not rotational, please check and run this script again",
		"The device doesn't have a EFI partition",
		"The device has the EFI partition in other side than "+additional+"1",
		"There's not disks available in your system, please verify!!!",
		"All the partitions of the device are mounted in your system, please unmount the desired partition",
		"=============== FORMAT ROOT FILESYSTEM AND SWAP =============== \n",
		"=============== FORMAT ROOT FILESYSTEM =============== \n",
		"=============== FORMAT EFI AND MOUNT =============== \n",
		"unmounted filesystems succesfully",
		"=============== PACSTRAP: INSTALL LINUX BASE AND CORE PACKAGES =============== \n",
		"Something failed inside the chroot, not unmounting filesystems so you can investigate.",
		"Please umount all partitions, and restart this script",
		"=============== ROOT PASSWORD FOR YOUR SYSTEM =============== \n",
        "=============== CONFIGURE GRUB =============== \n",
        "=============== START NETWORKMANAGER AND SSH SERVICES =============== \n",
        "=============== ADD A USER TO A SUDO GROUP =============== \n",
        "=============== AUR (YAY ASKS YOU YOUR PASSWORD, PAY ATTENTION) ===============  \n",
        "We create a script called omz.sh in your home directory, after reboot, use chmod +x at omz.sh",
        "=============== OPTIMIZATIONS =============== \n",
        "We create a script called software.sh in your home directory, after reboot, use chmod +x at software.sh",
        "Please reboot and remove your live media",
        "Your Python versión is less than 3.5, exiting",
        "You are not superuser, please run as root"
	)

    DICTIONARY_ESP=(
        "Este sistema no es GNU/Linux, saliendo",
		"Este script sólo trabaja en UEFI/EFI, considera cambiar tu PC o verifica tu BIOS",
		"Este script sólo se ejecuta en procesadores de x86_64.",
		"Arch Linux pacman no está disponible, ¿Acaso esto no es Arch Linux?",
		"No tienes conexión a internet, por favor revisa e inténtalo de nuevo",
		"Actualizando repositorios de Arch...",
		"lsb_release no está disponible, instalando",
		"Tu sistema operativo no es Arch Linux, saliendo",
		"f2fs.tools no está disponible, instalando",
		"dialog is no está disponible, instalando",
		"pacstrap no está disponible, instalando",
		"Todo ok!",
		"Este dispositivo tiene una tabla de tipo DOS (MBR), este script sólo trabaja con GPT",
		"Elegiste como SSD, pero este dispositivo es rotacional, si no es el caso, entonces este dispositivo es USB",
		"Elegiste como HDD, pero este dispositivo no es rotational, por favor verifica y ejecuta este script otra vez",
		"Este dispositivo no tiene una partición EFI",
		"Este dispositivo tiene una partición EFI en otro lado que no sea "+additional+"1",
		"No hay discos disponibles en tu sistema, por favor verifica!!!",
		"Todas las particiones de este dispositivo están montadas, por favor desmonta tu partición de elección",
		"=============== FORMATEAR PARTICIONES DE RAIZ E INTERCAMBIO =============== \n",
		"=============== FORMATEAR PARTICION DE RAIZ =============== \n",
		"=============== FORMATEAR EFI Y MONTARLO =============== \n",
        "Particiones desmontadas de manera exitosa",
		"=============== PACSTRAP: INSTALAR LA BASE DE LINUX Y PAQUETES CORE  =============== \n",
		"Algo falló en el chroot, no se desmontarán los sistemas de archivos, así que puedes investigar.",
		"Por favor desmonta tus particiones y reinicia este script",
		"=============== CONTRASEÑA DE ROOT PARA EL SISTEMA =============== \n",
		"=============== CONFIGURAR GRUB =============== \n",
		"=============== INICIAR NETWORKMANAGER Y SERVICIOS DE SSH =============== \n",
		"=============== AGREGAR UN USUARIO DE SUDO =============== \n",
		"=============== AUR (YAY PREGUNTA POR TU CONTRASEÑA, ESTATE ATENTO) ===============  \n",
		"Hemos creado un script llamado omz.sh en tu carpeta de home, después de reiniciar, usa chmod +x omz.sh",
		"=============== OPTIMIZACIONES =============== \n",
		"Hemos creado un script llamado software.sh en tu carpeta de home, después de reiniciar, usa chmod +x software.sh",
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
		"Before installing, we recomend that your disk has the next partition scheme\n\n",
		"GNU Parted script example  for format a 20GB disk\n\n",
		"Choose a device",
		"Choose a device for install",
		"Select a root partition",
		"Please select a partition \n",
		"Select a swap partition",
		"Please select a swap partition \n",
		"DANGER ZONE!!!",
		"This partitions will be format Continue? ",
		"Press Enter to continue...",
		"Please write your hostname (ex: A036-arch)",
		"America/Guayaquil is the timezone by default, if you want to change, here is the command\n\n ln -sf /usr/share/zoneinfo/REGION/CITY /etc/localtime",
		"Choose your locale, if you want to change to other locales, check the README of the Github of this project",
		"Write your new user: ",
		"Graphical Environment",
		"Choose a GUI, these are the common used, this script recommends XFCE",
		"Graphical Drivers",
		"Choose your GPU drivers",
		"If you are executing Arch Linux as a guest",
		"More Sofware!!",
		"This script has a little pack of software, Do you like it?\n",
		"READY!!!, Your PC is succesfully installed with Arch Linux, if you have errors, please report at 036bootstrap in GitHub"
        "Choose your procesor"
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
		"Por favor seleccione a swap partition \n",
		"ZONA DE PELIBRO!!!",
		"Estas particiones se van a formatear ¿Continuar? ",
		"Presione Enter para continuar...",
		"Por favor escriba su hostname (ej: A036-arch)",
		"America/Guayaquil es el timezone por defecto, si quieres cambiarlo por algún otro, aquí está la orden\n\n ln -sf /usr/share/zoneinfo/REGION/CITY /etc/localtime",
		"Elige tu Locale, si quieres cambiar a otros, revisa el README dentro del GitHub de este proyecto",
		"Escribe tu nuevo usuario: ",
		"Entorno Gráfico",
		"Selecciona un GUI, estos son los más usados, Este script recomienda XFCE",
		"Drivers de gráficos",
		"Elige tu controlador de GPU",
		"Si ejecutas como invitado",
		"Más Sofware!!",
		"Este script tiene un pequeño pack de software, ¿Te gusta?\n",
		"LISTO!!!, Tu PC ya instalo de manera correcta a Arch Linux, si hubo errores, repórtalo en 036bootstrap / GitHub"
        "Elige tu procesador"
	)
   
    if LANGUAGE == 1: return DICTIONARY_ENG[position]
    else: return DICTIONARY_ESP[position]

def commandverify(cmd: str) -> bool:
    return call("type " + cmd, shell=True, stdout=PIPE, stderr=PIPE) == 0

def language() -> None:
    
    global LANGUAGE
    
    print("Bienvenido /  Welcome")
    print("Please, choose your language / Por favor selecciona tu idioma")
    print("1) English"); print("2) Espanol")
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
        utils.clear(); printer("error",35); exit(1)
    if platform != "linux":
        utils.clear(); printer("error",0); exit(1)
    if getuid() != 0:
        utils.clear(); printer("error",36); exit(1)
    if not path.exists('/sys/firmware/efi'):
        utils.clear(); printer("error",1); exit(1)
    if machine() != "x86_64":
        utils.clear(); printer("error",2); exit(1)
    if not commandverify("pacman"):
        utils.clear(); printer("error",3); exit(1)
    try: urlopen('http://google.com')
    except: utils.clear(); printer("error",4); exit(1)

    printer("print",5); call("pacman -Sy &> /dev/null", shell=True)
    
    if not commandverify("lsb_release"):
        printer("print",6)
        call("pacman -S lsb-release --noconfirm &> /dev/null", shell=True)
        
    LSB: str = Popen("lsb_release -is", 
                    shell=True, stdout=PIPE).stdout.read().decode('utf-8').replace("\n", "")
        
    if LSB != "Arch":
        utils.clear(); printer("error",7); exit(1)
    
    if not commandverify("fsck.f2fs"):
        printer("print",8)
        call("pacman -S f2fs-tools --noconfirm &> /dev/null", shell=True)
    
    if not commandverify("dialog"):
        printer("print",9)
        call("pacman -S dialog --noconfirm &> /dev/null", shell=True)
        
    if not commandverify("pacstrap"):
        printer("print",10)
        call("pacman -S arch-install-scripts --noconfirm &> /dev/null", shell=True)
        
    call("pacman -S ncurses --noconfirm &> /dev/null", shell=True)
    printer("print",11)
    
    spinner = utils.spinning()
    for _ in range(15):
        stdout.write(next(spinner))
        stdout.flush(); sleep(0.1)  
        stdout.write('\b')

def diskenv() -> None:
    
    global DISKENVIRONMENT
        
    choices = [("HDD",reader(2)),("SSD-NVMe",reader(3))]
    response = d.menu(reader(1), 15, 50, 4, choices)
    if response[0] == "ok" and response[1] == "HDD":
        DISKENVIRONMENT="HDD"
    elif response[0] == "ok" and response[1] == "SSD-NVMe":
        DISKENVIRONMENT="SSD"
    else: utils.clear(); exit(0)
    
def disclaimer() -> None:
    
    utils.clear()
    d.msgbox(reader(4),8,70)
    
    if DISKENVIRONMENT == "HDD":
    
        d.msgbox(reader(5)+f"""
            GPT ->
            1.	/dev/sdX1	EFI			200MB		fat32		esp
            2.	/dev/sdX2	archlinux	>20GB		ext4		primary
            3.	/dev/sdx3	linux-swap	2GB-4GB		swap		primary
            {reader(6)}
            mklabel gpt
            mkpart EFI fat32 1MiB 200MiB
            set 1 esp on
            mkpart ROOT ext4 200MiB 19.0GiB
            mkpart SWAP linux-swap 19.0GiB 100%""",20,70)
    
    elif DISKENVIRONMENT == "SSD":

        d.msgbox(reader(5)+f"""
            GPT ->
            1.	/dev/sdX1	EFI			200MB		fat32		esp
            2.	/dev/sdX2	archlinux	>20GB		f2fs/ext4		primary
            {reader(6)}  
            mklabel gpt
            mkpart EFI fat32 1MiB 200MiB
            set 1 esp on
            mkpart ROOT f2fs 200MiB 100% """,20,70)
    
def diskverify(device: str) -> None:

    global DISK
    utils.clear()
    
    EFI: str = ""; EFIORDER: str = ""
    BLOCK: str = ""; ROTATIONAL: str = ""
    
    LABEL: str = Popen(f"blkid -o value -s PTTYPE {device}",
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
    
    if LABEL == "dos": printer("error",12); exit(1)
    if search("sd[A-Za-z]",device):
        EFI = Popen(f"fdisk -l {device} | sed -ne '/EFI/p'", 
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        EFIORDER = Popen(f"echo {EFI} | sed -ne '/[[:alpha:]]1/p'",
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        
        if DISKENVIRONMENT == "SSD":
            BLOCK = Popen(f'echo {device} | cut -d "/" -f3',
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
            
            ROTATIONAL = Popen(f"cat /sys/block/{BLOCK}/queue/rotational",
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
            
            if ROTATIONAL == "1": printer("error",13); exit(1)
            
        if DISKENVIRONMENT == "HDD":
            BLOCK = Popen(f'echo {device} | cut -d "/" -f3',
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
            
            ROTATIONAL = Popen(f"cat /sys/block/{BLOCK}/queue/rotational",
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
            
            if(ROTATIONAL == "0"): printer("error",14); exit(1)
            
        if EFI == "": printer("error",15); exit(1)
        if EFIORDER == "": printer("error",16,device); exit(1)  
        DISK = device; rootpartmenu()
        
    elif search("mmcblk[0-9_-]",device):
        EFI = Popen(f"fdisk -l {device} | sed -ne '/EFI/p'", 
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        EFIORDER = Popen(f"echo {EFI} | sed -ne '/[[:alpha:]]1/p'",
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        
        if DISKENVIRONMENT == "HDD": printer("error",14); exit(1)
        if EFI == "": printer("error",15); exit(1)
        if EFIORDER == "": printer("error",16,device); exit(1)  
        
        DISK = device; rootpartmenu()
        
    elif(search("nvme[0-9_-]",device)):
        EFI = Popen(f"fdisk -l {device} | sed -ne '/EFI/p'", 
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        EFIORDER = Popen(f"echo {EFI} | sed -ne '/[[:alpha:]]1/p'",
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        
        if DISKENVIRONMENT == "HDD": printer("error",14); exit(1)
        if EFI == "": printer("error",15); exit(1)
        if EFIORDER == "": printer("error",16,device); exit(1)  
        
        DISK = device; rootpartmenu()

def diskmenu() -> None:
    
    global ROOTPART
    
    utils.clear()
    
    COUNT: int = 0; BLOCK: list = []; DIRTYDEVS: list = []
    MODEL: int = 0; DEVICE: str = ""; ARRAY: list = []
    
    DEVICES: list = Popen("find /dev/disk/by-path/ | sed 's/^\/dev\/disk\/by-path\///'", 
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
    
    for DEVICETEMP in DEVICES:
        DIRTYDEVS.append(Popen(f'readlink "/dev/disk/by-path/{DEVICETEMP}"', 
                                shell=True, stdout=PIPE).stdout.read().decode('utf-8')
                                .rstrip().split("\n")[0]); COUNT += 1

    DIRTYDEVS = list(filter(('').__ne__, DIRTYDEVS))
    
    if COUNT == 0: printer("error",17); exit(1)
    COUNT = 0
    
    for DEV in DIRTYDEVS:
        ABSOLUTEPARTS = Popen(f"""
                            echo {DEV} | sed 's/^\.\.\/\.\.\//\/dev\//' | sed '/.*[[:alpha:]]$/d' | sed '/blk[[:digit:]]$/d' | sed '/nvme[[:digit:]]n[[:digit:]]$/d'""", 
                            shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        
        if ABSOLUTEPARTS == "":
            BLOCK.append(Popen(f"echo {DEV} | sed 's/^\.\.\/\.\.\///'", 
                                shell=True, stdout=PIPE).stdout.read()
                                .decode('utf-8').rstrip().split("\n")[0])
            
    for PART in BLOCK:
        DEVICE: str = "/dev/"+PART
        BLOCKSTAT: str = BLOCK[COUNT]
        SIZE: str = Popen(f'lsblk -no SIZE /dev/{PART} | head -1 | sed s/..//',
                    shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        MODEL: str = Popen(f'cat /sys/class/block/{BLOCKSTAT}/device/model',
                    shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
        ARRAY.append([DEVICE, MODEL + " " + SIZE]); COUNT +=1
        

    response = d.menu(reader(8), 15, 50, 4, ARRAY)
    if(response[0] == "ok"): diskverify(response[1])
    else: utils.clear(); exit(0)

def rootpartmenu() -> None:
    
    utils.clear()
    
    global ROOTPART; global EFIPART
    
    VERIFY: list = []; TYPE: str = ""
    COUNT: int = 0; COUNTMOUNT: int = 0
    ISMOUNTED: str = ""; ROOTPARTS: list = []

    EFIPART = Popen(f'fdisk -l {DISK} | sed -ne /EFI/p | cut -d " " -f1',
                    shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')[0]
    
    if search("sd[A-Za-z]",DISK):
        VERIFY = Popen(f"find {DISK}* | sed '/[[:alpha:]]$/d'",
                shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
    elif search("mmcblk[0-9_-]",DISK):
        VERIFY = Popen(f"find {DISK}* | sed '/k[[:digit:]]$/d'",
                shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
    elif search("nvme[0-9_-]n[0-9_-]",DISK):
        VERIFY = Popen(f"find {DISK}* | sed '/e[[:digit:]]n[[:digit:]]$/d'",
                shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
        
    for PART in VERIFY:
        if PART != EFIPART:
            ISMOUNTED = Popen(f"lsblk {PART} | sed -ne '/\//p'",
                    shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
            if ISMOUNTED != "": COUNTMOUNT += 1
            else: ROOTPARTS.append([PART,TYPE])
            COUNT += 1
    if COUNTMOUNT == COUNT: utils.clear(); printer("error", 18); exit(1)
    
    response = d.menu(reader(10), 15, 50, 4, ROOTPARTS)
    
    if(response[0] == "ok"):
        ROOTPART = response[1]; swapmenu(response[1])
    else: utils.clear(); exit(0)
    
def swapmenu(temp: str) -> None:
    
    utils.clear()
    
    global SWAPPART
    
    if temp == "": utils.clear(); exit(0)
    if DISKENVIRONMENT == "HDD":
        VERIFY: str = ""; TYPE: str = ""
        COUNT: int = 0; COUNTMOUNT: int = 0
        ISMOUNTED: int = 0; SWAPPARTS: list = []
        
        if search("sd[A-Za-z]",DISK):
            VERIFY = Popen(f"find {DISK}* | sed '/[[:alpha:]]$/d'",
                    shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
        elif(search("mmcblk[0-9_-]",DISK)):
            VERIFY = Popen(f"find {DISK}* | sed '/k[[:digit:]]$/d'",
                    shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
        elif(search("nvme[0-9_-]",DISK)):
            VERIFY = Popen(f"find {DISK}* | sed '/e[[:digit:]]$/d'",
                    shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
            
        for PART in VERIFY:
            if PART != EFIPART:
                if PART != ROOTPART:
                    ISMOUNTED = Popen(f"lsblk {PART} | sed -ne '/\//p'",
                        shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip()
                if ISMOUNTED != "": COUNTMOUNT += 1
                else: SWAPPARTS.append([PART,TYPE])
                COUNT += 1
                
        if(COUNTMOUNT == COUNT): utils.clear(); printer("error", 18); exit(1)
        
        response = d.menu(reader(12), 15, 50, 4, SWAPPARTS)
        
        if(response[0] == "ok"):
            SWAPPART = response[1]; diskformat(response[1])
        else: utils.clear(); exit(0)
    elif(DISKENVIRONMENT == "SSD"): diskformat("pass")
    
def diskformat(temp: str) -> None:
    
    if temp == "": utils.clear(); exit(0)
    utils.clear()
    if DISKENVIRONMENT == "HDD":
        if d.yesno(reader(14)+f"\n{EFIPART} (EFI) \n{ROOTPART} (ROOT) \n{SWAPPART} (SWAP)",8,60) == d.OK:
            utils.clear()
            printer("print",19)
            utils.live_tasker(f"mkfs.ext4 {ROOTPART}")
            utils.live_tasker(f"mkswap {SWAPPART}")
            call(f"swapon {SWAPPART}", shell=True)
            print(" ")
            print("=============== OK =============== \n")
            input(reader(15))
        else: utils.clear(); exit(0)
    elif DISKENVIRONMENT == "SSD":
        if d.yesno(reader(14)+"\n"+EFIPART+" (EFI) \n "+ROOTPART+" (ROOT)",7,60) == d.OK:
            utils.clear();
            printer("print",20)
            utils.live_tasker(f"mkfs.f2fs {ROOTPART}")
            print(" ")
            print("=============== OK =============== \n")
            input(reader(15))
        else: utils.clear(); exit(0)
    utils.clear()
    printer("print",21); 
    utils.live_tasker(f"mkfs.fat -F32 {EFIPART}")
    call(f"mount {ROOTPART} /mnt; mkdir /mnt/boot; mkdir /mnt/boot/efi", shell=True)
    call(f"mount {EFIPART} /mnt/boot/efi", shell=True)
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15)); pacstraper()
    
def unmounter() -> None:
    utils.clear()
    if DISKENVIRONMENT == "HDD":
        call(f"umount {ROOTPART} /mnt; swapoff {SWAPPART}", shell=True)
    elif DISKENVIRONMENT == "SSD":
        call(f"umount {ROOTPART}", shell=True)
    printer("print",22); exit(0)

def pacstraper() -> None:
    utils.clear(); printer("print",23)
    utils.live_tasker("""
                        pacstrap /mnt base linux linux-firmware nano sudo vi vim git wget \
                        grub efibootmgr reflector os-prober rsync networkmanager neofetch \
                        openssh arch-install-scripts screen unrar p7zip zsh dialog python python-pip""")
    
    call("genfstab -U /mnt >> /mnt/etc/fstab", shell=True)
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15)); toggler()
    
def toggler() -> None:
    call(f"cp {__file__} /mnt/arch-setupper.py", shell=True) 
    call(f"arch-chroot /mnt pip install pythondialog && python3 ./arch-setupper.py chroot {DISKENVIRONMENT} {LANGUAGE}",
            shell=True)
    
def configurator() -> None:
    
    utils.clear(); printer("print",26)
    call("passwd",shell=True)
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))
    
    choices = [("Intel","intel-ucode"),("AMD","amd-code")]
    response = d.menu(reader(28), 15, 50, 4, choices)
    
    if response[0] == "ok" and response[1] == "Intel":
        utils.clear()
        print("=============== INTEL MICROCODE  =============== \n")
        call("pacman -S intel-ucode --noconfirm", shell=True)
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    elif response[0] == "ok" and response[1] == "AMD":
        utils.clear()
        print("=============== AMD MICROCODE  =============== \n")
        call("pacman -S amd-ucode --noconfirm", shell=True)
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    else: utils.clear(); exit(0)

    utils.clear(); printer("print",27)
    utils.live_tasker("grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=arch")
    utils.live_tasker("grub-mkconfig -o /boot/grub/grub.cfg")
    utils.live_tasker("umount /boot/efi")
        
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))
    utils.clear(); printer("print",28)
    
    utils.live_tasker("systemctl enable NetworkManager")
    utils.live_tasker("systemctl enable sshd")
    utils.live_tasker(r"sed -i 's/^#PermitRootLogin\s.*$/PermitRootLogin Yes/' /etc/ssh/sshd_config &> /dev/null")
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))

def hostnamer() -> None:
    response = d.inputbox(reader(16), 8, 80)
    if response[0] == "ok":
        with open('/etc/hostname', 'w') as f: f.write(response[1])
        with open('/etc/hosts', 'a') as f: 
            f.write(f"echo 127.0.1.1 {response[1]}")
    elif response[0] == "cancel" : exit(0)
    
def localer() -> None:
    utils.clear(); d.msgbox(reader(17))
    call("ln -sf /usr/share/zoneinfo/America/Guayaquil /etc/localtime", shell=True)
    call(" hwclock --systohc",shell=True)

    choices = [("Spanish/Español","es_ES"),("English","en_US")]
    response = d.menu(reader(18), 12, 50, 4, choices)
    if response[0] == "ok" and response[1] == "Spanish/Español":
        call("sed -i 's/^#es_ES.UTF-8 UTF-8/es_ES.UTF-8 UTF-8/' /etc/locale.gen &> /dev/null", shell=True)
        utils.live_tasker("locale-gen")
        with open('/etc/locale.conf', 'w') as f: 
            f.writelines([
                'LANG="es_ES.UTF-8"\n',
                'LC_TIME="es_ES.UTF-8"\n',
                'LANGUAGE="es_EC:es_ES:es"\n'
                ])
    elif response[0] == "ok" and response[1] == "English":
        call("sed -i 's/^#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen &> /dev/null", shell=True)
        utils.live_tasker("locale-gen")
        with open('/etc/locale.conf', 'w') as f: 
            f.writelines([
                'LANG="en_US.UTF-8"\n',
                'LC_TIME="en_US.UTF-8"\n',
                'LANGUAGE="es_US:en"\n'
            ])
        
    else: utils.clear(); exit(0)
    
def newuser() -> None:
    
    global SUDOUSER
    
    utils.clear(); print("print",29)
    SUDOUSER = input(reader(19))
    utils.live_tasker(f"useradd --create-home {SUDOUSER}",shell=True)
    utils.live_tasker(f"passwd {SUDOUSER}",shell=True)
    utils.live_tasker(f"usermod -aG wheel,storage,power {SUDOUSER}",shell=True)
    call("sed -i 's/^#.*%wheel ALL=(ALL) ALL$/%wheel ALL=(ALL) ALL/' /etc/sudoers &> /dev/null", shell=True)
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))

def liquorix() -> None:
    
    utils.clear()
    print( "=============== LIQUORIX KERNEL =============== \n" )
    call("sed -i \"/\[multilib\]/,/Include/\"'s/^#//' /etc/pacman.conf", shell=True)
    call("sed -i 's/^SigLevel    = Required DatabaseOptional$/SigLevel = PackageOptional/' /etc/pacman.conf &> /dev/null", shell=True)
    with open('/etc/pacman.conf', 'a') as f: 
        f.writelines([
            '[kernel]\n',
            'Server = https://repo.archlinuxrepo.dev/$arch/$repo'
        ])
    utils.live_tasker("pacman -Syyu linux-lqx linux-lqx-headers --noconfirm", shell=True)
    utils.live_tasker("grub-mkconfig -o /boot/grub/grub.cfg")
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
    response = d.menu(reader(21), 15, 50, 4, choices)
    
    if response[0] == "ok" and response[1] == "XFCE":
        utils.clear()
        print("=============== XFCE =============== \n")
            
        utils.live_tasker("pacman -S xorg --noconfirm")
        utils.live_tasker("pacman -S xfce4 xfce4-goodies xfce4-terminal ttf-ubuntu-font-family --noconfirm")
        utils.live_tasker("pacman -S gtk-engines gtk-engine-murrine gnome-themes-standard --noconfirm")
        utils.live_tasker("pacman -S xdg-user-dirs ttf-dejavu gvfs xfce4-notifyd network-manager-applet --noconfirm")
        utils.live_tasker("pacman -S volumeicon firefox gdm grub-customizer nemo cinnamon-translations --noconfirm")
        utils.live_tasker("systemctl enable gdm")
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
        
    elif response[0] == "ok" and response[1] == "GNOME":
        utils.clear()
        print("=============== GNOME =============== \n")
        
        utils.live_tasker("pacman -S xorg --noconfirm")
        utils.live_tasker("pacman -S gnome gdm gnome-themes-standard network-manager-applet --noconfirm")
        utils.live_tasker("pacman -S firefox grub-customizer nemo cinnamon-translations --noconfirm")
        utils.live_tasker("systemctl enable gdm")

        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    elif response[0] == "ok" and response[1] == "KDE":
        utils.clear()
        print("=============== KDE =============== \n")
            
        utils.live_tasker("pacman -S xorg --noconfirm")
        utils.live_tasker("pacman -S plasma plasma-wayland-session kde-applications gnome-themes-standard --noconfirm")
        utils.live_tasker("pacman -S network-manager-applet firefox grub-customizer nemo cinnamon-translations --noconfirm")
        utils.live_tasker("systemctl enable sddm.service")
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    elif response[0] == "ok" and response[1] == "XORG":
        utils.clear()
        print("=============== XORG ONLY =============== \n")
        
        utils.live_tasker("pacman -S xorg --noconfirm")
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
        
    elif response[0] == "ok" and response[1] == "XORG":
        utils.clear()
        print("=============== CUTEFISH =============== \n")
        
        utils.live_tasker("pacman -S xorg --noconfirm")
        utils.live_tasker("pacman -S cutefish --noconfirm")
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    elif response[0] == "ok" and response[1] == "NOGUI": return
    else: exit(0)
    
def drivers() -> None:
    utils.clear()
    choices = [
        ("Intel","Intel Graphics"),
        ("ATI","ATI Cards"),
        ("AMD","AMD Cards"),
        ("NVIDIA","NVIDIA Cards"),
        ("VMware",reader(24))
    ]
    response = d.menu(reader(23), 15, 70, 4, choices)
    
    if response[0] == "ok" and response[1] == "Intel":
        utils.clear()
        print("=============== INTEL =============== \n")

        utils.live_tasker("pacman -S xf86-video-intel intem-media-driver intel-media-sdk lib32-mesa --noconfirm")

        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    elif response[0] == "ok" and response[1] == "ATI":
        utils.clear()
        print("=============== ATI =============== \n")

        utils.live_tasker("pacman -S xf86-video-ati --noconfirm")
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    elif response[0] == "ok" and response[1] == "AMD":
        utils.clear()
        print("=============== AMD =============== \n")

        utils.live_tasker("pacman -S xf86-video-amdgpu --noconfirm")
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    elif(response[0] == "ok" and response[1] == "NVIDIA"):
        utils.clear()
        print("=============== NVIDIA =============== \n")
            
        utils.live_tasker("pacman -S nvidia nvidia-utils --noconfirm")
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    elif(response[0] == "ok" and response[1] == "VMware"):
        utils.clear()
        print("=============== VMware =============== \n")

        utils.live_tasker("pacman -S gtkmm3 open-vm-tools xf86-input-vmmouse xf86-video-vmware --noconfirm")
        utils.live_tasker("systemctl enable vmtoolsd")
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(15))    
    
def aur() -> None:
    utils.clear(); printer("print",30)

    utils.live_tasker("pacman -S --needed base-devel fakeroot packer go --noconfirm")
    
    call(f"sudo -u {SUDOUSER} bash -c 'cd; git clone https://aur.archlinux.org/yay-bin.git'",shell=True)    
    call(f"sudo -u {SUDOUSER} bash -c 'cd; cd yay-bin; makepkg -si'",shell=True) 
    call(f"sudo -u {SUDOUSER} bash -c 'cd; rm -rf yay-bin'",shell=True) 
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))

def swapper() -> None:
    
    utils.clear()
    print("=============== SWAPPING =============== \n")
    
    if DISKENVIRONMENT == "HDD":
        with open('/etc/sysctl.d/99-sysctl.conf', 'a') as f: 
            f.write("vm.swappiness=60")
    if DISKENVIRONMENT == "SSD":
        call(f"sudo -u {SUDOUSER} bash -c 'yay -S zramswap'", shell=True)
        utils.live_tasker("systemctl enable zramswap.service")
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))    

def ohmyzsh() -> None:
    
    utils.clear()
    print("=============== OMZ =============== \n")
    call(f"touch /home/{SUDOUSER}/omz.sh", shell=True)
    
    with open(f'/home/{SUDOUSER}/omz.sh', 'w') as f: 
        f.writelines([
            "#!/bin/bash\n",
            'sh -c "$(wget https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"\n',
            'sed -i -e \'s/ZSH_THEME=.*/ZSH_THEME=\\\"pmcgee\\\"/\' .zshrc\n',
            "sed -i -e '/^source $ZSH.*/i ZSH_DISABLE_COMPFIX=true' .zshrc\n",
            r"git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting",
            "\n",
            r"git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions",
            "\n",
            "sed -i -e 's/plugins=(.*/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/' .zshrc"
        ])
    
    call(f'chown {SUDOUSER} /home/{SUDOUSER}/omz.sh', shell=True)
    call(f'chmod +x /home/{SUDOUSER}/omz.sh', shell=True)
    call("touch /root/omz.sh'")
    with open('/root/omz.sh', 'w') as f: 
        f.writelines([
            "#!/bin/bash\n",
            'sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"\n',
            'sed -i -e \'s/ZSH_THEME=.*/ZSH_THEME=\\\"pmcgee\\\"/\' .zshrc\n',
            "sed -i -e '/^source $ZSH.*/i ZSH_DISABLE_COMPFIX=true' .zshrc\n",
            r"git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting",
            "\n",
            r"git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions",
            "\n",
            "sed -i -e 's/plugins=(.*/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/' .zshrc"
        ])
    
    call(f'chmod +x /root/omz.sh', shell=True)
    
    printer("print",31)

    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))

def optimizations() -> None:
    
    utils.clear(); printer("print",32)
    call(r"""sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT=".*"/GRUB_CMDLINE_LINUX_DEFAULT="loglevel=0 nowatchdog"/' /etc/default/grub &> /dev/null""", shell=True)
    utils.live_tasker("grub-mkconfig -o /boot/grub/grub.cfg")
    call("systemctl mask lvm2-monitor")
    call("touch /etc/modprobe.d/blacklists.conf")
    with open('/etc/modprobe.d/blacklists.conf', 'w') as f:
        f.writelines([
            "blacklist iTCO_wdt\n",
            "blacklist joydev\n",
            "blacklist mousedev\n",
            "blacklist mac_hid",
        ])
    
    print(" ")
    print("=============== OK =============== \n")
    input(reader(15))

def software() -> None:
    utils.clear()

    if d.yesno(reader("26")+"""\n -> baobab \n -> ntfs-3g \n 
			-> exfat-utils \n -> xarchiver \n -> gparted \n 
			-> wine \n -> exe-thumbnailer \n -> brave \n 
			-> github-desktop \n -> playonlinux \n -> discord \n
            -> visual-studio-code-bin \n -> zerotier-gui-git \n -> notion-app \n
            -> teamviewer \n -> numix-gtk-theme-git \n -> numix-icon-theme-app \n
            -> preload """ ,20,65) == d.OK:
        
        utils.clear()
        print("=============== SOFTWARE =============== \n")
        
        with open('/etc/X11/Xwrapper.config', 'w') as f: f.write("allowed_users=anybody")
        
        call(f"touch /home/{SUDOUSER}/software.sh")
        with open(f'/home/{SUDOUSER}/software.sh', 'w') as f: 
            f.writelines([
                "#!/bin/bash\n",
                "yay -S baobab ntfs-3g exfatprogs \\\n",
                "xarchiver gparted wine playonlinux xrdp \\\n",
                "notion-app teamviewer preload  \\\n",
                "brave-bin exe-thumbnailer github-desktop-bin \\\n",
                "wps-office xorgxrdp gobject-introspection libdbusmenu-gtk2 \\\n",
                "libdbusmenu-glib libdbusmenu-gtk3 appmenu-gtk-module numix-gtk-theme \\\n",
                "numix-icon-theme-git numix-circle-icon-theme-git \\\n",
                "systemctl enable xrdp \\\n",
                "systemctl enable xrdp-sesman \\\n",
                "systemctl enable preload \\\n"
            ])
        call(f"chown {SUDOUSER} /home/{SUDOUSER}/software.sh", shell=True)
        call(f"chmod +x /home/{SUDOUSER}/software.sh", shell=True)
        printer("print",33); print(" ")
        print("=============== OK =============== \n")
        input(reader(15))
    else: utils.clear(); return
        
def finisher() -> None:
    
    utils.clear(); d.msgbox(reader(27),7,50)
    call("rm -f /arch-setupper.py &> /dev/null", shell=True)
    utils.clear(); printer("print", 34); exit(0)
    
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
    
    def live_tasker(cmd: str) -> int:
        task = Popen(cmd, stdout=PIPE, stderr=PIPE, encoding='utf8', shell=True)
        try:  
            while task.poll() is None:
                for line in task.stdout:
                    task.stdout.flush()
                    print(line.replace("\n", ""))
            return task.poll()
        except: return 1
    
    def spinning():
        while True:
            for cursor in '|/-\\':
                yield cursor

if __name__ == "__main__":
    main()
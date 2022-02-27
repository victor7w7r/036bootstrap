from subprocess import call, PIPE, Popen
from sys import stdin, stdout, platform, version_info
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

LANGUAGE: int = 0; XRDPTOGGLE=0

def main() -> None: 
    utils.clear(); language(); cover(); verify(); packages(); hostnamer()
    localer(); cockpit(); graphical(); remote(); kvm(); ohmyzsh(); software(); finisher()

def printer(type: str, position: int, additional: str = "") -> None:
    
    GREEN = '\033[92m';  WARNING = '\033[93m'; FAIL = '\033[91m';  ENDC = '\033[0m';
  
    DICTIONARY_ENG=(
	    "Your Operating System is not GNU/Linux, exiting",
		"This scripts only works in UEFI/EFI systems, consider change your PC or check your BIOS",
		"This script is only intended to run on Oracle Linux",
		"This script is only intended to run on x86_64 PCs.",
		"DNF is not available in this system, this system isn't Oracle Linux?, please install Oracle Linux 8",
		"This PC doesn't have internet connection, please check",
		"Updating Oracle Linux Repositories... Please Wait",
		"dialog is not available in this system, installing",
		"All dependencies is ok!",
		"=============== CORE PACKAGES =============== \n",
		"=============== COCKPIT SERVICE (IP:9090) =============== \n",
		"=============== SSH: PERMIT ROOT LOGIN ===============  \n",
		"We create a script called omz.sh in your home directory and root, after reboot, use chmod +x at omz.sh",
		"Please reboot your server to make changes",
        "Your Python versión is less than 3.5, exiting",
        "You are not superuser, please run as root"
	)

    DICTIONARY_ESP=(
	    "Este sistema no es GNU/Linux, saliendo",
		"Este script sólo trabaja en UEFI/EFI, considera cambiar tu PC o verifica tu BIOS",
		"Este script sólo permite ejecutarse en Oracle Linux",
		"Este script sólo se ejecuta en procesadores de x86_64.",
		"DNF no está disponible, ¿este sistema no es Oracle Linux?, instala Oracle Linux 8",
		"No tienes conexión a internet, por favor revisa e inténtalo de nuevo",
		"Actualizando repositorios de Oracle Linux... Por favor, espere",
		"dialog no está disponible, instalando",
		"Todo ok!",
		"=============== PAQUETES BASE =============== \n",
		"=============== SERVICIO DE COCKPIT (IP:9090) =============== \n",
		"=============== SSH: PERMITIR LOGIN DE ROOT ===============  \n",
		"Hemos creado un script llamado omz.sh en tu carpeta de home y de superusuario, después de reiniciar, usa chmod +x omz.sh",
		"Por favor reiniciar tu servidor para hacer los cambios",
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
		"Press Enter to continue...",
		"Please write your hostname (ex: A036-oracle)",
		"America/Guayaquil is the timezone by default, if you want to change, here is the command timedatectl set-timezone REGION/CITY",
		"Choose your keyboard layout",
		"Graphical",
		"Install XFCE as Desktop Environment?",
		"This is a VMware Guest?",
		"Permit Root Login?",
		"Install Oracle Linux KVM Suite?",
		"More Sofware!!",
		"This script has a little pack of software, Do you like it?",
		"READY!!!, Your Server is succesfully configured, if you have errors, please report at 036bootstrap in GitHub"
	)

    DICTIONARY_ESP=(
        "Presione Enter para continuar...",
		"Por favor escriba su hostname (ex: A036-oracle)",
		"America/Guayaquil es el timezone por defecto, si quieres cambiarlo por algún otro, aquí está la orden timedatectl set-timezone REGION/CITY",
		"Elige tu distribución de teclado",
		"Entorno Gráfico",
		"¿Instalar XFCE como Entorno gráfico?",
		"¿Este sistema es un invitado de VMware?",
		"Quieres permitir el superusuario al SSH?",
		"¿Instalar el Suite de Oracle KVM?",
		"Más Sofware!!",
		"Este script tiene un pequeño pack de software, ¿Te gusta?",
		"LISTO!!!, Tu servidor ha sido configurado exitosamente, si tú tienes errores, repórtalo a 036bootstrap"
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
    
    ORACLE: str = Popen(r"""#!/bin/bash
                        cat /etc/os-release | head -n 1 | cut -d "=" -f2
                      """, shell=True, stdout=PIPE).stdout.read().decode('utf-8').replace("\n", "")

    if version_info < (3, 5):
        utils.clear(); printer("error",14); exit(1)
    if platform != "linux":
        utils.clear(); printer("error",0); exit(1)
    if getuid() != 0:
        utils.clear(); printer("error",15); exit(1)
    if not path.exists('/sys/firmware/efi'):
        utils.clear(); printer("error",1); exit(1)
    if not (search("\"Oracle.* ",ORACLE)):
        utils.clear(); printer("error",2); exit(1)
    if machine() != "x86_64":
         utils.clear(); printer("error",3); exit(1)
    if not commandverify("dnf"):
        utils.clear(); printer("error",4); exit(1)
    try: urlopen('http://google.com')
    except: utils.clear(); printer("error",5); exit(1)
    
    printer("print",6)      
    
    Popen(r"""#!/bin/bash
                dnf update --assumeyes &> /dev/null
            """, shell=True, stdout=PIPE)
    
    if not commandverify("dialog"):
        printer("print",7)
        Popen(r"""#!/bin/bash
                dnf install dialog --assumeyes &> /dev/null
                """, shell=True, stdout=PIPE)
        
    printer("print",8)     
    
    spinner = utils.spinning()
    for _ in range(15):
        stdout.write(next(spinner))
        stdout.flush(); sleep(0.1)  
        stdout.write('\b')

def packages() -> None:
    
    utils.clear(); printer("print",9)
    proc = Popen("dnf -y install wget zsh", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    for line in iter(proc.stdout.readline, b''):
        print(line.rstrip())
    proc.stdout.close()
    proc.wait()
    print("=============== OK =============== \n")
    input(reader(0))
    
def hostnamer() -> None:
    
    response = d.inputbox(reader(1), 8, 80)
    if(response[0] == "ok" ):
        Popen("hostnamectl set-hostname " + response[1], shell=True)
    elif(response[0] == "cancel" ): exit(0) 

def localer() -> None:
    
    choices = [("Spanish/Español","es"),("English","us")]
    d.msgbox(reader(2))
    Popen("timedatectl set-timezone America/Guayaquil", shell=True)
    response = d.menu(reader(0), 15, 50, 4, choices)
    if(response[0] == "ok" and response[1] == "Spanish/Español"):
        Popen("localectl set-keymap es", shell=True)
    elif(response[0] == "ok" and response[1] == "English"):
        Popen("localectl set-keymap us", shell=True)
    else: utils.clear(); exit(0)
    
def cockpit() -> None:
    utils.clear(); printer("print",10)
    
    print(Popen(r"""#!/bin/bash
                    systemctl enable --now cockpit.socket
                """, shell=True, stdout=PIPE).stdout.read().decode('utf-8').replace("\n", ""))
    print(" ")
    print("=============== OK =============== \n")
    input(reader(0))

def graphical() -> None:
    
    global XRDPTOGGLE
    
    LISTHOME: list = Popen("ls /home", shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
    
    if d.yesno(reader("5"),7,60) == d.OK:
        XRDPTOGGLE=1; utils.clear()
        print("=============== EPEL & XFCE =============== \n")
        
        proc = Popen(r"""
                        #!/bin/bash
                        dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm --assumeyes
                        dnf update --assumeyes 
                        dnf groupinstall "base-x" --assumeyes 
                        dnf groupinstall "xfce" --assumeyes 
                        dnf install xfce4-whiskermenu-plugin --assumeyes 
                    """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
            
        proc.stdout.close(); proc.wait() 
        Popen("touch .xinitrc", shell=True); Popen('echo "xfce4-session" > .xinitrc', shell=True)
        
        for HOME in LISTHOME:
            Popen("touch /home/"+HOME+"/.xinitrc", shell=True)
            Popen('echo "xfce4-session" > /home/'+HOME+'/.xinitrc', shell=True)
            Popen('chown '+HOME+' /home/'+HOME+'/.xinitrc', shell=True)
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(0))
    else:
        utils.clear()
        print("=============== EPEL =============== \n")
        proc = Popen(r"""
                       #!/bin/bash
                        dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm --assumeyes
                      """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
            
        proc.stdout.close(); proc.wait() 
        print(" ")
        print("=============== OK =============== \n")
        input(reader(0))

def drivers() -> None:
    utils.clear()
    if d.yesno(reader("6"),8,60) == d.OK :
        utils.clear()
        proc = Popen(r"""
                       #!/bin/bash
                       dnf install open-vm-tools open-vm-tools-desktop --assumeyes
                      """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
    
        proc.stdout.close(); proc.wait() 
    else: utils.clear(); return

def remote() -> None:
    
    global XRDPTOGGLE
    LISTHOME: list = Popen("ls /home", shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
    
    utils.clear()
    if d.yesno(reader("7"),8,60) == d.OK :
        utils.clear(); printer("print",11)
        Popen(r"""
                #!/bin/bash
                    sed -i 's/^#PermitRootLogin\s.*$/PermitRootLogin yes/' /etc/ssh/sshd_config &> /dev/null
		            systemctl enable sshd; systemctl restart sshd
                """, shell=True)
        print(" ")
        print("=============== OK =============== \n")
        input(reader(0))
    utils.clear()
    if XRDPTOGGLE == 1:
        print("=============== XRDP ===============  \n")
        proc = Popen(r"""
                       #!/bin/bash
                      dnf install xrdp --assumeyes
                      """, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
    
        proc.stdout.close(); proc.wait() 
        
        for HOME in LISTHOME:
            Popen("touch /home/"+HOME+"/.Xclients", shell=True)
            Popen('echo "xfce4-session" > /home/'+HOME+'/.Xclients', shell=True)
            Popen('chmod a+x /home/'+HOME+'/.Xclients', shell=True)
            Popen('chown '+HOME+' /home/'+HOME+'/.Xclients', shell=True)
        
        Popen(r"""
                #!/bin/bash
                   systemctl enable xrdp
                    systemctl enable xrdp-sesman
                    systemctl start xrdp
                    systemctl start xrdp-sesman
                    firewall-cmd --permanent --add-port=3389/tcp 
                    firewall-cmd --reload
                    chcon --type=bin_t /usr/sbin/xrdp
                    chcon --type=bin_t /usr/sbin/xrdp-sesman
                """, shell=True)
        print(" ")
        print("=============== OK =============== \n")
        input(reader(0))

def kvm() -> None:
    utils.clear()
    if d.yesno(reader("8"),8,60) == d.OK:
        utils.clear()
        print("=============== KVM ===============  \n" )
        proc = Popen(r'''
                       #!/bin/bash
                       dnf config-manager --enable ol8_appstream ol8_kvm_appstream ol8_developer_EPEL
                        dnf module install virt --assumeyes 
                        dnf install virt-install virt-viewer virt-manager edk2-ovmf virt-v2v cockpit-machines --assumeyes
                        virt-host-validate qemu
                        systemctl enable libvirtd
                        systemctl start libvirtd
                        dnf install dnf-plugins-core --assumeyes 
                        dnf config-manager --add-repo https://www.kraxel.org/repos/firmware.repo
                        dnf install edk2.git-ovmf-x64 --assumeyes 
                        echo "nvram = [" >> /etc/libvirt/qemu.conf
                        echo "	\"/usr/edk.git/OVMF_CODE.fd:/usr/edk.git/OVMF_VARS.fd\"" >> /etc/libvirt/qemu.conf
                        echo "]" >> /etc/libvirt/qemu.conf
                        systemctl restart libvirtd
                        systemctl enable serial-getty@ttyS0.service
                        systemctl start serial-getty@ttyS0.service
                      ''', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
    
        proc.stdout.close(); proc.wait() 
    else: utils.clear(); return
        
def ohmyzsh() -> None:
    utils.clear()
    LISTHOME: list = Popen("ls /home", shell=True, stdout=PIPE).stdout.read().decode('utf-8').rstrip().split('\n')
    print("=============== OMZ =============== \n" )
    for HOME in LISTHOME:
        Popen("echo '#!/bin/bash' > /home/"+HOME+"/omz.sh", shell=True)
        Popen(r'echo \'sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"\' >> /home/'+HOME+'/omz.sh', shell=True)
        Popen(r'echo \'sed -i -e "s/ZSH_THEME=.*/ZSH_THEME=\"pmcgee\"/" .zshrc\' >> /home/'+HOME+'/omz.sh', shell=True)
        Popen(r'echo \'sed -i -e "/^source $ZSH.*/i ZSH_DISABLE_COMPFIX=true" .zshrc\' >> /home/'+HOME+'/omz.sh', shell=True)
        Popen(r'echo \'git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting\' >> /home/'+HOME+'/omz.sh', shell=True)
        Popen(r'echo \'git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions\' >> /home/'+HOME+'/omz.sh', shell=True)
        Popen(r'echo \'sed -i -e "s/plugins=(.*/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/" .zshrc\' >> /home/'+HOME+'/omz.sh', shell=True)
        Popen('chown '+HOME+' /home/'+HOME+'/omz.sh', shell=True)
        Popen('chmod +x /home/'+HOME+'/omz.sh', shell=True)
        
    Popen("echo '#!/bin/bash' > /root/omz.sh", shell=True)
    Popen(r'echo \'sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"\' >> /root/omz.sh', shell=True)
    Popen(r'echo \'sed -i -e "s/ZSH_THEME=.*/ZSH_THEME=\"pmcgee\"/" .zshrc\' >> /root/omz.sh', shell=True)
    Popen(r'echo \'sed -i -e "/^source $ZSH.*/i ZSH_DISABLE_COMPFIX=true" .zshrc\' >> /root/omz.sh', shell=True)
    Popen(r'echo \'git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting\' >> /root/omz.sh', shell=True)
    Popen(r'echo \'git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions\' >> /root/omz.sh', shell=True)
    Popen(r'echo \'sed -i -e "s/plugins=(.*/plugins=(git zsh-syntax-highlighting zsh-autosuggestions)/" .zshrc\' >> /root/omz.sh', shell=True)
    Popen('chown '+HOME+' /root/omz.sh', shell=True)
    Popen('chmod +x /root/omz.sh', shell=True)
    
    printer("print",12)

    print(" ")
    print("=============== OK =============== \n")
    input(reader(0))
    
def software() -> None:
    utils.clear()
  
    if d.yesno(reader("10")+"""\n -> baobab \n -> ntfs-3g \n 
			-> gparted \n -> nautilus \n -> gedit \n 
			-> tar \n -> yum-utils \n -> numix-gtk-theme \n 
			-> numix-icon-theme \n -> numix-icon-theme-circle""" ,20,65) == d.OK:
        utils.clear()
        print("=============== SOFTWARE =============== \n")

        proc = Popen(r'''
                       #!/bin/bash
                        dnf install baobab ntfs-3g gparted exfatprogs nautilus gedit tar yum-utils --assumeyes
                        dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm --assumeyes
                        dnf install numix-gtk-theme --assumeyes
                        dnf install gnome-icon-theme --assumeyes
                        dnf install numix-icon-theme --assumeyes
                        dnf install numix-icon-theme-circle --assumeyes
                        dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm --assumeyes
                      ''', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        for line in iter(proc.stdout.readline, b''):
            print(line.rstrip())
    
        proc.stdout.close(); proc.wait() 
        
        print(" ")
        print("=============== OK =============== \n")
        input(reader(0))
        
    else: utils.clear(); return

def finisher() -> None:
    
    utils.clear(); d.msgbox(reader(11))
    utils.clear(); printer("print", 13); exit(0)
        
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
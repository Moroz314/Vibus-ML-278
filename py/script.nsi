!define APPNAME "Disk"
!define APPDIR "C:\Disk"

Outfile "DiskInstaller.exe"
InstallDir "${APPDIR}"

Section "Install"
    SetOutPath "$INSTDIR"
    File "E:\code_moroz\Vibeus-ML-278\Vibus-ML-278\py\disk.exe"

    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Disk" '"$INSTDIR\disk.exe"'
    
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

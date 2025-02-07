!define APPNAME "Disk"
!define APPDIR "C:\Disk"

Outfile "DiskInstaller.exe"
InstallDir "${APPDIR}"

Section "Install"
    SetOutPath "$INSTDIR"
    File "D:\disk.exe"

    # Добавляем программу в автозапуск
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Disk" '"$INSTDIR\disk.exe"'
    
    # Создаём uninstall.exe (файл удаления программы)
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\disk.exe"
    Delete "$INSTDIR\uninstall.exe"

    # Удаляем запись из автозапуска
    DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Disk"

    RMDir "$INSTDIR"
SectionEnd
!define APPNAME "Disk"
!define APPDIR "C:\Disk"

Outfile "DiskInstaller.exe"
InstallDir "${APPDIR}"

Section "Install"
    SetOutPath "$INSTDIR"
    File "D:\disk.exe"

    # ��������� ��������� � ����������
    WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Disk" '"$INSTDIR\disk.exe"'
    
    # ������ uninstall.exe (���� �������� ���������)
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\disk.exe"
    Delete "$INSTDIR\uninstall.exe"

    # ������� ������ �� �����������
    DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Disk"

    RMDir "$INSTDIR"
SectionEnd
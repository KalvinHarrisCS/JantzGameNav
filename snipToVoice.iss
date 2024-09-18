[Setup]
AppName=JantzGameNav
AppVersion=1.0
DefaultDirName={pf}\JantzGameNav
DefaultGroupName=JantzGameNav
OutputBaseFilename=JantzGameNavInstaller
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "tesseract-ocr-w64-setup-5.4.0.20240606.exe"; DestDir: "{tmp}"; Flags: ignoreversion

[Run]
; Install Tesseract OCR silently
Filename: "{tmp}\tesseract-ocr-w64-setup-5.4.0.20240606.exe"; Parameters: "/SILENT /DIR=""{app}\Tesseract-OCR"""; Flags: waituntilterminated
; Add Tesseract to the system PATH
Filename: "cmd"; Parameters: "/C setx /M PATH ""%PATH%;{app}\Tesseract-OCR"""; Flags: runhidden shellexec
; Launch your application after installation
Filename: "{app}\main.exe"; Description: "Launch JantzGameNav"; Flags: nowait postinstall skipifsilent

[Icons]
Name: "{group}\JantzGameNav"; Filename: "{app}\main.exe"
Name: "{group}\Uninstall JantzGameNav"; Filename: "{uninstallexe}"

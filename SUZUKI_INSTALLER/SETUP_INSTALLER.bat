@echo off
setlocal enabledelayedexpansion

echo ======================================================
echo    SUZUKI PLC MONITORING - OFFLINE INSTALLER
echo ======================================================
echo.

set "INSTALL_DIR=C:\Suzuki_PLC_Service"
set "BIN_DIR=%INSTALL_DIR%\bin"
set "DB_DIR=%INSTALL_DIR%\database"

echo [1/2] Membuat folder instalasi di %INSTALL_DIR%...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"
if not exist "%DB_DIR%" mkdir "%DB_DIR%"

echo [2/2] Menyalin file aplikasi dan database...
copy /Y "bin\Suzuki_PLC_Service.exe" "%BIN_DIR%\" >nul
copy /Y "database\plc_db_v2.sql" "%DB_DIR%\" >nul
copy /Y "database\plc_db.sql" "%DB_DIR%\" >nul

echo [3] Membuat Shortcut di Desktop dan Startup (Autorun)...
set "SCRIPT_PATH=%temp%\CreateShortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%SCRIPT_PATH%"

rem Shortcut Desktop
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Suzuki PLC Service.lnk" >> "%SCRIPT_PATH%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%SCRIPT_PATH%"
echo oLink.TargetPath = "%BIN_DIR%\Suzuki_PLC_Service.exe" >> "%SCRIPT_PATH%"
echo oLink.WorkingDirectory = "%BIN_DIR%" >> "%SCRIPT_PATH%"
echo oLink.Description = "Suzuki PLC Monitoring Service" >> "%SCRIPT_PATH%"
echo oLink.Save >> "%SCRIPT_PATH%"

rem Shortcut Startup (Autorun)
echo sStartupFile = oWS.SpecialFolders("Startup") ^& "\Suzuki PLC Service Autorun.lnk" >> "%SCRIPT_PATH%"
echo Set oLink2 = oWS.CreateShortcut(sStartupFile) >> "%SCRIPT_PATH%"
echo oLink2.TargetPath = "%BIN_DIR%\Suzuki_PLC_Service.exe" >> "%SCRIPT_PATH%"
echo oLink2.WorkingDirectory = "%BIN_DIR%" >> "%SCRIPT_PATH%"
echo oLink2.Description = "Suzuki PLC Monitoring Service Autorun" >> "%SCRIPT_PATH%"
echo oLink2.Save >> "%SCRIPT_PATH%"

cscript /nologo "%SCRIPT_PATH%"
del "%SCRIPT_PATH%"

echo.
echo ======================================================
echo   PENYALINAN DAN SET AUTORUN SELESAI!
echo ======================================================
echo.
echo Lokasi Instalasi: %INSTALL_DIR%
echo File Database   : %DB_DIR%\plc_db_v2.sql
echo.
echo CATATAN PENTING:
echo Silahkan lakukan IMPORT DATABASE secara manual melalui 
echo phpMyAdmin atau Command Line sebelum menjalankan program.
echo.
echo Anda sekarang bisa menjalankan program melalui Shortcut di Desktop.
echo.
pause

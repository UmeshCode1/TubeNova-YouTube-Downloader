@echo off
echo ================================================
echo TubeNova Wiki Setup
echo ================================================
echo.
echo GitHub Wiki is now enabled!
echo.
echo Step 1: Visit https://github.com/UmeshCode1/TubeNova-YouTube-Downloader/wiki
echo Step 2: Click "Create the first page" button
echo.
echo Step 3: Clone the wiki
echo   git clone https://github.com/UmeshCode1/TubeNova-YouTube-Downloader.wiki.git temp-wiki
echo.
echo Step 4: Copy wiki files
echo   xcopy wiki\*.md temp-wiki\ /Y
echo   cd temp-wiki
echo   git add .
echo   git commit -m "docs: add comprehensive wiki documentation"
echo   git push origin master
echo   cd ..
echo.
echo Step 5: Clean up
echo   rmdir /s /q temp-wiki
echo.
echo ================================================
echo Wiki files ready:
dir /b wiki\*.md
echo ================================================
pause

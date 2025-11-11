# Wiki Setup Script for TubeNova# Wiki Setup Script for TubeNova

# This script helps you populate the GitHub Wiki with documentation# This script helps you populate the GitHub Wiki with documentation



$separator = "=================================================="Write-Host "🎯 TubeNova Wiki Setup" -ForegroundColor Cyan

Write-Host "=" * 50

Write-Host "TubeNova Wiki Setup" -ForegroundColor Cyan

Write-Host $separator# Check if wiki folder exists

if (-not (Test-Path "wiki")) {

# Check if wiki folder exists    Write-Host "❌ Error: wiki folder not found!" -ForegroundColor Red

if (-not (Test-Path "wiki")) {    exit 1

    Write-Host "Error: wiki folder not found!" -ForegroundColor Red}

    exit 1

}Write-Host "✅ Wiki files found" -ForegroundColor Green



Write-Host "Wiki files found" -ForegroundColor Green# Instructions

Write-Host "`n📚 GitHub Wiki is now enabled!" -ForegroundColor Yellow

# InstructionsWrite-Host "`nTo populate the wiki, follow these steps:" -ForegroundColor White

Write-Host ""

Write-Host "GitHub Wiki is now enabled!" -ForegroundColor YellowWrite-Host "`n1️⃣  Visit your repository wiki:" -ForegroundColor Cyan

Write-Host ""Write-Host "   https://github.com/UmeshCode1/TubeNova-YouTube-Downloader/wiki" -ForegroundColor Blue

Write-Host "To populate the wiki, follow these steps:" -ForegroundColor White

Write-Host "`n2️⃣  Click 'Create the first page' button" -ForegroundColor Cyan

Write-Host ""

Write-Host "Step 1: Visit your repository wiki:" -ForegroundColor CyanWrite-Host "`n3️⃣  Once created, clone the wiki repo:" -ForegroundColor Cyan

Write-Host "  https://github.com/UmeshCode1/TubeNova-YouTube-Downloader/wiki" -ForegroundColor BlueWrite-Host "   git clone https://github.com/UmeshCode1/TubeNova-YouTube-Downloader.wiki.git temp-wiki" -ForegroundColor Gray



Write-Host ""Write-Host "`n4️⃣  Copy wiki files:" -ForegroundColor Cyan

Write-Host "Step 2: Click 'Create the first page' button" -ForegroundColor CyanWrite-Host "   Copy-Item wiki\*.md temp-wiki\" -ForegroundColor Gray

Write-Host "   cd temp-wiki" -ForegroundColor Gray

Write-Host ""Write-Host "   git add ." -ForegroundColor Gray

Write-Host "Step 3: Once created, clone the wiki repo:" -ForegroundColor CyanWrite-Host "   git commit -m 'docs: add comprehensive wiki documentation'" -ForegroundColor Gray

Write-Host "  git clone https://github.com/UmeshCode1/TubeNova-YouTube-Downloader.wiki.git temp-wiki" -ForegroundColor GrayWrite-Host "   git push origin master" -ForegroundColor Gray



Write-Host ""Write-Host "`n5️⃣  Clean up:" -ForegroundColor Cyan

Write-Host "Step 4: Copy wiki files:" -ForegroundColor CyanWrite-Host "   cd .." -ForegroundColor Gray

Write-Host "  Copy-Item wiki\*.md temp-wiki\" -ForegroundColor GrayWrite-Host "   Remove-Item -Recurse -Force temp-wiki" -ForegroundColor Gray

Write-Host "  cd temp-wiki" -ForegroundColor Gray

Write-Host "  git add ." -ForegroundColor GrayWrite-Host "`n✨ Or use the automated helper:" -ForegroundColor Yellow

Write-Host "  git commit -m 'docs: add comprehensive wiki documentation'" -ForegroundColor GrayWrite-Host "   .\setup-wiki-auto.ps1" -ForegroundColor Blue

Write-Host "  git push origin master" -ForegroundColor Gray

Write-Host "`n📖 Wiki pages ready to upload:" -ForegroundColor Magenta

Write-Host ""Get-ChildItem wiki\*.md | ForEach-Object {

Write-Host "Step 5: Clean up:" -ForegroundColor Cyan    Write-Host "   ✓ $($_.Name)" -ForegroundColor Green

Write-Host "  cd .." -ForegroundColor Gray}

Write-Host "  Remove-Item -Recurse -Force temp-wiki" -ForegroundColor Gray

Write-Host "`n🎉 Your wiki will be live at:" -ForegroundColor Yellow

Write-Host ""Write-Host "   https://github.com/UmeshCode1/TubeNova-YouTube-Downloader/wiki" -ForegroundColor Blue

Write-Host "Wiki pages ready to upload:" -ForegroundColor Magenta

Get-ChildItem wiki\*.md | ForEach-Object {Write-Host ""

    Write-Host "  $($_.Name)" -ForegroundColor Green$separator = "=" * 50

}Write-Host $separator


Write-Host ""
Write-Host "Your wiki will be live at:" -ForegroundColor Yellow
Write-Host "  https://github.com/UmeshCode1/TubeNova-YouTube-Downloader/wiki" -ForegroundColor Blue

Write-Host ""
Write-Host $separator
Write-Host "Wiki setup complete! Follow the steps above to populate." -ForegroundColor Green

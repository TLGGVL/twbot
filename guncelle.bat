@echo off
chcp 65001 >nul
echo GitHub guncellemesi baslatiliyor...

git add .
set /p mesaj="Commit (aciklama) mesaji girin: "
git commit -m "%mesaj%"
git push

echo.
echo Islem tamamlandi! Kapatmak icin bir tusa basin...
pause >nul
@echo off
:: Get MM/DD from system date via PowerShell (avoids locale issues with %date%)
for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format MM/dd"') do set TODAY=%%a
obsidian append path=Flightline.md "content=\n# %TODAY%\n- "
obsidian open path=Flightline.md

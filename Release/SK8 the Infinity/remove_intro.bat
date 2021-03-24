@echo off

for %%i in (*.mkv) do "C:/Program Files/MKVToolNix\mkvmerge.exe" --output "release/%%i" --split timestamps:12s --language 1:jpn --track-name 1:Japanese --default-track 1:yes --language 0:und --default-track 0:yes "%%i" --track-order 0:0,0:1

del "*001.mkv"

pause

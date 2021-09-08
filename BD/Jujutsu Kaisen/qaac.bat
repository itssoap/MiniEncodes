@echo off
for %%i in (*.mkv) do (ffmpeg -v quiet -stats -hide_banner -i "%%i" -map 0:a:0 -f wav - | qaac -o audio.m4a -V 127 -
ffmpeg -v quiet -stats -hide_banner -i "%%i" -i audio.m4a -map 0 -map -0:v -map -0:a:0 -map 1 -c copy "out%%i"
del audio.m4a)
pause
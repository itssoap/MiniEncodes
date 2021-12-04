@echo off
ffmpeg -v quiet -stats -hide_banner -i "%~1" -c copy -movflags +faststart "%~nx1.mkv"
del "%~1"
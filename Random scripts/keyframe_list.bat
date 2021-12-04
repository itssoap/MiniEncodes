@echo off
ffprobe -select_streams v -show_frames -show_entries frame=pict_type -of csv "%~1" | grep -n I | cut -d ":" -f 1 > "%~n1.txt"
pause
@echo off
ffprobe -select_streams v -show_frames -show_entries frame=pict_type -of csv "%~1" | findstr /N I
pause

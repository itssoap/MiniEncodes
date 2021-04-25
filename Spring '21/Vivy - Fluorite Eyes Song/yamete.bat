@Echo off

Set "n=%~nx1"
echo %n%
Set nom=%n:~44,-15%
echo %nom%
echo %~1

set "ff=subsVivy"

call set ffxx=%%ff%%%nom%%

echo %ffxx%

ffmpeg -i "%~nx1" -hide_banner -v quiet -stats -map 0 -map -0:v -c copy "Z:/Public/%ffxx%.mkv"
pause

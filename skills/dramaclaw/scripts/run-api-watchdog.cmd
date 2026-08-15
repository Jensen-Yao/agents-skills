@echo off
set "PATH=F:\DramaClaw\runtime\ffmpeg\ffmpeg-9.0.1-essentials_build\bin;%PATH%"
:loop
echo [%date% %time%] starting API >> "F:\DramaClaw\state\api-run.log"
"F:\DramaClaw\.venv\Scripts\novelvideo.exe" api --host 127.0.0.1 --port 8780 >> "F:\DramaClaw\state\api-run.log" 2>&1
echo [%date% %time%] API exited (code %ERRORLEVEL%), restarting in 3s >> "F:\DramaClaw\state\api-run.log"
timeout /t 3 /nobreak >nul
goto loop

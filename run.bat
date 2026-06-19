@echo off
cd /d "C:\Users\mbugu\OneDrive\Desktop\OpenCode\Trading Services website"
start /B /MIN "" "C:\Users\mbugu\AppData\Local\Programs\Python\Python312\python.exe" manage.py runserver 0.0.0.0:8000 --noreload
echo Server starting on http://127.0.0.1:8000
timeout /t 4 >nul
curl -s http://127.0.0.1:8000/ >nul 2>&1 && echo SUCCESS: ALGOEDGE is running! || echo FAILED: Server did not start

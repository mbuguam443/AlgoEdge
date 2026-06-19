@echo off
cd /d "C:\Users\mbugu\OneDrive\Desktop\OpenCode\Trading Services website"
start /B python manage.py runserver 0.0.0.0:8000 --noreload
echo AlgoEdge server starting on http://127.0.0.1:8000
timeout /t 3 >nul
curl -s http://127.0.0.1:8000/ | findstr "ALGOEDGE" >nul && echo Server is running!

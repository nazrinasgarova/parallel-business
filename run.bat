@echo off
title PARALLEL BUSINESS — AI Decision Simulator
color 0B
echo ===================================================================
echo             PARALLEL BUSINESS — QUANTUM DECISION ENGINE
echo          Alternativ Biznes Gələcəklərinin AI Simulyatoru
echo ===================================================================
echo.
echo  [1] Web Tətbiqi Birbaşa Brauzerdə Aç (index.html - Tövsiyə Olunur)
echo  [2] Streamlit İnteraktiv İdarəetmə Panelini Başlat (app.py)
echo  [3] Lokal HTTP Veb Serverini Başlat (port 8080)
echo.
set /p choice="Seciminizi daxil edin (1, 2 ve ya 3): "

if "%choice%"=="1" (
    echo Web sehifesi acilir...
    start index.html
    exit
)

if "%choice%"=="2" (
    echo Streamlit serveri ise salinir...
    streamlit run app.py
    pause
    exit
)

if "%choice%"=="3" (
    echo Lokal web server http://localhost:8080 unvaninda ise salinir...
    start http://localhost:8080/index.html
    python -m http.server 8080
    pause
    exit
)

echo Standart olaraq index.html acilir...
start index.html

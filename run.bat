@echo off
chcp 65001 >nul
echo ================================================
echo      影视剧论坛 - 正在启动...
echo ================================================
echo.
echo Python路径: C:\Python311Embed\python.exe
echo 项目路径: %~dp0
echo.
set PYTHONPATH=%~dp0
echo 正在启动服务器，请稍等...
echo 启动成功后请访问: http://localhost:5000
echo.
echo 测试账号:
echo   管理员: admin / 123456
echo   用户:  user1 / 123456
echo.
echo 按 Ctrl+C 可停止服务器
echo ================================================
start "" "http://localhost:5000"
C:\Python311Embed\python.exe "%~dp0app.py"
pause

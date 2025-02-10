@echo off
REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 运行 main.py
cd excelTranslate
python main.py

echo 程序执行完毕，按任意键退出...
pause

REM 取消激活虚拟环境
deactivate

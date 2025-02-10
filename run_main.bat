@echo off
REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 运行 main.py
python main.py

REM 暂停以查看输出（可选）
pause

REM 取消激活虚拟环境
deactivate

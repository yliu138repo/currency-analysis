:loop
call I:\currency-analyzer\.venv\Scripts\activate.bat && python I:\currency-analyzer\get-rate.py
timeout /t 300 /nobreak
goto :loop
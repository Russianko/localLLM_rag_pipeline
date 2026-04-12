@echo off
cd /d "C:\Users\ADMINSKY\Desktop\Личная LLM"

call conda activate base

start http://127.0.0.1:8001/docs

uvicorn api.main:app --port 8001 --reload

pause
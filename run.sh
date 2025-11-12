#!/usr/bin/env bash
# from project root
# start backend (ensure virtualenv activated)
cd backend || exit
uvicorn main:app --reload --host 127.0.0.1 --port 8000
# GitHub Profile Fetcher


Run the backend:


```bash
python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\activate on Windows
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
# edit backend/.env to add GITHUB_TOKEN if you have one
bash run.sh

Open frontend/index.html in the browser (or serve it with a tiny static server) and fetch profiles.
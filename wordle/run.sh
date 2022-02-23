if [ ! -d python-env ]; then
    echo creating virtual python
    python3 -m venv python-env
fi
source python-env/bin/activate
python3 src/main.py
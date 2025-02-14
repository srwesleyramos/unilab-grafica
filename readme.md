# gerar virtual environment
python -m venv <ambiente>

# ativar escopo do environment
<ambiente>\Scripts\activate

# gerar lista de pacotes
pip freeze > requirements.txt

# instalar pacotes
pip install -r requirements.txt
# Env setup
conda create -n flask_app
conda activate flask_app
conda install flask

# lauching server
FLASK_ENV=development flask run --host=0.0.0.0
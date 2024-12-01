from app import create_app
from app.extensions import db
from app.models import create_example_data
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=3000)
args = parser.parse_args()

port = args.port

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_example_data()
    
    # lokal
    # app.run(host='0.0.0.0', port=5000, debug=True)
    
    # web:
    app.run(host='0.0.0.0', port=3000, debug=True, ssl_context=('cert.pem', 'key.pem'))
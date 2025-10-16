from app import create_app
import os

app = create_app()

@app.route('/')
def index():
    return "Kogui API - up"

if __name__ == '__main__':
    use_ssl = os.environ.get('USE_SSL', '0') == '1'
    if use_ssl:
        # coloque cert.pem e key.pem na raiz do kogui-backend ou ajuste caminhos
        app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
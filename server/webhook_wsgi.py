import os

from webhook import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5002))
    app.run(debug=False, port=port, host='0.0.0.0')

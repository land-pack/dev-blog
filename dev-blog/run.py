import sys
from app import app

if __name__ == '__main__':
    app.run(debug=True, port=int(sys.argv[1] if len(sys.argv) > 1 else 9999))

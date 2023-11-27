import argparse
from subprocess import Popen

from flask_cors import CORS

from mosquitoknow import create_app, enable_logging
from waitress import serve

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=int, default=5001, dest="port")
    parser.add_argument("--dev", "-d", action="store_true", dest="dev", default=False)
    args = parser.parse_args()
    logger = enable_logging("test_log.log")
    logger.info("logs!@")
    if args.dev:
        Popen(["npm", "start"])
    app = create_app()
    CORS(app.app)
    serve(app, port=args.port)

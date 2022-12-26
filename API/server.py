from flask import Flask, request, jsonify
import logging
from fpc.fpcg_engine import FPCG_Engine

logger = logging.getLogger()
app = Flask(__name__)
port = 50001

@app.get('/')
def test():
    logger.debug("[GET]: /test: Testing endpoint working")
    return {"message" : f"Flask server starting at port {port}"}

if __name__ == '__main__':
    logger.debug(f"Flask server starting at port {port}")
    app.run(port=port, debug=True, host="0.0.0.0")
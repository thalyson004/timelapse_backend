from app import app
import requests
from flask import Response, jsonify, make_response
from app.components.picture import get_picture, get_config

@app.route('/shoot/<ip>')
def shoot(ip:str):
    r = requests.get(f"http://{ip}/capture")
    
    return Response(
        r,
        status=r.status_code,
        content_type=r.headers['content-type']
    )
    
@app.route('/status/<ip>')
def status(ip:str):
    r = get_config(ip)
    return r
    
@app.route('/attribute/<ip>/<atr>')
def attribute(ip:str, atr:str):
    r = get_config(ip)
    return jsonify( {
        atr: r.json[atr]     
    })

@app.route('/framesize/<ip>/<val>')
def set_framesize(ip:str, val:str):
    r = requests.get(f"http://{ip}/control?var=framesize&val={val}")
    
    return Response(
        r,
        status=r.status_code,
        content_type=r.headers['content-type']
    )
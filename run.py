from app import app
from config import *


app.run(
    host=ipv4, 
    port=port, 
    debug=True, 
    use_reloader=False
)
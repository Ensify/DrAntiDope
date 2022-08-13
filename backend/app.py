from flask import Flask, render_template, request
import json
from website import create_app
import os


app = create_app()























if __name__ =="__main__":
    
    app.run(
        host    = "0.0.0.0", 
        debug   = False, 
        port    = 5011,
        use_reloader=False)
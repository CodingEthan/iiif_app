from app.router import app
from flask import render_template


@app.route('/viewer')
def viewer():
    return render_template('viewer.html')

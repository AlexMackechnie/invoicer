from flask import Flask, request
from invoicer_api.model.template import Template
import sqlite3

conn = sqlite3.connect("../db/invoicer.db")
conn.cur


app = Flask(__name__)


@app.route("/template", methods = ['GET', 'POST'])
def create_template():
    request_data = request.get_json()
    template = Template(
        request_data["template_name"],
        request_data["name"],
        request_data["address"],
        request_data["payment_details"],
        request_data["send_to"],
        request_data["amount"],
        request_data["description"],
    )


    return str(template.__dict__)

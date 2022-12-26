from flask import Flask, request
from invoicer_api.model.template import Template
import sqlite3



app = Flask(__name__)


@app.route("/template", methods = ['POST'])
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

    conn = sqlite3.connect("../db/invoicer.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO template (template_name, name, address, payment_details, send_to, amount, description) VALUES (?, ?, ?, ?, ?, ?, ?)", (template.template_name, template.name, template.address, template.payment_details, template.send_to, template.amount, template.description))

    conn.commit()

    return str(template.__dict__)


@app.route("/template", methods = ['GET'])
def get_template():
    template_name = request.args.get("template_name")
    conn = sqlite3.connect("../db/invoicer.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM template WHERE template_name == '" + template_name + "';")
    resp = cur.fetchall()

    template = Template(*resp[0])

    return str(template.__dict__)


@app.route("/template", methods = ['POST'])
def create_invoice_from_template():
    request_data = request.get_json()
    return str(template.__dict__)

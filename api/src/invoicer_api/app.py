from flask import Flask, request
from invoicer_api.model.template import Template
from invoicer_api.model.invoice import Invoice
import sqlite3
from fpdf import FPDF


app = Flask(__name__)


@app.route("/template", methods = ['POST'])
def create_template():
    request_data = request.get_json()
    invoice = Invoice(
        request_data["name"],
        request_data["address"],
        request_data["payment_details"],
        request_data["send_to"],
        request_data["amount"],
        request_data["description"],
    )
    template = Template(
        request_data["template_name"],
        invoice
    )

    conn = sqlite3.connect("../db/invoicer.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO template (template_name, name, address, payment_details, send_to, amount, description) VALUES (?, ?, ?, ?, ?, ?, ?)", (template.template_name, template.invoice.name, template.invoice.address, template.invoice.payment_details, template.invoice.send_to, template.invoice.amount, template.invoice.description))

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


@app.route("/invoice", methods = ['POST'])
def create_invoice_from_template():
    request_data = request.get_json()
    template = Invoice(
        request_data["name"],
        request_data["address"],
        request_data["payment_details"],
        request_data["send_to"],
        request_data["amount"],
        request_data["description"],
    )  

    pdf = FPDF()
    pdf.add_page()
    pdf.set_margin(2)
    pdf.set_font('helvetica', size=12)
    pdf.write_html(
        f"""
        <h1> INVOICE</h1>
        <p><b>Name</b>: {template.name}</p>
        <p><b>Address</b>: {template.address}</p>
        <p><b>Payment Details</b>: {template.payment_details}</p>
        <table>
          <tr>
            <th width="75%">Description</th>
            <th width="25%">Amount</th>
          </tr>
          <tr>
            <td>{template.description}</td>
            <td>£{template.amount}</td>
          </tr>
        </table>
        """
    )
    #pdf.cell(txt="hello world")
    pdf.output("hello_world.pdf")

    return str(template.__dict__)


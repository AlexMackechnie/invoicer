from flask import Flask, request, url_for, render_template, redirect, session
from invoicer_api.model.template import Template
from invoicer_api.model.invoice import Invoice
import sqlite3
from fpdf import FPDF
from authlib.integrations.flask_client import OAuth
from functools import wraps
import os


app = Flask(__name__)
app.secret_key = os.environ["FLASK_APP_SECRET_KEY"]
oauth = OAuth(app)


oauth.register(
    name="github",
    client_id="5362969895ac3af06940",
    client_secret=os.environ["GITHUB_CLIENT_SECRET"],
    access_token_url="https://github.com/login/oauth/access_token",
    access_token_params=None,
    authorize_url="https://github.com/login/oauth/authorize",
    authorize_params=None,
    api_base_url="https://api.github.com",
    client_kwargs={"scope": "profile email"} # GitHub doesn't support OIDC as of yet.
)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('user_id', None)
        if user:
            return f(*args, **kwargs)
        return redirect("/login")
    return decorated_function


@app.route('/whoami')
@login_required
def whoami():
    return str(dict(session).get("user_id"))


@app.route('/login')
def login():
    github = oauth.create_client('github')
    redirect_uri = url_for('authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token() # This internally parses the "code" request arg.

    # Get user information.
    resp = github.get('user', token=token) # Usually we would be able to get userdata here, but GitHub doesn't support OIDC.
    profile = resp.json()
    user_id = profile["id"]
    name = profile["name"]

    # Create a session keyed by used_id
    session['user_id'] = user_id

    # Write/update data to user table, keyed by the ID.
    conn = sqlite3.connect("../db/invoicer.db")
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO user VALUES (?, ?);", (user_id, name))
    conn.commit()

    return redirect('/')


@app.route('/')
@login_required
def entry_point():
    return f"<h1>Hello {session['user_id']}!🤘</h1>"


@app.route("/template", methods = ['POST'])
def create_template():
    request_data = request.get_json()
    invoice = Invoice(
        request_data["name"],
        request_data["email"],
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

    cur.execute("INSERT INTO template (template_name, name, email, address, payment_details, send_to, amount, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (template.template_name, template.invoice.email, template.invoice.name, template.invoice.address, template.invoice.payment_details, template.invoice.send_to, template.invoice.amount, template.invoice.description))

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
        request_data["email"],
        request_data["address"],
        request_data["payment_details"],
        request_data["send_to"],
        request_data["amount"],
        request_data["description"],
    )

    pdf = FPDF()
    pdf.add_page()
    pdf.set_margin(10)
    pdf.set_font('helvetica', size=12)
    pdf.write_html(
        f"""
        <h1> INVOICE</h1>
        <p><b>To</b>: {template.send_to} <p>
        <br/><br/>
        <p><b>Name</b>: {template.name}</p>
        <p><b>Email</b>: {template.email}</p>
        <p><b>Address</b>: {template.address}</p>
        <p><b>Payment Details</b>: {template.payment_details}</p>
        <table style="margin-left:auto; margin-right:auto; text-align:center;" border="1">
          <tr>
            <th width="75%">Description</th>
            <th width="25%">Amount</th>
          </tr>
          <tr>
            <td>{template.description}</td>
            <td>£{template.amount}</td>
          </tr>
        </table>
        <font size="7"><p><strong>This template was generated using Invoicer: <a href="https://github.com/AlexMackechnie/invoicer">https://github.com/AlexMackechnie/invoicer</a></strong></p></font>
        """
    )

    pdf.output("hello_world.pdf")

    return "DONE"


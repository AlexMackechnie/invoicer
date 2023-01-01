from flask import Flask, request, url_for, render_template, redirect, session, send_from_directory, send_file
from invoicer_api.model.template import Template
from invoicer_api.model.invoice import Invoice
from invoicer_api import templates
import sqlite3
from fpdf import FPDF
from authlib.integrations.flask_client import OAuth
from functools import wraps
import os
import pkg_resources
from io import BytesIO
from invoicer_api.config import config


app = Flask(__name__, template_folder=templates.__path__[0])
app.config.from_mapping(config.config[os.environ["ENV"]])
app.secret_key = app.config["FLASK_APP_SECRET_KEY"]
oauth = OAuth(app)


oauth.register(
    name="gitlab",
    client_id=app.config["GITLAB_CLIENT_ID"],
    client_secret=app.config["GITLAB_CLIENT_ID"],
    access_token_url="https://gitlab.com/oauth/token",
    access_token_params=None,
    authorize_url="https://gitlab.com/oauth/authorize",
    authorize_params=None,
    userinfo_endpoint="https://gitlab.com/oauth/userinfo",
    server_metadata_url="https://gitlab.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid"}
)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('user_id', None)
        if user:
            return f(str(user), *args, **kwargs)
        return redirect("/login")
    return decorated_function


@app.route('/whoami')
@login_required
def whoami(user_id):
    return user_id


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/oidc-gitlab')
def oidc_gitlab():
    gitlab = oauth.create_client('gitlab')
    redirect_uri = url_for('authorize', _external=True)
    return gitlab.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    gitlab = oauth.create_client('gitlab')
    token = gitlab.authorize_access_token() # This internally parses the "code" request arg.

    sub = token["userinfo"]["sub"]
    name = gitlab.userinfo()["name"]

    # Create a session keyed by sub
    session['user_id'] = sub

    # Write/update data to user table, keyed by the ID.
    conn = sqlite3.connect(app.config["SQLITE_PATH"])
    cur = conn.cursor()
    cur.execute("INSERT OR REPLACE INTO user VALUES (?, ?);", (sub, name))
    conn.commit()

    return redirect('/')


@app.route('/')
@login_required
def entry_point(user_id):
    return render_template("root.html", user_id=user_id)


@app.route("/template", methods = ['POST'])
@login_required
def create_template(user_id):
    request_data = request.form
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
        user_id,
        invoice
    )

    conn = sqlite3.connect(app.config["SQLITE_PATH"])
    cur = conn.cursor()

    cur.execute("INSERT INTO template (template_name, user_id, name, email, address, payment_details, send_to, amount, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (template.template_name, template.user_id, template.invoice.name, template.invoice.email, template.invoice.address, template.invoice.payment_details, template.invoice.send_to, template.invoice.amount, template.invoice.description))

    conn.commit()

    return redirect('/templates') 


@app.route("/templates", methods = ['GET'])
@login_required
def get_templates(user_id):
    conn = sqlite3.connect(app.config["SQLITE_PATH"])
    cur = conn.cursor()
    query = f"SELECT template_name, user_id, name, email, address, payment_details, send_to, amount, description FROM template WHERE user_id = {user_id};"
    cur.execute(query)
    resp = cur.fetchall()

    templates = []
    for item in resp:
        templates.append(Template(item[0], item[1], Invoice(*item[2:])))

    return render_template("templates.html", templates=templates)


@app.route("/template", methods = ['GET'])
@login_required
def template(user_id):
    template_name = request.args.get("template_name")
    conn = sqlite3.connect(app.config["SQLITE_PATH"])
    cur = conn.cursor()
    query = f"SELECT template_name, user_id, name, email, address, payment_details, send_to, amount, description FROM template WHERE user_id = {user_id} AND template_name = '{template_name}';"
    cur.execute(query)
    resp = cur.fetchall()

    template = Template(resp[0][0], resp[0][1], Invoice(*resp[0][2:]))

    return render_template("template.html", template=template)


@app.route("/invoice", methods = ['POST'])
@login_required
def create_invoice(user_id):
    request_data = request.form
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

    buffer = BytesIO()

    pdf.output(buffer, "F")

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="invoice.pdf")


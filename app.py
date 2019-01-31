import sqlite3
from flask import Flask, request, render_template
import string
import io
import os
from werkzeug import secure_filename

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/donee/')
def renderDonee():
    return render_template("test_template.html")

# @app.route('/search/<organization_name>')
# def delete(organization_name):
#     conn = sqlite3.connect('donor.db')
#     c = conn.cursor()
#     c.execute("DELETE FROM donor WHERE org='{}'".format(organization_name)) # might create bug here
#     conn.commit()
#     conn.close()
#     return render_template("beforeDonated.html")

@app.route('/search/<organization_name>', methods=["POST"])
def delete(organization_name):
    donation_quantity = int(request.form["quantity"])
    print (donation_quantity)
    conn = sqlite3.connect('donor.db')
    c = conn.cursor()
    c.execute("SELECT quantity FROM donor WHERE org='{}'".format(organization_name))
    q = int(c.fetchone()[0])
    if q - donation_quantity <= 0: #need to get the donation quantity from form submitted
        c.execute("DELETE FROM donor WHERE org='{}'".format(organization_name)) # might create bug here
    else:
        c.execute("UPDATE donor SET quantity = '{}' WHERE org='{}'".format(q - donation_quantity,organization_name)) # might create bug here
    conn.commit()
    conn.close()
    return render_template("beforeDonated.html")

@app.route('/donated/')
def renderDonated():
    return render_template("beforeDonated.html")

@app.route('/donor/')
def renderDonor():
    return render_template("donor_template.html")

def form2db( org, obj, description, quantity, email, address):
    conn = sqlite3.connect('donor.db')
    c = conn.cursor()
    c.execute("INSERT INTO donor VALUES ( 52'{}', '{}', '{}', '{}', '{}', '{}')".format( org, email, address, obj, description, quantity))
    conn.commit()
    conn.close()

@app.route('/doneeform', methods=["POST"])
def read_form():
    email = request.form["email"]
    address = request.form["address"]
    org = request.form["org"]
    obj = request.form["object"]
    description = request.form["description"]
    quantity = request.form["quantity"]
    form2db( org, obj, description, quantity, email, address)
    return render_template("beforeSubmission.html")


@app.route('/search', methods=["GET"])
def search():
    ky = request.args["keywords"]
    conn = sqlite3.connect('donor.db')
    c = conn.cursor()
    c.execute("SELECT * FROM donor WHERE description LIKE '%{}%' OR object LIKE '%{}%'".format(ky, ky))
    search_results = c.fetchall()
    return render_template("beforeResult.html", search_results = search_results)


## google api new added 
@app.route('/search_img', methods=["POST"])
def search_img():
    # Instantiates a client
    print("getting vision client")
    client = vision.ImageAnnotatorClient()
    print("got vision client")
    file_in = request.files['files']
    file_name = os.path.join(
        os.path.dirname(__file__),
        secure_filename(file_in.filename))
    # Loads the image into memory
    #file_name = "/Users/tony/Desktop/donation/Unknown.jpg"
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print(labels[1].description)

    conn = sqlite3.connect('donor.db')
    c = conn.cursor()
    c.execute("SELECT * FROM donor WHERE description LIKE '%{}%' OR object LIKE '%{}%' OR description LIKE '%{}%' OR object LIKE '%{}%'".format(labels[0].description, labels[0].description, labels[1].description, labels[1].description))
    search_results = c.fetchall()
    ## ALSO select secondary descriptors
    # c.execute("SELECT * FROM donor WHERE description LIKE '%{}%' OR object LIKE '%{}%'".format(labels[1].description, labels[1].description))
    # r = c.fetchall()
    # if r != None:
    #     search_results.append(r)
    return render_template("beforeResult.html", search_results = search_results)

if __name__ == '__main__':
        app.run(debug = True)

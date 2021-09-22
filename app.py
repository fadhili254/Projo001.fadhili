import email

from flask import *

# method 2: click on view - tool windows - terminal
# once terminal type: pip install flask
# create the flask object
app = Flask(__name__)  # __name__ means main , you cant code before this code
# This key encrypts your user session for security reasons
app.secret_key = 'AGABD_@accv^^%%$125844444414789##***!!!AAAARANDOMpOlOHDQ$$&*z@S1'


# this is the body of your flask object
@app.route("/home")
def home():
    return render_template("home.html")


import pymysql

# establish db connection
connection = pymysql.connect(host='localhost', user='root', password='', database='shoes_tbl')


@app.route("/shoes")
def shoes():
    # create your query
    sql = "SELECT * FROM product_tbl"
    # execute/ run your
    # create a cursor used to execute sql
    cursor = connection.cursor()
    # Now use the cursor to execute your sql
    cursor.execute(sql)

    # check how many rows were returned
    if cursor.rowcount == 0:
        return render_template('shoes.html', msg='out of stock')
    else:
        rows = cursor.fetchall()
        return render_template('shoes.html', rows=rows)

    # this will display single shoes
    # thi route will need a product id


@app.route('/single/<product_id>')
def single(product_id):
    # create your query, provide a %s placeholder
    sql = "SELECT * FROM product_tbl WHERE product_id = %s"
    # execute/run your
    # create a cursor used to execute sql
    cursor = connection.cursor()
    # Now use the cursor to execute your sql
    # below you provide id to replace the %s
    cursor.execute(sql, (product_id))

    # check how many rows were returned
    if cursor.rowcount == 0:
        return render_template('single.html', msg='Product does not exist')
    else:
        row = cursor.fetchone()  # NB: product id was unique, so fetch one
        return render_template('single.html', row=row)


@app.route("/log-in", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # receive the posted email and password as variables
        email = request.form['customer_email']
        password = request.form['customer_password']
        # we now move to the database and confirm if above details exist
        sql = "SELECT * FROM customers_tbl where customer_email=%s and customer_password=%s"
        # create a cursor and execute above sql
        cursor = connection.cursor()
        # execute the sql
        cursor.execute(sql, (email, password))
        # check if a match was found
        if cursor.rowcount == 0:
            return render_template('log in.html', error="Wrong Credentials")
        elif cursor.rowcount == 1:
            # create a user to track who is logged in
            # attach user email to the session
            session['user'] = email
            return redirect('/shoes')
        else:
            return render_template('log in.html', error='Error Occurred, Try Latter')
    else:
        return render_template('log in.html')


@app.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        customer_firstname = request.form['customer_firstname']
        customer_surname = request.form['customer_surname']
        customer_lastname = request.form['customer_lastname']
        customer_email = request.form['customer_email']
        customer_phone = request.form['customer_phone']
        customer_password = request.form['customer_password']
        customer_password2 = request.form['customer_password2']
        customer_dob = request.form['customer_dob']
        gender = request.form['gender']
        customer_address = request.form['customer_address']

        # validation
        import re
        if customer_password != customer_password2:
            return render_template("sign up.html", password='password do not match')
        elif len(customer_password) < 8:
            return render_template("sign up.html", password='password to short')
        elif not re.search("[a-z]", customer_password):
            return render_template('sign up.html', password='Must have a small letter')
        elif not re.search("[A-Z]", customer_password):
            return render_template('sign up.html', password='Must have a capital letter')
        elif not re.search("[0-9]", customer_password):
            return render_template('sign up.html', password='Must have a small letter')
        else:
            sql = "insert into customers_tbl(customer_firstname, customer_surname, customer_lastname, customer_email, customer_phone, customer_password, gender,customer_address, customer_dob) VALUEs(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor = connection.cursor()
            try:
                cursor.execute(sql, (
                customer_firstname, customer_surname, customer_lastname, customer_email, customer_phone,
                customer_password, gender, customer_address, customer_dob))
                connection.commit()
                return render_template("sign up.html", success="SAVED")
            except:
                return render_template("sign up.html", error="FAILED")
    else:
        return render_template("sign up.html")

@app.route('/logout')
def logout():
    session.pop('user')  # clear session
    return redirect('/log-in')


@app.route('/reviews', methods = ['POST','GET'])
def reviews():
    if request.method =='POST':
        user = request.form['user']
        product_id = request.form['product_id']
        message = request.form['message']
        sql = "insert into reviews(user, product_id, message) values (%s, %s, %s)"
        cursor = connection.cursor()
        try:
            cursor.execute(sql, (user, product_id, message))
            connection.commit()
            # when going back to /single caarying the product id
            return redirect(url_for('single', product_id=product_id))
        except:
            flash('Review Not Posted')
            return redirect(url_for('single', product_id=product_id))
    else:
        return ''
# create a table named reviews
# review_id INT PK AI   50
# user VARCHAR 100
# product_id INT 50
# message VARCHAR 200
# review_date TIMESTAMP   - default CURRENT TIME STAMP

# git link: https://github.com/modcomlearning/FlaskProject
# create a github.com account

import requests
from flask import Flask, request, render_template
import datetime
import base64
from requests.auth import HTTPBasicAuth
@app.route('/mpesa_payment', methods = ['POST','GET'])
def mpesa_payment():
        if request.method == 'POST':
            phone = str(request.form['phone'])
            amount = str(request.form['amount'])

            # capture the session of paying client
            email = session['user']
            qtty = str(request.form['qtty'])
            product_id = str(request.form['product_'])

            # multiply qtty * amount
            total_pay = float(qtty) * float(amount)

            sql = 'insert into payment_info(phone, email, qtty, total_pay, pay_id) values(%s, %s, %s, %s, %s)'
            cursor = connection.cursor()
            cursor.execute(sql, (phone, email, qtty, total_pay, product_id))
            connection.commit()
            # GENERATING THE ACCESS TOKEN
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"

            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

            data = r.json()
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            business_short_code = "174379"
            data = business_short_code + passkey + timestamp
            encoded = base64.b64encode(data.encode())
            password = encoded.decode('utf-8')


            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password": "{}".format(password),
                "Timestamp": "{}".format(timestamp),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": 1,  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                "AccountReference": "account",
                "TransactionDesc": 'Qtty: '+qtty +'ID'+ product_id
            }

            # POPULAING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

            response = requests.post(url, json=payload, headers=headers)
            print (response.text)
            return render_template('payment.html', msg = 'Please Complete Payment in Your Phone')
        else:
            return render_template('payment.html')


@app.route('/contact_us', methods =['POST', 'GET'])
def contuct_us():
    if request.method =='POST':
        user = request.form['email']
        message = request.form['message']
        sql = "insert into contact_us(email, message) values (%s, %s)"
        cursor = connection.cursor()
        try:
            cursor.execute(sql, (user,  message))
            connection.commit()
            flash('message posted successfully')
            return redirect('/contact_us')
        except:
            flash('message not posted')
            return redirect('/contact_us')
    else:
        return render_template('contact_us.html')


@app.route('/admin', methods=['POST', 'GET'])
def admin():
    if request.method == 'POST':
        # receive the posted email and password as variables
        email = request.form['email']
        password = request.form['password']
        # we now move to the database and confirm if above details exist
        sql = "SELECT * FROM admin where email=%s and password=%s"
        # create a cursor and execute above sql
        cursor = connection.cursor()
        # execute the sql
        cursor.execute(sql, (email, password))
        # check if a match was found
        if cursor.rowcount == 0:
            return render_template('admin.html', error="Wrong Credentials")
        elif cursor.rowcount == 1:
            # create a user to track who is logged in
            # attach user email to the session
            session['admin'] = email
            return redirect('/dashboard')
        else:
            return render_template('admin.html', error='Error Occurred, Try Latter')
    else:
        return render_template('admin.html')



@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        sql = "select * from customers_tbl"
        cursor = connection.cursor()
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return render_template('dashboard.html', msg="No Customers")
        else:
            rows = cursor.fetchall()
            return render_template('dashboard.html', rows=rows)
    else:
        return redirect('/admin')

@app.route('/customer_del/<customer_id>')
def customer_del(customer_id):
    if 'admin' in session:
        sql = 'delete from customers where customer_id = %s'
        cursor = connection.cursor()
        cursor.execute(sql, (customer_id))
        connection.commit()
        flash(" Delete successful")
        return redirect('/dashboard')
    else:
        return redirect('/admin')

@app.route('/admin_logout')
def logout():
    session.pop('user')  # clear session
    return redirect('/admin')


# check
if __name__ == "__main__":
    app.run(debug=True)
# you cant code outside this code

import stripe
import json
import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/donate')
def donate():
  return render_template('donate.html')

@app.route('/karenpeople')
def karenpeople():
  return render_template('karenpeople.html')

@app.route('/mrmjc')
def mrmjc():
  return render_template('mrmjc.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/otherhelp')
def otherhelp():
  return render_template('otherhelp.html')

@app.route('/success')
def success():
  return render_template('success.html')

@app.route('/success2')
def success2():
  return render_template('success2.html')

@app.route('/cancel')
def cancel():
  return render_template('cancel.html')



# createing sessions
@app.route('/create-session1', methods=['POST'])
def create_session1():
  data = json.loads(request.data)
  session = stripe.checkout.Session.create(
    success_url='http://localhost:5000/success?id={CHECKOUT_SESSION_ID}',
    cancel_url='http://localhost:5000/donate',
    submit_type='donate',
    payment_method_types=['card'],
    line_items=[{
      'amount': data['amount1'],
      'name': 'Donation',
      'currency': 'USD',
      'quantity': 1,
      'images': ['https://iili.io/d9q8RR.png'],
    }],
  )
  return jsonify(session)

# createing sessions
@app.route('/create-session2', methods=['POST'])
def create_session2():
  data = json.loads(request.data)
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'price_data': {
        'unit_amount': data['amount2'],
        'currency': 'usd',
        'product': 'prod_HbtM7aYLL4P1LW',
        'recurring': {
          'interval': 'month',
        },
      },
      'quantity': 1,
    }],
    mode='subscription',
    success_url='http://localhost:5000/success2?id={CHECKOUT_SESSION_ID}',
    cancel_url='http://localhost:5000/donate',
  )
  return jsonify(session)




# retrieving sessions
@app.route('/retrieve-session')
def retrieve_session():
  session = stripe.checkout.Session.retrieve(
    request.args['id'],
    expand=['payment_intent'],
  )
  return jsonify(session)

# Start server
if __name__ == '__main__':
    app.run(port=5000)


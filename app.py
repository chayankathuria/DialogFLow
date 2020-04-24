from flask import Flask, request, make_response
import json
import os
from flask_cors import cross_origin
from emailer import EmailSender
from logger import logger
# from email_templates import template_reader

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello Bot'

# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    log = logger.Log()

    sessionID=req.get('responseId')


    result = req.get("queryResult")
    user_says=result.get("queryText")
    log.write_log(sessionID, "User Says: "+user_says)
    parameters = result.get("parameters")
    cust_email=parameters.get("email")
    cust_contact = parameters.get("phone-number")
    cust_name=parameters.get("any")
    intent = result.get("intent").get('displayName')
    if (intent=='ContactInfoIntent'):

        email_sender=EmailSender()
        #email_message='abcd'
        email_sender.send_email_to_student(cust_email)
        #email_sender.send_email_to_support(cust_name=cust_name,cust_contact=cust_contact,cust_email=cust_email)
        fulfillmentText="We have sent the order confirmation details to you via email."
        log.write_log(sessionID, "Bot Says: "+fulfillmentText)
        return {
            "fulfillmentText": fulfillmentText
        }
    else:
        log.write_log(sessionID, "Bot Says: " + result.fulfillmentText)

if __name__ == '__main__':
    app.run(debug=True)
    
#if __name__ == '__main__':
#    port = int(os.getenv('PORT', 5000))
#    print("Starting app on port %d" % port)
#    app.run(debug=False, port=port, host='0.0.0.0')

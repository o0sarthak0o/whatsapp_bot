from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Dictionary to store user expenses
user_expenses = {}

@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    response = MessagingResponse()
    msg = response.message()

    if incoming_msg.lower() == 'hi':
        msg.body('Hello! Send me your expenses in the format: amount description.')
    else:
        try:
            amount, description = incoming_msg.split(' ', 1)
            amount = float(amount)
            if from_number not in user_expenses:
                user_expenses[from_number] = []
            user_expenses[from_number].append({'amount': amount, 'description': description})
            msg.body(f'Logged: {amount} for {description}.')
        except ValueError:
            msg.body('Invalid format. Please send in the format: amount description.')

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)

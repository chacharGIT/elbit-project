#!/usr/bin/python
from flask import Flask, jsonify, render_template
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

app = Flask(__name__)


# Define the route for retrieving the Jewish holidays
@app.route('/holidays', methods=['GET'])
def get_holidays():
    # Fetch the Jewish holidays data from the API and process it
    current_date = datetime.today()
    three_months_ahead = datetime.today() + relativedelta(months=+3)
    start_date = current_date.strftime('%Y-%m-%d')
    end_date = three_months_ahead.strftime('%Y-%m-%d')

    # Define the API endpoint URL
    api_url = \
        'https://www.hebcal.com/hebcal/?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&start={}&end={}&ss=on&mf=on&c=on'.format(
            start_date, end_date)

    # Send GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:

        # Parse the JSON response
        holiday_data = response.json()
        holidays = []
        for item in holiday_data['items']:
            holiday = {'name': item['title'], 'date': item['date']}
            holidays.append(holiday)

        # Return the holiday html from the JSON response
        return render_template('holidays.html', holidays=holidays)
    else:

        # Handle the request failure
        return jsonify({'error': 'Request failed with status code: {response.status_code}'
                        })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
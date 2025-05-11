#!/usr/bin/env python3
from flask import Flask, request, render_template_string
from datetime import datetime, timedelta

app = Flask(__name__)

# Inline HTML template
HTML = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Ovulation Tracker</title>
  </head>
  <body>
    <h1>Ovulation Period Tracker</h1>
    <form method="post">
      <label for="last_period">First day of last period:</label>
      <input type="date" id="last_period" name="last_period" required><br><br>

      <label for="cycle_length">Average cycle length (days):</label>
      <input type="number" id="cycle_length" name="cycle_length" min="20" max="45" required><br><br>

      <button type="submit">Calculate</button>
      <button type="button" onclick="window.location.href='/'">Clear</button>
    </form>

    {% if ovulation %}
      <h2>Results</h2>
      <p>Estimated ovulation day: <strong>{{ ovulation }}</strong></p>
      <p>Estimated fertile window: <strong>{{ fertile_start }}</strong> to <strong>{{ fertile_end }}</strong></p>
    {% elif error %}
      <p style="color:red;">{{ error }}</p>
    {% endif %}
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    ovulation = fertile_start = fertile_end = None
    error = None
    if request.method == 'POST':
        lp = request.form.get('last_period', '')
        cl = request.form.get('cycle_length', '')
        try:
            last_period = datetime.strptime(lp, '%Y-%m-%d').date()
            cycle_length = int(cl)
            if cycle_length < 20 or cycle_length > 45:
                raise ValueError('Cycle length out of typical range')
            ovulation = last_period + timedelta(days=cycle_length - 14)
            fertile_start = ovulation - timedelta(days=5)
            fertile_end = ovulation + timedelta(days=1)
        except Exception:
            error = 'Invalid input: please check your date and cycle length.'
    return render_template_string(HTML, ovulation=ovulation, fertile_start=fertile_start, fertile_end=fertile_end, error=error)

if __name__ == '__main__':
    # Run on localhost:5000
    app.run(host='0.0.0.0', port=8080, debug=True)


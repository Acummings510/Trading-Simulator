from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            initial_capital = float(request.form['capital'])
            trading_days = int(request.form['days'])
            win_rate = float(request.form['win_rate']) / 100  # Convert percentage to a fraction
            risk_per_trade = 0.01  # Risking 1%
            reward_per_trade = 0.015  # Winning 1.5%
            daily_target = initial_capital * 0.015  # Target for the day

            capital = initial_capital
            results = []

            for day in range(trading_days):
                day_results = []
                daily_gain = 0

                for trade in range(3):  # Simulate 3 trades per day
                    if daily_gain >= daily_target:
                        break  # Stop trading if target is reached
                    
                    if random.random() < win_rate:  # Win
                        capital += capital * reward_per_trade
                        daily_gain += capital * reward_per_trade
                        result = f'<span style="color: green;">Win</span>'
                    else:  # Lose
                        capital -= capital * risk_per_trade
                        daily_gain -= capital * risk_per_trade
                        result = f'<span style="color: red;">Lose</span>'

                    day_results.append(f"Trade {trade + 1}: {result} - Capital = ${capital:,.2f}")

                results.append(f"<strong>Day {day + 1} Results:</strong><br>" + "<br>".join(day_results) + "<br>")

            final_capital_color = "green" if capital > initial_capital else "red"
            final_capital = f"<strong style='color: {final_capital_color};'>Final Capital after trading: ${capital:,.2f}</strong>"
            return render_template('index.html', results=results, final_capital=final_capital)

        except ValueError:
            error_message = "Please enter valid numbers for capital, trading days, and win rate."
            return render_template('index.html', error=error_message)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()

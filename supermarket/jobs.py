import schedule
import time
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from initiator import app
from database import Purchases
from flask import render_template



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'cperiyasamy085@gmail.com'
app.config['MAIL_PASSWORD'] = 'rbdk uxgz ccfx oupm'
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

app.app_context().push()

def send_daily_sales_report():
    try:
        # Get the total sales for the day
        # today = datetime.now().date()
        # print('today', today)
        today = "2024-12-02"
        try:
            sales = Purchases.query.filter(Purchases.purchase_date == today).all()
        except Exception as e:
            print(f'Error getting sales for today: {e}')
            

        # Create a dictionary to store the sales data
        sales_data = {}
        for sale in sales:
            item_name = sale.item_name
            if item_name not in sales_data:
                sales_data[item_name] = {'QTY': 0, 'Amount': 0}
            sales_data[item_name]['QTY'] += sale.quantity
            sales_data[item_name]['Amount'] += sale.quantity * sale.rate

        # Render the HTML template
        try:
            html = render_template('daily_sales_report.html', sales_data=sales_data)
        except Exception as e:
            print(f'Error rendering HTML template: {e}')

        # Send the sales report to the manager via email
        msg = Message("Daily Sales Report", sender="cperiyasamy085@gmail.com", recipients=["cperiyasamy085@gmail.com"])
        msg.html = html
        try:
            mail.send(msg)
            print('Daily sales report sent')
        except Exception as e:
            print(f'Error sending daily sales report: {e}')
    except Exception as e:
        print(f'Error sending daily sales report: {e}')

def send_weekly_sales_report():
    try:
        # Get the total sales for the week
        today = datetime.now().date() - timedelta(days=7)
        # today = "2024-12-02"
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        try:
            sales = Purchases.query.filter(Purchases.purchase_date >= start_of_week, Purchases.purchase_date <= end_of_week).all()
        except Exception as e:
            print(f'Error getting sales for today: {e}')

        # Create a dictionary to store the sales data
        sales_data = {}
        for sale in sales:
            item_name = sale.item_name
            if item_name not in sales_data:
                sales_data[item_name] = {'QTY': 0, 'Amount': 0}
            sales_data[item_name]['QTY'] += sale.quantity
            sales_data[item_name]['Amount'] += sale.quantity * sale.rate

        # Render the HTML template
        try:
            html = render_template('weekly_sales_report.html', sales_data=sales_data)
        except Exception as e:
            print(f'Error rendering HTML template: {e}')

        # Send the sales report to the manager via email
        msg = Message("Weekly Sales Report", sender="cperiyasamy085@gmail.com", recipients=["cperiyasamy085@gmail.com"])
        msg.html = html
        try:
            mail.send(msg)
            print('Weekly sales report sent')
        except Exception as e:
            print(f'Error sending weekly sales report: {e}')
    except Exception as e:
        print(f'Error sending weekly sales report: {e}')



# Schedule the tasks
schedule.every().day.at("15:24").do(send_daily_sales_report)  # 10 PM every day
schedule.every().monday.at("15:25").do(send_weekly_sales_report)  # 11 AM every Saturday

while True:
    schedule.run_pending()
    time.sleep(1)
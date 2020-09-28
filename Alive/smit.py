import sqlite3
import os.path
from nsetools import Nse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from jinja2 import Environment, BaseLoader



msg = MIMEMultipart()



path = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(path, 'db.sqlite3')



nse = Nse()


with sqlite3.connect(db) as conn:
    c = conn.cursor()
    for row in c.execute("SELECT * FROM smt_trails"):
        y = row[2]
        step1 = y.replace("[", "")
        step2 = step1.replace("]", "")


        for x in step2:
            if x == "'":
                step2 = step2.replace(x, "")


        final_elements = step2.split(', ')


        company = []
        last_prices = []
        open_prices = []
        day_highs = []
        average_prices = []
        low_52s = []
        high_52s = []



        for company_name in final_elements:
            all_stock_codes = nse.get_quote(company_name)
            company.append(all_stock_codes['companyName'])
            last_prices.append(all_stock_codes['lastPrice'])
            open_prices.append(all_stock_codes['open'])
            day_highs.append(all_stock_codes['dayHigh'])
            average_prices.append(all_stock_codes['averagePrice'])
            low_52s.append(all_stock_codes['low52'])
            high_52s.append(all_stock_codes['high52'])



        html_temp = """
        <html>
        <head></head>
        <body>
        <h1 style="text-align: center">Here is your stocks Information</h1>
        <table style="border: solid">
        <thead style="border: solid">
        <tr>
        <th>Name of compay</th>
        <th>last price</th>  
        </thead>
        <tbody style="border: solid">
        {% for price in last_price %}
          <tr>
           <td>com</td>
           <td> {{ price }} </td>
        {% endfor %}
        </body>
        </html>
        """

        # jinja2 rendering template for email
        template = Environment(loader=BaseLoader).from_string(html_temp)
        stock_info = zip(company, last_prices, open_prices, low_52s, high_52s, day_highs, average_prices)
        template_vars = {"stock_info": stock_info}
        html_out = template.render(template_vars)



        msg['from'] = "smitgol007@gmail.com"
        msg['to'] = row[1]
        msg["subject"] = "testing email"
        msg.attach(MIMEText(html_out, "html"))



        smt = smtplib.SMTP_SSL('smtp.gmail.com')
        smt.login("smitgol007@gmail.com", "smitsmit9825397527")
        smt.send_message(msg)
        smt.quit()
        print("Mail send!!")

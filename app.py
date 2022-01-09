from flask import Flask, render_template, request 
from datetime import date, timedelta 
import requests
from xml.etree import ElementTree
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '192.168.0.220'
app.config['MYSQL_USER'] = 'diploma_svc'
app.config['MYSQL_PASSWORD'] = 'password1'
app.config['MYSQL_DB'] = 'diploma'
mysql = MySQL(app)


@app.route('/',methods=['GET', 'POST'])
def index():
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        if request.form.get('Clear') == 'Clear':
            sql = "TRUNCATE TABLE metals"
            cursor.execute(sql)
            mysql.connection.commit()
            return render_template("index.html")
        elif request.form.get('Load') == 'Load':
            today = date.today()
            START_DATE = (today - timedelta(30)).strftime('%d/%m/%Y')
            END_DATE = today.strftime('%d/%m/%Y')
            api_url = f"https://www.cbr.ru/scripts/xml_metall.asp?date_req1={START_DATE}&date_req2={END_DATE}"
            sql = "INSERT INTO metals (code, date, buy, sell) VALUES (%s, %s, %s, %s)"
            response = requests.get(api_url)
            tree = ElementTree.fromstring(response.content)
            for child in tree:
                sql_date = child.attrib['Date']
                sql_code = child.attrib['Code']
                sql_buy = child[0].text
                sql_sell = child[1].text
                val = (sql_code, sql_date,sql_buy,sql_sell)
                cursor.execute(sql, val)
                mysql.connection.commit()
    sql = 'SELECT code,date,buy,sell FROM metals'
    cursor.execute(sql)
    data_from_sql = cursor.fetchall()
    return render_template("index.html", data=data_from_sql)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, request
import json
import requests
import zipfile
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders




app = Flask(__name__)

@app.route('/', methods= ['POST','GET'] )
def Home():
    if request.method == 'GET':
        return("""
     <html>
     <body>
     <form method='post'>
      <h1>Please Enter the data</h1>
      <input name='data' type='text'></input>
      <button type="submit">Enter</button>
     </form>
     </body>
     </html>
    """)
    if request.method == 'POST':
        data = request.form['data']
        archive = zipfile.ZipFile('Archive.zip', mode='w')
        file_list = []
        email = ''
        senders_email = 'youremailaddress'
        senders_password = 'password'
        req_data = json.loads(data)
        for item in req_data:
            if item == 'urls':
                for endpoint in req_data[item]:
                    url = endpoint
                    r = requests.get(endpoint)
                    file_list.append(endpoint.split('https://')[1])
                    print(r.text)
                    f = open(endpoint.split('https://')[1]+'.html', "w+")
                    f.write(r.text)
                    f.close
            if item == 'email':
                email = req_data['email']
        for item in file_list:
            try:
                archive.write(item+'.html')
            except Exception as e:
                print(str(e))
        archive.close()
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(senders_email,senders_password)
        msg = MIMEMultipart()
        msg['From']= senders_email
        msg['To']= email
        msg['Subject'] = "This is TEST"
        msg.attach(MIMEText('Zip files for your website\'s HTML are attached to this email. Thank You!' , 'plain'))
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(open("Archive.zip","rb").read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition',"attachment; filename= Archive.zip ")
        msg.attach(attachment)
        print(email)
        try:
          s.send_message(msg)
          return "<h1>Message sent Successfullly</h1>"
        except Exception as e:
          return "<h1>Message not sent : </h1> "+str(e)
        del msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 8002 , debug = "True")

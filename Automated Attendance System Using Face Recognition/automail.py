def send_mail():
    import os
    import yagmail
    import time
    import datetime
    try:
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        receiver = "atifyaqoob5242@gmail.com","manussicgupta@gmail.com"  # receiver email address
        body = "Attendence File"  # email body
        filename = os.getcwd()+os.sep+"Attendance"+os.sep+"Attendance_"+date+"_.csv"
        # mail information
        #yag = yagmail.SMTP("atifyaqoob6118@gmail.com", "tfvinkiehgawsqal")
        yag = yagmail.SMTP("itsmanuguptaofficial@gmail.com", "hotkgsblfwpusgbf")

        # sent the mail
        with open(filename,'r') as f:
            yag.send(
                to=receiver,
                subject="Attendance Report",  # email subject
                contents=body,  # email body
                attachments = f # file attached
            )
        print("Mail Successfully Send")
    except Exception as e:
        # print(e)
        print("Mail has not been send")

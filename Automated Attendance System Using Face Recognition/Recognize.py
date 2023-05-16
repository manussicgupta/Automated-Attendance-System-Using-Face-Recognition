import datetime
import os
import time

import cv2
import pandas as pd


#-------------------------
def Attendance(attendance):
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        fileName = "Attendance"+os.sep+"Attendance_"+date+"_"+".csv"
        if not os.path.isfile(fileName):
            attendance.to_csv(fileName, index=False)
        else:

            df= pd.read_csv(fileName,sep= ",")
            attendance= pd.concat([df,attendance]).drop_duplicates(subset= "Id",keep = "last")
            attendance.to_csv(fileName, index=False)
        print("Attendance Successful")

def recognize_attendence():
    try:
        start_time= time.time()
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
        recognizer.read("TrainingImageLabel" + os.sep+ "Trainner.yml")
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)
        df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv")
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Id', 'Name', 'Date', 'Time']
        attendance = pd.DataFrame(columns=col_names)

        # Initialize and start realtime video capture
        cam = cv2.VideoCapture(0)
        flag = "Not_Pass"
        while True:
            end_time = time.time()
            if (end_time - start_time) >30:
                break
            _, im = cam.read()
            # im = cv2.resize(im,(640,480))
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray,1.2, 5,minSize = (30, 30))
            for(x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x+w, y+h), (255, 255,0), 2)
                Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

                if conf < 100:

                    aa = df.loc[df['Id'] == Id]['Name'].values
                    confstr = "  {0}%".format(round(100 - conf))
                    tt = str(Id)+"-"+aa


                else:
                    Id = '  Unknown  '
                    tt = str(Id)
                    confstr = "  {0}%".format(round(100 - conf))

                if (100-conf) >=67:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = str(aa)[2:-2]
                    attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]

                    tt = str(tt)[2:-2] +" "+ "Pass"
                    cv2.putText(im, str(tt), (x+5,y-5), font, 1, (0, 255, 0), 2)
                    flag = "Pass"
                    Attendance(attendance)
                    break
                else:
                    cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

                if (100-conf) >= 67:
                    cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
                else:
                    cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)

            cv2.imshow('Attendance', im)
            
            if (cv2.waitKey(1) == ord('q')) or flag == "Pass":
                break
        
        if flag == "Not_Pass":
            print("Attendance not stored")
        flag = "Not_Pass"
        cam.release()
        cv2.destroyAllWindows()

    except:
        print("Something went wrong...")

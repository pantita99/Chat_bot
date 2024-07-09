import os
from flask import Flask, request, abort, jsonify
import mysql.connector
import messagemodel
import helper
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime
from pythainlp.util import thai_strftime
import random
from pythainlp.corpus import thai_stopwords
from pythainlp.tokenize import word_tokenize

folderpath = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
@app.route('/diw', methods=['POST', 'GET'])
def Factories():
    state_tag_userid_path = ""
    if request.method == "POST":
        data_load = request.json
        print(data_load)
        messagetype = data_load["MessageType"]
        state_tag_userid_path = data_load['ConnectID'] +"_state_tag.json"
        userID = data_load['ConnectID']
        #ask = selectaskuser(userID)
        if messagetype == "Text":
            try:
                message = data_load["Msg"]
                #ask = selectaskuser(userID)
                if (message in messagemodel.greating):
                    #text_message = helper.sendtext(userID,folderpath, messagetype,messagemodel.greating_out)
                    text_message = messagemodel.greating_out
                    return text_message
                elif (message in messagemodel.Text_gas):
                    #text_message = helper.sendtext(userID, folderpath, messagetype, "คุณกำลังติดต่อเรื่องก๊าซ")
                    text_message = "คุณกำลังติดต่อเรื่องก๊าซ"
                    return text_message
                else:
                    #return "เรื่องที่คุณสอบถามกำลังนำเข้าระบบเพื่อประมวลผล ติดต่อกลับภายหลังนะคะ"
                    results = predict_first_model(message)
                    if(results == "AskDate"):
                        print(results)
                        current_datetime = datetime.datetime.now()
                        Time = thai_strftime(current_datetime, "%A %d %B %Y ")
                        print(Time)
                        text_message = random.choice(messagemodel.time_output)%Time
                        return text_message
                    elif(results == "Greet"):
                        text_message = messagemodel.greating_out
                        return text_message
                    elif(results == "Ainame"):
                        text_message = "ผมคือผู้ช่วยของกรมโรงงานค่ะ"
                        return text_message
                    elif(results == "Gas"):
                        results = predict_seconds_model(message)
                        if(results == "Gas_Login_Type"):
                            text_message = "การล็อกอินเข้าใช้งานระบบก๊าซของผู้ประกอบการโรงงานในปัจจุบันมี 2 แบบ ล็อกอินด้วยเลขทะเบียนโรงงาน 14 หลัก และ ล็อกอินผ่านระบบ I-INDUSTRY ด้วยเลขบัตรประชาชน 13 หลัก"
                            return text_message
                        elif(results == "Gas_Use"):
                            text_message = "https://diw-platform.diw.go.th/Account/Login เลือกหัวข้อ การขึ้นทะเบียน/ต่ออายุ บุคลากรด้านก๊าซอุตสาหกรรมประจำโรงงาน"
                            return text_message
                        elif(results == "Individual_account"):
                            text_message = "การลงทะเบียนบัญชีบุคคลธรรมดา (DGA) เพื่อเข้าใช้ระบบก๊าซ ได้ตามลิงก์ https://connect.egov.go.th/Account/Register "
                            return text_message
                        elif(results == "Mean_agency"):
                            text_message = "ระบบพิสูจน์และยืนยันตัวตนทางดิจิทัล (DGA Digital ID) นอกจากจะทำหน้าที่ในการตรวจสอบการเข้าใช้งานระบบต่างๆแล้ว ยังมีเทคโนโลยีที่เรียกว่า OpenID ที่จะทำให้ผู้ใช้งานสามารถเข้าใช้งานระบบต่างๆ ได้โดยที่ไม่ต้องล็อกอินซ้ำ (Single Sign-On) อีกด้วย ซึ่งถูกพัฒนาโดย สำนักงานพัฒนารัฐบาลดิจิทัล (องค์การมหาชน) สพร. หรือ DGA เป็นหน่วยงานกลางของระบบรัฐบาลดิจิทัล ทำหน้าที่ให้บริการส่งเสริมและสนับสนุนการดำเนินการของหน่วยงานของรัฐและหน่วยงานอื่นเกี่ยวกับการพัฒนารัฐบาลดิจิทัล"
                            return text_message
                        elif(results == "gather_gas_data"):
                            text_message = "กรมโรงงานฯ ต้องการรวบรวมข้อมูลก๊าซของโรงงานจึงขอให้ ผปก. บันทึกข้อมูลก๊าซที่โรงงานใช้อยู่ ณ ปัจจุบัน ที่หัวข้อ ข้อมูลก๊าซอุตสาหกรรมโรงงาน และคลิกที่ Link บันทึกข้อมูลก๊าซอุตสาหกรรมโรงงาน"
                            return text_message
                        elif(results == "Usage_gas"):
                            text_message = "ผปก. login เข้ามาในระบบแล้วให้คลิกที่ เลขที่คำขอ ก็จะเข้าดูข้อมูลคนงานควบคุมก๊าซของโรงงานได้และสามารถดาวน์โหลดใบอนุญาตได้ที่ ตรวจสอบทะเบียน จะเป็น PDF 1 ฉบับ .บัญชีบุคคลธรรมดา (DGA) ถ้าลงทะเบียนแล้วจะได้ User + Password เพื่อเข้าสู่บริการ เมื่อ login เข้าไปจะเจอเลขบัตรประชาชน ชื่อ-นามสกุล และที่อยู่ตามบัตรประชาชน สามารถคลิกที่ปุ่ม ยื่นคำขอ เพื่อ ดำเนินการขึ้นทะเบียน/ต่ออายุคนงานควบคุมก๊าซได้เลย"
                            return text_message
                        elif(results == "gas_problemDGA_tel"):
                            text_message = "เบอร์โทร 02 612 6060  Email : contact@dga.or.th"
                            return text_message
                        elif(results == "gas_problemIND_tel"):
                            text_message = "Call Center : 02-430-6976 Email : service_ids@industry.go.th"
                            return text_message
            except Exception as ex:
                print(ex)
                return "เรื่องที่คุณสอบถามกำลังนำเข้าระบบเพื่อประมวลผล ติดต่อกลับภายหลังนะคะ"

def predict_first_model(message):
    with open('vectorizer1.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('model1', 'rb') as f:
        model = pickle.load(f)
    new_texts = [message]
    X_text = vectorizer.transform(new_texts)
    predictions = model.predict(X_text)
    for text, prediction in zip(new_texts, predictions):
        print(f"Text: {text} - Predicted tag: {prediction}")
    return prediction

def predict_seconds_model(message):
    with open('vectorizer_naive_bayes.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('naive_bayes_model.pkl', 'rb') as f:
        model = pickle.load(f)
    new_texts = [message]
    X_text = vectorizer.transform(new_texts)
    predictions = model.predict(X_text)
    for text, prediction in zip(new_texts, predictions):
        print(f"Text: {text} - Predicted tag: {prediction}")
    return prediction

if __name__ == '__main__':
    #app.run(port=200, host="0.0.0.0", debug=True)   
    app.run(port=300, debug=False, host="0.0.0.0")
   


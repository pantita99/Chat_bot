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
from pythainlp.util import normalize 

folderpath = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)\



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
                #ปรับข้อความให้อยู่ในรูปแบบมาตราฐาน ลบเครื่องหมายวรรคตอน
                message = data_load["Msg"]
                message = normalize(message) 
                message = message.replace(" ", "") 
                stopwords = list(thai_stopwords()) 
                message_tokens = message.split()

                #ask = selectaskuser(userID)
                if (message in messagemodel.greating):
                    text_message = messagemodel.greating_out
                    return text_message
                elif (message in messagemodel.Text_gas):
                    if(message =="การเข้าใช้งานระบบก๊าซออนไลน์ของกรมโรงงานอุตสาหกรรมสามารถเข้าไปใช้ระบบที่ช่องทางไหน(ลิงก์ระบบ)"):
                        text_message = "https://diw-platform.diw.go.th/Account/Login เลือกหัวข้อ การขึ้นทะเบียน/ต่ออายุ บุคลากรด้านก๊าซอุตสาหกรรมประจำโรงงาน"
                        return text_message
                    elif(message == "การลงทะเบียนบัญชีบุคคลธรรมดา(DGA)เพื่อเข้าใช้ระบบก๊าซ"):
                        text_message = "การลงทะเบียนบัญชีบุคคลธรรมดา (DGA) เพื่อเข้าใช้ระบบก๊าซ ได้ตามลิงก์ https://connect.egov.go.th/Account/Register  "
                        return text_message
                    elif(message == "ระบบบัญชีบุคคลธรรมดา(DGA)คืออะไรและเป็นของหน่วยงานใด"):
                        text_message = "ระบบพิสูจน์และยืนยันตัวตนทางดิจิทัล (DGA Digital ID) นอกจากจะทำหน้าที่ในการตรวจสอบการเข้าใช้งานระบบต่างๆแล้ว ยังมีเทคโนโลยีที่เรียกว่า 'OpenID' ที่จะทำให้ผู้ใช้งานสามารถเข้าใช้งานระบบต่างๆ ได้โดยที่ไม่ต้องล็อกอินซ้ำ (Single Sign-On) อีกด้วย ซึ่งถูกพัฒนาโดย สำนักงานพัฒนารัฐบาลดิจิทัล (องค์การมหาชน) สพร. หรือ DGA เป็นหน่วยงานกลางของระบบรัฐบาลดิจิทัล ทำหน้าที่ให้บริการส่งเสริมและสนับสนุนการดำเนินการของหน่วยงานของรัฐและหน่วยงานอื่นเกี่ยวกับการพัฒนารัฐบาลดิจิทัล"
                        return text_message
                    elif(message == "การloginของผปก.เข้าใช้ระบบก๊าซมีกี่แบบ"):
                        text_message = "การล็อกอินเข้าใช้งานระบบก๊าซของผู้ประกอบการโรงงานในปัจจุบันมี 2 แบบ ล็อกอินด้วยเลขทะเบียนโรงงาน 14 หลัก และ ล็อกอินผ่านระบบ I-INDUSTRY ด้วยเลขบัตรประชาชน 13 หลัก"
                        return text_message
                    elif(message == "ทำไมถึงกรมโรงงานฯถึงต้องรวบรวมข้อมูลก๊าซชองโรงงาน"):
                        text_message = "กรมโรงงานฯ ต้องการรวบรวมข้อมูลก๊าซของโรงงานจึงขอให้ ผปก. บันทึกข้อมูลก๊าซที่โรงงานใช้อยู่ ณ ปัจจุบัน ที่หัวข้อ ข้อมูลก๊าซอุตสาหกรรมโรงงาน และคลิกที่ Link บันทึกข้อมูลก๊าซอุตสาหกรรมโรงงาน"
                        return text_message
                    elif(message == "การใช้งานของระบบก๊าซของผู้ประกอบการ"):
                        text_message = "ผปก. login เข้ามาในระบบแล้วให้คลิกที่ เลขที่คำขอ ก็จะเข้าดูข้อมูลคนงานควบคุมก๊าซของโรงงานได้และสามารถดาวน์โหลดใบอนุญาตได้ที่ ตรวจสอบทะเบียน จะเป็น PDF 1 ฉบับ .บัญชีบุคคลธรรมดา (DGA) ถ้าลงทะเบียนแล้วจะได้ User + Password เพื่อเข้าสู่บริการ เมื่อ login เข้าไปจะเจอเลขบัตรประชาชน ชื่อ-นามสกุล และที่อยู่ตามบัตรประชาชน สามารถคลิกที่ปุ่ม ยื่นคำขอ เพื่อ ดำเนินการขึ้นทะเบียน/ต่ออายุคนงานควบคุมก๊าซได้เลย"
                        return text_message 
                    elif(message == "การลงทะเบียนDGAถ้ามีปัญหาในการสมัครเข้าใช้งานต้องติดต่อเบอร์โทรศัพท์เบอร์ไหน"):
                        text_message = "เบอร์โทร 02 612 6060  Email : contact@dga.or.th"
                        return text_message
                    elif(message == "ถ้ามีปัญหาในการเข้าใช้งานผู้ประกอบการโรงงานอุตสาหกรรมและผู้ประกอบการโรงงานอุตสาหกรรม(I-industry)ต้องติดต่อหน่วยงานใดและเบอร์โทรศัพท์เบอร์ไหน"):
                        text_message = "Call Center : 02-430-6976 Email : service_ids@industry.go.th"
                        return text_message
                   
                    return text_message
                
                elif (message in messagemodel.Text_law):
                    if(message == "จุดเริ่มต้นของการเข้าสู่กระบวนการรับทราบข้อกล่าวหาผ่านระบบอิเล็กทรอนิกส์เริ่มต้นกระบวนการที่จุดใด"):
                       text_message = "เมื่อผู้ประกอบกิจการโรงงานได้รับหนังสือแจ้งการกระทำความผิด และประสงค์ที่จะรับทราบข้อกล่าวหาผ่านระบบอิเล็กทรอนิกส์ โดยนำรหัสที่ได้รับจากหนังสือแจ้งการกระทำความผิด กรอกในระบบการรับทราบข้อกล่าวหาผ่านระบบอิเล็กทรอนิกส์"
                       return text_message
                    elif(message == "หากประสงค์จะเข้าสู่กระบวนการรับทราบข้อกล่าวหาผ่านระบบอิเล็กทรอนิกส์ผู้ประกอบกิจการโรงงานจำเป็นต้องมีบัญชีหรือลงทะเบียนผ่านระบบหรือหน่วยงานใด"):
                        text_message = "ผู้ประกอบกิจการโรงงานจำเป็นต้องมีบัญชี ดังนี้ 1. บัญชีผู้ใช้บุคคลธรรมดา (Digital ID) 2. บัญชีผู้ใช้นิติบุคคลของกรมพัฒนาธุรกิจการค้า (Digital ID DBD)  "
                        return text_message 
                    elif(message == "เมื่อผู้ประกอบกิจการโรงงานจะเข้าสู่กระบวนการรับทราบข้อกล่าวหาผ่านระบบอิเล็กทรอนิกส์แล้วจะต้องมีการยืนยันตัวตนหรือจะตรวจสอบอย่างไรว่าเป็นผู้ประกอบกิจการโรงงานที่ถูกดำเนินคดีรายนั้นๆ"):
                        text_message = "ภายหลังจากที่ผู้ประกอบกิจการเข้าสู่ระบบ (การรับทราบข้อกล่าวหาผ่านระบบอิเล็กทรอนิกส์)ผู้ประกอบกิจการจะต้องยืนยันตัวตนด้วยรหัส OTP ผ่านทางอีเมล"
                        return text_message
                    elif(message == "หากผู้ประกอบการโรงงานรับทราบข้อกล่าวหาผ่านระบบอิเล็กทรอนิกส์แล้วต่อมาประสงค์จะดำเนินกระบวนการในขั้นตอนต่อไปเป็นแบบปกติได้หรือไม่"):
                        text_message = "สามารถกระทำได้"
                        return text_message
                    elif(message == "หากครบกำหนดระยะเวลามารับทราบข้อกล่าวหาผ่านระบบอิเล็กทรอนิกส์แล้วจะขอขยายระเวลาอีกได้หรือไม่"):
                        text_message = "เมื่อครบระยะเวลาการรับทราบข้อกล่าวหาแล้ว ไม่สามารถขยายระยะเวลาได้อีก"
                        return text_message
                    elif(message == "ภายหลังจากรับทราบข้อกล่าวหาผ่านระบบอิเล็กทรอนิกส์แล้วจะสามารถชำระเงินค่าปรับได้เมื่อใด"):
                        text_message = "เมื่อรับทราบข้อกล่าวหาแล้ว พนักงานเจ้าหน้าที่จะส่งสำนวนเข้าคณะกรรมการเปรียบเทียบคดี ภายหลังจากคณะกรรมการเปรียบเทียบคดีกำหนดจำนวนเงินค่าปรับแล้ว พนักงานเจ้าหน้าที่จะแจ้งจำนวนเงินค่าปรับและรายละเอียดการชำระเงินค่าปรับให้ผู้ประกอบกิจการทราบผ่านระบบอิเล็กทรอนิกส์"
                        return  text_message
                    elif(message == "การชำระเงินค่าปรับสามารถดำเนินการชำระผ่านช่องทางใดได้บ้าง"):
                        text_message = "1. วิธีการจ่ายชำระเงินผ่านใบแจ้งการชำระเงิน (Bill Payment) 1.1 ชำระเงินผ่านเคาน์เตอร์ธนาคารได้ทุกธนาคารที่เข้าร่วมโครงการ Bill Payment Prompt pay 1.2 ชำระเงินผ่านเคาน์เตอร์เซอร์วิส (7-Eleven ทุกสาขา) 1.3 ชำระเงินผ่านเครื่อง ATM 1.4 ชำระเงินผ่าน application ของธนาคารผู้ให้บริการบนโทรศัพท์มือถือ (Mobile Banking) ด้วยช่องทาง QR Code หรือ Bar Code 2. วิธีการจ่ายชำระเงินด้วยวิธีออนไลน์ (Online Payment) 2.1 ชำระเงินด้วยบัตรเครดิต/บัตรเครดิต 2.2 ชำระเงินผ่าน Internet Banking ของธนาคารผู้ให้บริการ 2.3 ชำระเงินผ่านการหักเงินจากบัญชีธนาคารของผู้ใช้บริการ รายละเอียดเพิ่มเติม https://epayment.cgd.go.th/e-payment/files/posts/267/file.pdf"


                        return text_message
                    elif(message == "ภายหลังจากชำระเงินค่าปรับแล้วจะได้รับใบเสร็จรับเงินอิเล็กทรอนิกส์(e-Receipt)เมื่อใด"):
                        text_message = "การออกใบเสร็จรับเงินแบบอิเล็กทรอนิกส์ของระบบแบ่งเป็น 2 กรณี คือ 1. กรณีชำระค่าบริการแบบออนไลน์ผ่านหน้าเว็บไซต์ของระบบการรับชำระเงินกลางฯ ด้วยวิธีการหักเงินจากบัญชีธนาคาร บัตรเครดิต/บัตรเดบิต หรือชำระเงินผ่านช่องทางเคาน์เตอร์ธนาคาร (เฉพาะชำระด้วยเงินสด) ATM Mobile และ Internet Banking ผู้ใช้บริการจะได้ใบเสร็จรับเงินแบบอิเล็กทรอนิกส์ทันที ผ่านทาง e-mail หรือค้นหาผ่านหน้าเว็บไซต์ระบบการรับชำระเงินกลางฯ 2. กรณีชำระค่าบริการผ่านเคาน์เตอร์เซอร์วิส หรือชำระด้วยแคชเชียร์เช็คที่เคาน์เตอร์ธนาคารกรุงไทยฯ ผู้ชำระเงินจะได้ใบเสร็จรับเงินอิเล็กทรอนิกส์ภายใน 2 - 3 วันทำการ หลังจากวันที่ชำระเงิน"
                        return text_message 
                    
                    return text_message
                
                else : 




                   
                    

                


                    #return "เรื่องที่คุณสอบถามกำลังนำเข้าระบบเพื่อประมวลผล ติดต่อกลับภายหลังนะคะ"
                    results = predict_first_model(message)
                    if(results == "AskDate"):
                        print(results)
                        current_datetime = datetime.datetime.now()
                        Time = current_datetime.strftime("%A %d %B %Y")
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
    elif (request.method == "GET"): #รีเควสGET 
        return "คำสั่งGETของChat Bot"



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
   


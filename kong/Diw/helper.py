import json

folder_state = "\\file-etc\\state_web\\"
def sendtext(userID, folderpath,message_type,_Reply_message,txtjson = ""):
    state = "text_web.json"
    _data_tag = {
                "data_tag":{
                    "message_type":"{}".format(message_type),
                    "message":"{}".format(_Reply_message)}}
                    
    with open(folderpath + folder_state + userID + state, 'w', encoding="utf-8") as f:
        json.dump(_data_tag, f, ensure_ascii=False)
    with open(folderpath + folder_state + userID + state,"r",encoding="utf-8") as f:
        data = json.load(f)
        text_msg_web  = {"type":data["data_tag"]["message_type"],"Massage":data["data_tag"]["message"],"json":txtjson}
    return text_msg_web
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp",methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body","").strip()
    
    response =  MessagingResponse()
    LOGO_URL = "https://res.cloudinary.com/dd4bsgg46/image/upload/v1768571938/Untitled_design_2_t1kqlx.png"
    
             
    MENU_URL = "https://res.cloudinary.com/dd4bsgg46/image/upload/v1786202948/ChatGPT_Image_Aug_8_2026_08_54_57_PM_zonj16.png "
    
             
    response = MessagingResponse()

    message = response.message(
        "👋 Ji aayan nu Brew Cafe! ☕\n"
        "Main Shaliss AI haan 🤖"
    )
    message.media(LOGO_URL)

    menu = response.message()
    menu.media(MENU_URL)

    return str(response)


if __name__ == "__main__":
    app.run(debug=True) 
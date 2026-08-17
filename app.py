from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
from twilio.rest import Client
import time

app = Flask(__name__)
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
MENU_PREVIEW_SID = os.getenv("MENU_PREVIEW_SID")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
BREW_CATEGORY_FLOW_SID = os.getenv("BREW_CATEGORY_FLOW_SID")

client = Client(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
)

LOGO_URL = "https://res.cloudinary.com/dd4bsgg46/image/upload/v1768571938/Untitled_design_2_t1kqlx.png" 

MENU_URL =  "https://res.cloudinary.com/dd4bsgg46/image/upload/v1786202948/ChatGPT_Image_Aug_8_2026_08_54_57_PM_zonj16.png"

MENU = {
    "coffee": {
        "name": "☕ Coffee & Beverages",
        "items": {
            "espresso": ("Espresso", 99),
            "americano": ("Americano", 129),
            "cappuccino": ("Cappuccino", 149),
            "latte": ("Latte", 159),
            "mocha": ("Mocha", 169),
            "cold_coffee": ("Cold Coffee", 149)
        }
    },

    "starters": {
        "name": "🥪 Starters",
        "items": {
            "garlic_bread": ("Garlic Bread", 99),
            "cheesy_garlic_bread": ("Cheesy Garlic Bread", 129),
            "french_fries": ("French Fries", 109),
            "peri_peri_fries": ("Peri Peri Fries", 129),
            "chicken_popcorn": ("Chicken Popcorn", 149),
            "paneer_tikka": ("Paneer Tikka", 179)
        }
    },

    "burgers": {
        "name": "🍔 Burgers",
        "items": {
            "veg_burger": ("Veg Burger", 129),
            "cheese_burger": ("Cheese Burger", 149),
            "paneer_burger": ("Paneer Burger", 159),
            "chicken_burger": ("Chicken Burger", 169)
        }
    },

    "pasta": {
        "name": "🍝 Pasta",
        "items": {
            "white_sauce": ("White Sauce Pasta", 199),
            "red_sauce": ("Red Sauce Pasta", 189),
            "mix_sauce": ("Mix Sauce Pasta", 209),
            "cheesy_pasta": ("Cheesy Pasta", 219),
            "chicken_pasta": ("Chicken Pasta", 249)
        }
    },

    "pizza": {
        "name": "🍕 Pizza",
        "items": {
            "margherita": ("Margherita Pizza", 219),
            "farmhouse": ("Farmhouse Pizza", 259),
            "paneer_tikka_pizza": ("Paneer Tikka Pizza", 279),
            "chicken_bbq": ("Chicken BBQ Pizza", 299),
            "peri_peri_chicken": ("Peri Peri Chicken Pizza", 299)
        }
    },

    "sandwiches": {
        "name": "🥪 Sandwiches",
        "items": {
            "veg_sandwich": ("Veg Sandwich", 99),
            "cheese_sandwich": ("Cheese Sandwich", 119),
            "grilled_sandwich": ("Grilled Veg Sandwich", 129),
            "paneer_sandwich": ("Paneer Tikka Sandwich", 149),
            "club_sandwich": ("Club Sandwich", 169)
        }
    },

    "main_course": {
        "name": "🍚 Main Course",
        "items": {
            "veg_fried_rice": ("Veg Fried Rice", 199),
            "paneer_fried_rice": ("Paneer Fried Rice", 229),
            "veg_noodles": ("Veg Hakka Noodles", 199),
            "paneer_noodles": ("Paneer Hakka Noodles", 229),
            "chicken_fried_rice": ("Chicken Fried Rice", 249)
        }
    },

    "desserts": {
        "name": "🍰 Desserts",
        "items": {
            "brownie": ("Chocolate Brownie", 129),
            "lava_cake": ("Chocolate Lava Cake", 149),
            "cheesecake": ("Cheesecake", 149),
            "ice_cream": ("Ice Cream", 99),
            "sizzling_brownie": ("Sizzling Brownie", 169)
        }
    }
}

carts = {}


def find_item(item_id):
    for category in MENU.values():
        if item_id in category["items"]:
            return category["items"][item_id]
    return None


@app.route("/", methods=["GET"])
def home():
    return "Brew Cafe Bot is running!"


@app.route("/whatsapp", methods=["POST"])
def whatsapp():

    customer = request.values.get("From", "unknown")

    incoming = request.values.get("Body", "").strip().lower()

    selected = request.values.get("ButtonPayload",incoming).strip().lower()
    print("SELECTED:",selected)

    if customer not in carts:
        carts[customer] = {}

    response = MessagingResponse()
    # First message 
    if selected in ["hi", "hello", "start", "Hello"]:

     client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=customer,
        body="👋 Ji aayan nu Brew Cafe! ☕\nMain Shaliss AI haan 🤖",
        media_url=[LOGO_URL],
       status_callback= "https://cafeautomation-zucy.onrender.com/logo-status"  
    )
     
    if selected == "explore_menu":
     try:
          msg = client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=customer,
            content_sid=BREW_CATEGORY_FLOW_SID
        )
          print("FLOW SENT:", msg.sid)
     except Exception as e:
          print("FLOW ERROR:", str(e))

    return "", 200
    
@app.route("/logo-status", methods=["POST"])
def logo_status():
    status = request.values.get("MessageStatus")
    customer = request.values.get("To")

    if status == "delivered":
        client.messages.create(
            from_=TWILIO_WHATSAPP_FROM,
            to=customer,
            content_sid=MENU_PREVIEW_SID
        )
      
       
    return "", 200
    

    # Item selected
    item = find_item(selected)

    if item:                       

        carts[customer]["current_item"] = {
            "id": selected,
            "name": item[0],
            "price": item[1],
            "size": None,
            "quantity": 1
        }

        response.message(
            f"🍽️ {item[0]}\n"
            f"₹{item[1]}\n\n"
            "Choose size:"
        )

        return str(response)

    # Size
    if selected in ["half", "full"]:

        if "current_item" in carts[customer]:

            carts[customer]["current_item"]["size"] = selected

            response.message(
                f"Size: {selected.title()}\n\n"
                "Choose quantity:"
            )

        return str(response)

    # Quantity
    if selected.startswith("qty_"):

        quantity = int(selected.replace("qty_", ""))

        if "current_item" in carts[customer]:

            carts[customer]["current_item"]["quantity"] = quantity

            response.message(
                f"Quantity: {quantity}\n\n"
                "Add to cart?"
            )

        return str(response)

    # Add to cart
    if selected == "add_cart":

        if "current_item" in carts[customer]:

            item = carts[customer]["current_item"]

            carts[customer].setdefault("items", []).append(item)

            del carts[customer]["current_item"]

            response.message(
                "✅ Added to cart!\n\n"
                "What next?"
            )

        return str(response)

    # View cart
    if selected == "view_cart":

        items = carts[customer].get("items", [])

        if not items:
            response.message("🛒 Your cart is empty.")
            return str(response)

        total = 0
        text = "🛒 Your Cart\n\n"

        for item in items:

            subtotal = item["price"] * item["quantity"]
            total += subtotal

            size = item.get("size")

            text += (
                f"{item['name']}\n"
                f"{size.title() if size else ''} × "
                f"{item['quantity']} = ₹{subtotal}\n\n"
            )

        text += f"💰 Total: ₹{total}"

        response.message(text)

        return str(response)

    # Add more
    if selected == "add_more":

        response.message(
            "🍽️ Choose another category."
        )

        return str(response)

    # Checkout
    if selected == "checkout":

        response.message(
            "🧾 Order Summary ready!\n\n"
            "Choose delivery option."
        )

        return str(response)

    # Delivery
    if selected == "home_delivery":

        response.message(
            "🏠 Home Delivery selected.\n\n"
            "Please enter your address."
        )

        return str(response)

    # Pickup
    if selected == "pickup":

        response.message(
            "🏪 Cafe Pickup selected.\n\n"
            "Choose payment:"
        )

        return str(response)

    # Payment
    if selected == "upi":

        response.message(
            "💳 UPI selected.\n\n"
            "Complete payment and confirm your order."
        )

        return str(response)

    if selected == "cash":

        response.message(
            "💵 Cash selected.\n\n"
            "Confirm your order."
        )

        return str(response)

    # Confirm
    if selected == "confirm_order":

        response.message(
            "✅ Order Confirmed!\n\n"
            "Thank you for ordering from Brew Cafe ❤️"
        )

        return str(response)

    response.message(
        "Please choose an option to continue 😊"
    )

    return str(response)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


ALLOWED_PIZZA_SIZES = ["small", "medium", "large", "extra-large", "extra large", "s", "m", "l", "xl"]
ALLOWED_PIZZA_TYPES = ["BURGER","CHICKEN DELIGHT","VEGAN SUPREME","VEGAN HEAVEN","VEGGIE DREAM","TEXAS BBQ","PROSCIUTTO FUNGHI","HAWAIIAN"]
VEGETARIAN_PIZZAS = ["VEGAN SUPREME","VEGAN HEAVEN","VEGGIE DREAM","TEXAS BBQ","PROSCIUTTO FUNGHI","HAWAIIAN"]
MEAT_PIZZAS = ["BURGER","CHICKEN DELIGHT","HAWAIIAN"]


class ValidateSimplePizzaForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_pizza_form"

    def validate_vegetarian(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""
        if tracker.get_intent_of_latest_message() == "affirm":
            dispatcher.utter_message(text="Ok, this is the list of our vegetarian pizzas")
            return {"vegetarian": True}
        if tracker.get_intent_of_latest_message() == "deny":
            dispatcher.utter_message(text="Ok, this is the list of our meat pizzas")
            return {"vegetarian": False}
        dispatcher.utter_message(text="I didn't get that.")
        return {"vegetarian": None}

    def validate_pizza_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""

        if slot_value.lower() not in ALLOWED_PIZZA_SIZES:
            dispatcher.utter_message(text=f"We only accept pizza sizes: s/m/l/xl.")
            return {"pizza_size": None}
        dispatcher.utter_message(text=f"")
        return {"pizza_size": slot_value}

    def validate_pizza_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_type` value."""

        if slot_value not in ALLOWED_PIZZA_TYPES:
            dispatcher.utter_message(text=f"I don't recognize that pizza. We serve {'/'.join(ALLOWED_PIZZA_TYPES)}.")
            return {"pizza_type": None}
        dispatcher.utter_message(text=f"OK! You want to have a {slot_value} pizza.")
        return {"pizza_type": slot_value}

    def validate_custom_pizza(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_size` value."""
        if tracker.get_intent_of_latest_message() == "affirm":
            dispatcher.utter_message(text="Cool, select the option you want to choose.")
            return {"custom_pizza": True}
        if tracker.get_intent_of_latest_message() == "deny":
            dispatcher.utter_message(text="ok")
            return {"custom_pizza": False}
        dispatcher.utter_message(text="I didn't get that.")
        return {"custom_pizza": None}
    def validate_pizza_custom_choice(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `pizza_type` value."""

        
        dispatcher.utter_message(text=f"OK! You want {slot_value} .")
        return {"pizza_custom_choice": slot_value}

class AskForVegetarianAction(Action):
    def name(self) -> Text:
        return "action_ask_vegetarian"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(text="Would you like to order a vegetarian pizza?",
                                 buttons=[
                                     {"title": "yes", "payload": "/affirm"},
                                     {"title": "no", "payload": "/deny"}
                                 ])
        return []

class AskForCustomPizzaAction(Action):
    def name(self) -> Text:
        return "action_ask_custom_pizza"

    def run(
            self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        dispatcher.utter_message(text="Do you want to customise your pizza?",
                                 buttons=[
                                     {"title": "yes", "payload": "/affirm"},
                                     {"title": "no", "payload": "/deny"}
                                 ])
        return []

class AskForPizzaTypeAction(Action):
    def name(self) -> Text:
        return "action_ask_pizza_type"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:


        message1 = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    
                    {
                        "title": "VEGAN SUPREME",
                        "subtitle": "Tomato sauce, Vegan Cheese, Baby Spinach, Mushrooms, Bell Peppers, Fresh Tomatoes, Olives",
                        "image_url": "https://cache.dominos.com/wam/prod/market/CH/_en/images/promo/680149d8-e3dc-4f0a-99cf-d85c95ba71b0.jpg",
                        "buttons": [ 
                            {
                            "title": "Order",
                            "payload": "VEGAN SUPREME",
                            "type": "postback"
                            },

                        ]
                    },
                    {
                        "title": "VEGAN HEAVEN",
                        "subtitle": "Tomato sauce, Vegan Cheese, Baby Spinach, Red Onions, Fresh Tomatoes, Garlic",
                        "image_url": "https://cache.dominos.com/wam/prod/market/CH/_en/images/promo/d1feca27-3fa6-48b5-9f6e-06c1aeae580e.jpg",
                        "buttons": [ 
                            {
                            "title": "Order",
                            "payload": "VEGAN HEAVEN",
                            "type": "postback"
                            },

                        ]
                    },
                    {
                        "title": "VEGGIE DREAM",
                        "subtitle": "Tomato sauce, Mozzarella, Baby Spinach, Red Onions, Bell Peppers, Garlic, Cherry Tomatoes, Olives, Herbes de Provence",
                        "image_url": "https://cache.dominos.com/olo/6_74_5/assets/build/market/CH/_en/images/img/products/larges/S_DRM.jpg",
                        "buttons": [ 
                            {
                            "title": "Order",
                            "payload": "VEGGIE DREAM",
                            "type": "postback"
                            },

                        ]
                    },
                    {
                        "title": "PROSCIUTTO FUNGHI",
                        "subtitle": "Tomato sauce, Mozzarella, Ham, Extra Mushrooms",
                        "image_url": "https://cache.dominos.com/olo/6_74_5/assets/build/market/CH/_en/images/img/products/larges/S_REI.jpg",
                        "buttons": [ 
                            {
                            "title": "Order",
                            "payload": "PROSCIUTTO FUNGHI",
                            "type": "postback"
                            },

                        ]
                    },

                    {
                        "title": "VEGAN CLASSIC",
                        "subtitle": "Tomato sauce, Vegan Cheese",
                        "image_url": "https://cache.dominos.com/wam/prod/market/CH/_en/images/promo/4577961e-152b-41ba-992f-b8b6a4b2ab9c.jpg",
                        "buttons": [ 
                            {
                            "title": "Order",
                            "payload": "VEGAN CLASSIC",
                            "type": "postback"
                            },

                        ]
                    }
                
                    
                ]
                }
          }
        
        message2 = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    
                    
            
                    {
                        "title": "CHICKEN DELIGHT",
                        "subtitle": "\nTomato sauce, Mozzarella, Chicken, Baby Spinach, Cherry Tomatoes, Olives",
                        "image_url": "https://cache.dominos.com/olo/6_74_5/assets/build/market/CH/_en/images/img/products/larges/S_DLT.jpg",
                        "buttons": [ 
                            {
                            "title": "Order",
                            "payload": "CHICKEN DELIGHT",
                            "type": "postback"
                            },

                        ]
                    },
                    {
                        "title": "HAWAIIAN",
                        "subtitle": "Tomato sauce, Mozzarella, Ham, Pineapple",
                        "image_url": "https://cache.dominos.com/olo/6_74_5/assets/build/market/CH/_en/images/img/products/larges/S_HWN.jpg",
                        "buttons": [ 
                            {
                            "title": "Order HAWAIIAN",
                            "payload": "HAWAIIAN",
                            "type": "postback"
                            },

                        ]
                    },                    
                    {
                        "title": "BURGER",
                        "subtitle": "\nTomato sauce, Mozzarella, Beef, Fresh Tomatoes, Red Onions, Pickles, Burger sauce",
                        "image_url": "https://cache.dominos.com/olo/6_74_5/assets/build/market/CH/_en/images/img/products/larges/S_DIA.jpg",
                        "buttons": [ 
                            {
                            "title": "Order",
                            "payload": "BURGER",
                            "type": "postback"
                            },

                        ]
                    }
                ]
                }
        }
        

        if tracker.get_slot("vegetarian"):
            dispatcher.utter_message(attachment=message1)
        else:
            dispatcher.utter_message(attachment=message2)
        return []


class AskForPizzaCustomChoice(Action):
    def name(self) -> Text:
        return "action_ask_pizza_custom_choice"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:


        message1 = {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    
                    {
                        "buttons": [ 
                            {
                            "title": "Toppings",
                            "payload": "Toppings",
                            "type": "postback"
                            },
                            {
                            "title": "Crust Type",
                            "payload": "Crust Type",
                            "type": "postback"
                            },
                            {
                            "title": "Extra Cheese",
                            "payload": "Extra Cheese",
                            "type": "postback"
                            }
                           
                        ]
                    }   
                ]
                }
          }
        


        if tracker.get_slot("custom_pizza"):
            dispatcher.utter_message(attachment=message1)

        return []



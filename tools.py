from datetime import datetime
import requests
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_city_weather(city): 
    url = f"https://wttr.in/{city}?format=3" #format string
    response = requests.get(url, timeout=10)
    return response.text

def get_user_city():
    return "Banglore"

#Tools = [{}, {}, {}]
Tools = [
    {
        "type" : "function", 
        "function" : {
            "name" : "get_current_time",
            "description" : "Get the current time",
            "parameters" : {"type" : "object","properties" : {
                    # "city" : "string"
                    # "description" : "The city to get the current time for"
                }, 
            }
        }
    }, 
    {
            "type" : "function", 
            "function" : {
                "name" : "get_city_weather",
                "description" : "Get the weather for a specific city",
                "parameters" : {"type" : "object","properties" : {
                        "city" : 
                            {"type" : "string", 
                                  "description" : "The city to get the weather for"
                                }
                    }, 
                }
            }
        },
    {
            "type" : "function", 
            "function" : {
                "name" : "get_user_city",
                "description" : "Return the city of user, Get the city of the user, use this tool when asked 'my city','my location', 'my home', without giving the city name",
                "parameters" : {"type" : "object","properties" : {
                        # "city" : 
                        #     {"type" : "string", 
                        #           "description" : "The city to get the weather for"
                        #         }
                    }, 
                }
            }
        }
]


FUNCTION_NAME_TO_FUNCTION = {
    "get_current_time" : get_current_time,
    "get_city_weather" : get_city_weather,
    "get_user_city" : get_user_city
}
from datetime import datetime
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


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
    }    
]


FUNCTION_NAME_TO_FUNCTION = {
    "get_current_time" : get_current_time,
}
from datetime import datetime
import requests
from rag import search
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_city_weather(city): 
    url = f"https://wttr.in/{city}?format=3" #format string
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text

def get_user_city():
    return "Banglore"


def search_knowledge_base(query):
    result = search(query, top_k=2)
    blocks = []
    for res in result:
        sourcefileName = res["source"]
        chunkId = res.get("chunk_id", 0)  # Safe fallback if missing
        chunkText = res["text"]
        header = f"Source: {sourcefileName}, Chunk ID: {chunkId}\n"
        block = f"{header}\n{chunkText}"
        blocks.append(block)
        
    return "\n\n".join(blocks)

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
                    "required" : ["city"]
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
        },
    {
        "type" : "function", 
            "function" : {
                "name" : "search_knowledge_base",
                "description" : "Search the knowledge base for relevant information like leave policy, travel policy, HR policy, company policy, company information, company details, company rules, company regulations, company guidelines, company procedures, company processes, company standards, company practices, company protocols, company instructions, company directives, company mandates, company requirements, company obligations, company responsibilities, company duties, company commitments, company expectations of Zorvex technologies, and return the most relevant information from the knowledge base. Use this tool when asked about company policies, procedures, guidelines, rules, regulations, standards, practices, protocols, instructions, directives, mandates, requirements, obligations, responsibilities, duties, commitments, or expectations of Zorvex technologies.",
                "parameters" : {"type" : "object","properties" : {
                        "query" : 
                            {"type" : "string", 
                                  "description" : "The query to search the knowledge base for"
                                }
                    },
                    "required" : ["query"]
                }
            }
    }
]


FUNCTION_NAME_TO_FUNCTION = {
    "get_current_time" : get_current_time,
    "get_city_weather" : get_city_weather,
    "get_user_city" : get_user_city,
    "search_knowledge_base" : search_knowledge_base
}
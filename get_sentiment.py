import requests # This is for Python based HTTP
import json # This is for parsing the JSON response

# This function uses the "requests" Python module
# to make a POST request to the Google NLP API web service 
# in order to analyze the sentiment of a news article, as in the
# Javascript exercise: https://codepen.io/mayacakmak/pen/dZoega

def get_sentiment(text):
    # Construct the URL for a POST request
    base_url = "https://language.googleapis.com/v1/documents:analyzeSentiment";
    key = "key=AIzaSyBsj362-xU5nMLzBQiTSJ6aTg8uJ_zYR88"
    full_url = base_url + "?" + key 
    
    request_body = { "document": 
                      { "type": "PLAIN_TEXT",
                        "language": "en",
                        "content": text
                      },
                     "encodingType": "NONE"}
    
    # Send the request and get the response
    r = requests.post(full_url, data=json.dumps(request_body))
    
    is_good_news = None
    # Check the status of the response to make sure it is OK
    if r.status_code == requests.codes.ok: # That is 200
        # Parse the JSON response into a dictionary
        response = json.loads(r.text)
        mag = response['documentSentiment']['magnitude']
        score = response['documentSentiment']['score']
        is_good_news = mag > 0 and score > 0
        print("Magnitude:", mag, "Score:", score)
        
    return is_good_news

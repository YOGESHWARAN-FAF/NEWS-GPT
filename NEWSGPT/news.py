import requests
class NEWS:

 def get_news(place,api_key='GNEWS_API_KEY'):
    url= f"https://gnews.io/api/v4/search?q={place}&token={api_key}"
    try:
        response=requests.get(url)
        if response.status_code !=200:
            print(f"Error:Recived status code{response.status_code,response.text}")
            return []
        news_data=response.json().get('articles',[])
        if not news_data:
            print('NO news found')
            
        else:
            return news_data
    except Exception as e:  
        print(f"Error fetching news: {e}")
        return []

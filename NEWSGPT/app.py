from flask import Flask, request, render_template
import google.generativeai as genai
from news import NEWS  

genai.configure(api_key='REPLACE_YOUR_API_KEY')
gemini = genai.GenerativeModel('gemini-2.0-flash')

app = Flask(__name__)

@app.route('/news', methods=['GET', 'POST'])
def news():
    news_results = []

    if request.method == 'POST':
        user_input = request.form.get('place')
        if user_input:
            articles = NEWS.get_news(user_input)  # Assume it returns top 5 articles (list of dicts)

            for article in articles:
                prompt = f"""
📢 You are a smart news summarizer. You will receive a news article as a dictionary.

Your tasks:
1. 📌 Extract key details.
2. ✍️ Write a short summary in clear English.
3. 📝 Write the same summary in Tamil.
4. 🌟 Add 1–3 relevant emojis.
5. 💬 Format clearly with title, date, source, summaries, and link.
6.dont put a **  like a sybols 

Here is the news:
{article}
"""

                try:
                    response = gemini.generate_content(prompt)
                    summary = response.text.strip()

                    news_item = {
                        'title': article.get('title'),
                        'image': article.get('image'),
                        'summary': summary
                    }

                    news_results.append(news_item)
                except Exception as e:
                    news_results.append({
                        'title': article.get('title', 'No title'),
                        'image': article.get('image'),
                        'summary': f"❌ Error: {e}"
                    })

    return render_template('news.html', news_list=news_results)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template
from chatbot.bot import FAQBot

app = Flask(__name__)

faq_bot = FAQBot()

# Simple in-memory cache
cache = {}


@app.route('/')
def index():
    # Show the HTML page
    return render_template('index.html')


@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question']

    # Check if answer is in cache
    if question in cache:
        results = cache[question]
    else:
        # Search FAQs
        results = faq_bot.search_faqs(question)
        # If no FAQ found,general response
        if not results:
            results = faq_bot.generate_response(question)
        # Save answer in cache
        cache[question] = results

    # Show results on the HTML page
    return render_template('index.html', question=question, results=results)


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=True)


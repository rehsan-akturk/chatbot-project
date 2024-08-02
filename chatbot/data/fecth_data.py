import os
import json
import re
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

# Dowloand NLTK  data package
nltk.download('punkt')
nltk.download('stopwords')

class FAQProcessor:
    def __init__(self, faq_dir, faq_url=None):
        self.faq_dir = faq_dir
        self.faq_url = faq_url
        self.stop_words = set(stopwords.words('english'))
        self.faqs = []

    def preprocess_text(self, text):
        # Removing non-alphanumeric characters
        text = re.sub(r'\W', ' ', text)
        # Convert text to lowercase and tokenize
        words = word_tokenize(text.lower())
        # Removing stop words
        filtered_words = []
        for word in words:
            if word not in self.stop_words:
                filtered_words.append(word)
        return filtered_words

    def fetch_faqs_from_site(self):
        if self.faq_url:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            try:
                response = requests.get(self.faq_url, headers=headers)
                response.raise_for_status()
                print("FAQ page accessed.")
                return response.text
            except requests.RequestException as e:
                print(f"An error occurred: {e}")
                return None
        return None

    def parse_faqs_from_site(self, page_source):
        soup = BeautifulSoup(page_source, 'html.parser')
        faq_sections = soup.find_all('div', class_='item-inner border-hover')

        for section in faq_sections:
            question = section.find('div', class_='s__title').get_text(strip=True)
            answer = section.find('div', class_='s__text').get_text(strip=True)
            self.faqs.append({'question': question, 'answer': answer})

    def load_faqs_from_dir(self):
        for root, dirs, files in os.walk(self.faq_dir):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        question = file.replace('.txt', '').replace('_', ' ').strip()
                        answer = f.read().strip()
                        self.faqs.append({'question': question, 'answer': answer})

    def preprocess_faqs(self):
        for faq in self.faqs:
            faq['question_tokens'] = self.preprocess_text(faq['question'])
            faq['answer_tokens'] = self.preprocess_text(faq['answer'])

    def save_faqs_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.faqs, f, ensure_ascii=False, indent=4)

def main():
    faq_dir = 'funderpro-faqs'  # Folder path extracted from ZIP file
    faq_url = 'https://funderpro.com/faqs/'  # FAQ page URL on the website

    processor = FAQProcessor(faq_dir, faq_url)

    # Load data from file system
    processor.load_faqs_from_dir()

    # Pull and process data from the site
    faq_page_source = processor.fetch_faqs_from_site()
    if faq_page_source:
        processor.parse_faqs_from_site(faq_page_source)

    # Pre-process the data and save as JSON
    processor.preprocess_faqs()
    processor.save_faqs_to_json('faqs.json')

if __name__ == "__main__":
    main()

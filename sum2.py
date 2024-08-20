from bs4 import BeautifulSoup as bs
import re
import urllib
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from fake_useragent import UserAgent
from rake_nltk import Rake
import nltk
try:
    nltk.data.find('corpora/stopwords.zip')
except LookupError:
    nltk.download('stopwords')
ua = UserAgent()
rake = Rake()

class AmazonReviewExtractor:
    def get_reviews_summary(self, soup1):
        ul_element = soup1.find('ul', id='histogramTable', class_='a-unordered-list a-nostyle a-vertical _cr-ratings-histogram_style_histogram__-J2UR')

        if ul_element:
            href_links = [a['href'] for a in ul_element.find_all('a', href=True)]
            full_links = ["https://www.amazon.in" + link for link in href_links]

            pos_link = full_links[0]
            neg_link = full_links[-1]

            posreviews = self._get_reviews_from_link(pos_link)
            negreviews = self._get_reviews_from_link(neg_link)

            pos_summary = self._summarize_reviews(posreviews)
            neg_summary = self._summarize_reviews(negreviews)

            pos_key= self._keyword_reviews(posreviews)
            neg_key=self._keyword_reviews(negreviews)

            return [pos_summary,neg_summary,pos_key[0:5],neg_key[0:5]]

    def _get_reviews_from_link(self, link):
        headers = {"User-Agent": ua.random}
        request = urllib.request.Request(link, headers=headers)
        response = urllib.request.urlopen(request)
        soup = bs(response, "html.parser")
        
        review_elements = soup.find_all("span", class_='review-text-content')
        reviews_list = [element.get_text(strip=True) for element in review_elements]
        reviews = " ".join(reviews_list)
        
        # Clean the reviews text
        reviews_cleaned = reviews.replace(r'\'', '\'')
        reviews_cleaned = re.sub(r'\d+\.', '', reviews_cleaned)
        reviews_cleaned = re.sub(r'[^a-zA-Z0-9.:,()\-/ ]', '', reviews_cleaned)
        
        return reviews_cleaned

    def _summarize_reviews(self, reviews, num_sentences=5):
        sentences = sent_tokenize(reviews)
        words = word_tokenize(reviews)
        stop_words = set(stopwords.words('english'))
        
        # Filter out stopwords
        filtered_words = [word for word in words if word.lower() not in stop_words]
        
        # Calculate word frequency
        word_freq = FreqDist(filtered_words)
        
        # Score sentences based on word frequency
        sentence_scores = {}
        for sentence in sentences:
            for word in word_tokenize(sentence.lower()):
                if word in word_freq:
                    if len(sentence.split(' ')) < 30:  # Consider shorter sentences as key points
                        if sentence not in sentence_scores:
                            sentence_scores[sentence] = word_freq[word]
                        else:
                            sentence_scores[sentence] += word_freq[word]
        
        # Select top sentences as the summary
        summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
        summary = ' '.join(summarized_sentences)
        
        return summary
    def _keyword_reviews(self,reviews):
        rake.extract_keywords_from_text(reviews)

        # Get the ranked phrases
        keywords = rake.get_ranked_phrases()

        # Define a list of terms related to technical specs
        technical_specs_terms = [
            'build quality', 'sound quality', 'design', 'battery', 'performance', 'durability',
            'warranty', 'comfort', 'investment', 'specs', 'features', 'hardware', 'processor',
            'RAM', 'storage', 'resolution', 'screen size', 'weight', 'portability', 'connectivity',
            'battery life', 'charging speed', 'speed', 'speed performance', 'graphics', 'camera',
            'software', 'user interface', 'design quality', 'build', 'materials', 'construction',
            'weight', 'dimensions', 'price', 'value', 'reliability', 'versatility', 'functionality',
            'expandability', 'upgradability', 'compatibility', 'usability', 'support', 'service',
            'repairability', 'brand', 'model', 'generation', 'specification', 'technology', 'features',
            'resolution', 'refresh rate', 'input', 'output', 'connectors', 'ports', 'touchscreen',
            'keyboard', 'trackpad', 'mouse', 'audio', 'speakers', 'microphone', 'webcam', 'display',
            'color accuracy', 'contrast ratio', 'brightness', 'power consumption', 'heat dissipation',
            'cooling', 'ergonomics', 'usability', 'ergonomic design', 'manual', 'setup', 'installation',
            'upgrade', 'backlight', 'wireless', 'Bluetooth', 'Wi-Fi', 'networking', 'security',
            'encryption', 'privacy', 'software compatibility', 'hardware compatibility', 'expansion slots',
            'dock', 'adapter', 'cable', 'charger', 'battery life', 'energy efficiency', 'operating system',
            'software updates', 'performance benchmarks', 'hardware benchmarks', 'user reviews',
            'customer feedback', 'after-sales service', 'return policy', 'refund policy'
        ]

        filtered_keywords = [keyword for keyword in keywords if any(term in keyword.lower() for term in technical_specs_terms)]
        return filtered_keywords



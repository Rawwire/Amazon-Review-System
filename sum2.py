from bs4 import BeautifulSoup as bs
import re
import urllib
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from fake_useragent import UserAgent

ua=UserAgent()

class AmazonReviewExtractor:
    def get_reviews_summary(self,soup1):

        anchor_element = soup1.find(class_="aok-nowrap a-nowrap")
        if anchor_element:
            href_link = anchor_element.find('a')['href']
            base_url = "https://www.amazon.in"
            amazon_url = base_url + str(href_link)
            amazon_url2=amazon_url.replace("five","one")
            headers = {"User-Agent": ua.random}
            request = urllib.request.Request(amazon_url, headers=headers)
            response = urllib.request.urlopen(request)
            soup1 = bs(response, "html.parser")
            elements = soup1.find_all(class_="a-size-base review-text review-text-content")
            name = ' '.join([element.get_text() for element in elements])
            cleaned_text = name.replace("\n", " ")
            cleaned_text = re.sub(r'\d+\.', '', cleaned_text)
            cleaned_text = re.sub(r'[^a-zA-Z0-9.:,()\-/ ]', '', cleaned_text)
            def summarize_paragraph(paragraph, num_sentences=2):
                sentences = sent_tokenize(paragraph)
                words = word_tokenize(paragraph)
                stop_words = set(stopwords.words('english'))
                filtered_words = [word for word in words if word.lower() not in stop_words]
                word_freq = FreqDist(filtered_words)
                sentence_scores = {}
                for sentence in sentences:
                    for word in word_tokenize(sentence.lower()):
                        if word in word_freq:
                            if len(sentence.split(' ')) < 30:
                                if sentence not in sentence_scores:
                                    sentence_scores[sentence] = word_freq[word]
                                else:
                                    sentence_scores[sentence] += word_freq[word]
                summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
                return ' '.join(summarized_sentences)
            paragraph = cleaned_text
            summary_pos = summarize_paragraph(paragraph)
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}
            request = urllib.request.Request(amazon_url2, headers=headers)
            response = urllib.request.urlopen(request)
            soup1 = bs(response, "html.parser")
            elements = soup1.find_all(class_="a-size-base review-text review-text-content")
            name = ' '.join([element.get_text() for element in elements])
            cleaned_text = name.replace("\n", " ")
            cleaned_text = re.sub(r'\d+\.', '', cleaned_text)
            cleaned_text = re.sub(r'[^a-zA-Z0-9.:,()\-/ ]', '', cleaned_text)
            def summarize_paragraph(paragraph, num_sentences=2):
                sentences = sent_tokenize(paragraph)
                words = word_tokenize(paragraph)
                stop_words = set(stopwords.words('english'))
                filtered_words = [word for word in words if word.lower() not in stop_words]
                word_freq = FreqDist(filtered_words)
                sentence_scores = {}
                for sentence in sentences:
                    for word in word_tokenize(sentence.lower()):
                        if word in word_freq:
                            if len(sentence.split(' ')) < 30:
                                if sentence not in sentence_scores:
                                    sentence_scores[sentence] = word_freq[word]
                                else:
                                    sentence_scores[sentence] += word_freq[word]
                summarized_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
                return ' '.join(summarized_sentences)
            paragraph = cleaned_text
            summary_neg = summarize_paragraph(paragraph)
            summary=[summary_pos,summary_neg]
            return summary
    

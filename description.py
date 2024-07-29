import re
class AmazonDescription():
    def description_amazon(self,soup):
        anchor_element = soup.find(class_="a-section a-spacing-medium a-spacing-top-small")
        element=anchor_element.find_all(class_="a-list-item")
        cleaned_texts =[]
        for item in element:
            text = item.get_text()
            cleaned_text = text.replace("\n", " ")
            cleaned_text = re.sub(r'\d+\.', '', cleaned_text)
            cleaned_text = re.sub(r'[^a-zA-Z0-9.:,()\-/ ]', '', cleaned_text)
            cleaned_texts.append(cleaned_text)
        return cleaned_texts
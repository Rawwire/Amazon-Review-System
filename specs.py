class specifications():
    def spec(soup):
        try:
            tech_spec_section = soup.find(id="productDetails_techSpec_section_1")
            prod_det_entries = tech_spec_section.find_all(class_="prodDetSectionEntry")
            values1 = [entry.get_text(strip=True) for entry in prod_det_entries]
        except:
            values1=["nf"]
        try:
            tech_spec_section1= soup.find(id="productDetails_techSpec_section_1")
            prod_det=tech_spec_section1.find_all(class_="prodDetAttrValue")
            values2= [entry.get_text(strip=True) for entry in prod_det]
        except:
            values2=["nf"]
        spec_dict = dict(zip(values1, values2))
        
        return spec_dict
    # .
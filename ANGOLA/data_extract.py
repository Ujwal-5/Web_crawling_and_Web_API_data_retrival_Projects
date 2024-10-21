from lxml import html

def exract_data_using_xpath(response, xpath):
    try:
        tree = html.fromstring(response.encode('utf-8'))
        text = tree.xpath(xpath)
        text = text[0].strip() if text else None
        return text
    except:
        return None
from google.cloud import vision
from django.conf import settings
from dotenv import load_dotenv
import os, requests

def detect_text(image_byte):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = settings.GOOGLE_CREDENTIALS_PATH

    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_byte)

    response = client.text_detection(image=image)
    result = response.text_annotations

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return result


def get_info(q):
    load_dotenv()

    API_URL = 'http://www.aladin.co.kr/ttb/api/ItemSearch.aspx'
    API_KEY = os.environ.get('REACT_APP_API_KEY')
    params = {
        'ttbkey': API_KEY,
        'Query': q,
        'QueryType': 'Keyword',
        'SearchTarget' : 'Book',
        'Cover': 'Big',
        'MaxResults': 30,
        'output': 'js',
        'Version': '20131101',
        'outofStockfilter': 1, 
    }
    
    response = requests.get(API_URL, params=params)

    try:
        books = response.json()
        if 'item' not in books:
            raise ValueError("No books found in the response")
        book_infos = books['item']
    except (ValueError, KeyError) as e:
        return {'error': str(e)}

    books = response.json()
    book_infos = books['item']

    search_result = []
    for idx in range(len(book_infos)):
        search_result.append({
            'title': book_infos[idx]['title'],
            'author': book_infos[idx]['author'].split(' (지은이)')[0],
            'pub_date': book_infos[idx]['pubDate'],
            'description': book_infos[idx]['description'],
            'cover': book_infos[idx]['cover']
        })

    result = {'query': books['query'], 'result': search_result}
    return result
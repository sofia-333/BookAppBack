import json

import urllib3


def get_book_data(isbn):
    print("Getting book from openlibrary")
    http = urllib3.PoolManager()
    url = f'https://openlibrary.org/api/volumes/brief/isbn/{isbn}.json'
    try:
        response = http.request('GET', url)
        json_response = json.loads(response.data)
        book = {}
        if json_response:
            records = json_response['records']
            for i, j in records.items():
                book_data = j.get('data')
                book = {
                    'isbn_10': book_data.get('identifiers').get('isbn_10')[0] if book_data.get(
                        'identifiers') and book_data.get('identifiers').get('isbn_10') else isbn if len(
                        isbn) == 10 else None,
                    'isbn_13': book_data.get('identifiers').get('isbn_13')[0] if book_data.get(
                        'identifiers') and book_data.get('identifiers').get('isbn_13') else isbn if len(
                        isbn) == 13 else None,
                    'title': book_data.get('title'),
                    'authors': book_data.get('authors'),
                    'number_of_pages': book_data.get('number_of_pages'),
                    'publish_date': book_data.get('publish_date'),
                    'publishers': book_data.get('publishers'),
                    'publish_places': book_data.get('publish_places'),
                    'subjects': book_data.get('subjects'),
                    'subject_places': book_data.get('subject_places'),
                    'subject_people': book_data.get('subject_people'),
                    'notes': book_data.get('notes'),
                    'links': book_data.get('links'),
                    'cover_url': book_data.get('cover').get('medium') if book_data.get('cover') else '',

                }
            return book
        print("No books found with provided ISBN")
        return {}
    except Exception as e:
        print(f"Something went wrong: {e}")
        return {}

# get_book_data('179714510X')

import re
import urllib.request
import urllib.error


def get_page(url):
    response_data = {'data': None, 'errors': None}
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            response_data['data'] = response.read().decode('utf-8', 'ignore')
    except ValueError as e:
        response_data['errors'] = e
    except urllib.error.URLError as e:
        response_data['errors'] = e
    return response_data


def get_phone_numbers_in_page(page, phone_pattern):
    if page['errors']:
        return
    phones = re.findall(phone_pattern, page['data'])
    return phones


def clean_phone(phone):
    return re.sub(r'\D', '', phone)


def get_clean_phones_from_url(url):
    phone_pattern = r'\+{0,1}[78]\s*\(*\d{3}\)*\s*\d{3}-*\s*\d{2}-*\s*\d{2}'
    phones = get_phone_numbers_in_page(get_page(url), phone_pattern)
    if not phones:
        return
    return set(map(clean_phone, phones))


def main():
    urls = ['http://y.g', '', 'https://www.i-media.ru/company/contacts/', 'https://hands.ru/company/about', 'https://repetitors.info']
    phones = {}
    for url in urls:
        phones[url] = (get_clean_phones_from_url(url))
    print(phones)


if __name__ == '__main__':
    main()

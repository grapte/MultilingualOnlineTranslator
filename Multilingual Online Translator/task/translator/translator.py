import sys
from types import SimpleNamespace

from bs4 import BeautifulSoup
import requests

http_status_codes = {
    100: "Continue",
    101: "Switching Protocols",
    103: "Early Hints",
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    304: "Not Modified",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout"
}

src_lang: str

i18n = [
    'arabic',
    'german',
    'english',
    'spanish',
    'french',
    'hebrew',
    'japanese',
    'dutch',
    'polish',
    'portuguese',
    'romanian',
    'russian',
    'turkish',
]

def main():
    headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/93.0.4577.82 Safari/537.36'}

    from_lang = sys.argv[1]
    if from_lang not in i18n:
        print(f"Sorry, the program doesn't support {from_lang}")
        return
    trans = sys.argv[2]
    if trans not in i18n and trans != 'all':
        print(f"Sorry, the program doesn't support {trans}")
        return
    word = sys.argv[3]

    old_sys_stdout = sys.stdout
    with open(f"{word}.txt", "w") as f:
        sys.stdout = f

        if trans == 'all':
            for to_lang in i18n:
                if to_lang == from_lang:
                    continue
                url = f'https://context.reverso.net/translation/{from_lang}-{to_lang}/{word}'
                page = requests.get(url, headers=headers)
                if 'not found in Context.' in page.text:
                    sys.stdout = old_sys_stdout
                    print(f'Sorry, unable to find {word}')
                    return
                match page.status_code:
                    case 200:
                        soup = BeautifulSoup(page.text, 'html.parser')
                        terms = [
                            term['data-term']
                            for term in soup.find_all(attrs={'data-term': True})
                        ]
                        print(f'{to_lang.capitalize()} Translations:')
                        print(terms[0])
                        print()
                        examples = [
                            text.text.replace('\r', '').replace('\n', '').strip()
                            for example in soup.find_all(attrs={'class': 'example'})
                            for text in example.find_all(attrs={'class': 'text'})
                        ]
                        print(f'{to_lang.capitalize()} Examples:')
                        print(examples[0])
                        print(examples[1])
                        print()
                    case _:
                        sys.stdout = old_sys_stdout
                        print('Something wrong with your internet connection')
                        return
        else:
            to_lang = trans
            url = f'https://context.reverso.net/translation/{from_lang}-{to_lang}/{word}'
            page = requests.get(url, headers=headers)
            if 'not found in Context.' in page.text:
                sys.stdout = old_sys_stdout
                print(f'Sorry, unable to find {word}')
                return
            match page.status_code:
                case 200:
                    soup = BeautifulSoup(page.text, 'html.parser')
                    terms = [
                        term['data-term']
                        for term in soup.find_all(attrs={'data-term': True})
                    ]
                    print(f'{to_lang.capitalize()} Translations:')
                    for t in terms:
                        print(t)
                    print()
                    examples = [
                        text.text.replace('\r', '').replace('\n', '').strip()
                        for example in soup.find_all(attrs={'class': 'example'})
                        for text in example.find_all(attrs={'class': 'text'})
                    ]
                    print(f'{to_lang.capitalize()} Examples:')
                    for i, e in enumerate(examples):
                        print(e)
                        if i % 2 == 1:
                            print()
                case _:
                    sys.stdout = old_sys_stdout
                    print('Something wrong with your internet connection')
                    return
        sys.stdout = old_sys_stdout

    with open(f"{word}.txt", "r") as f:
        for line in f:
            print(line, end="")

if __name__ == '__main__':
    main()

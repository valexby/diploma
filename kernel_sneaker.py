#!/usr/bin/env python3

import requests
import sys

def get_python_id(language, ace_language, notebook):
    TOKEN_LEN = 1000
    params = {
    'sortBy': 'hotness',
    'group': 'everyone',
    'pageSize': TOKEN_LEN,
    }
    init = True
    init_url = 'https://www.kaggle.com/kernels/all/0'
    response = requests.get(init_url)
    while True:
        for kernel in response.json():
            import ipdb
            ipdb.set_trace()
            if kernel['languageName'] == language \
               and kernel['aceLanguageName'] == ace_language \
               and kernel['isNotebook'] == notebook:
                return kernel['scriptVersionId']
        if init:
            init = False
        elif len(response.json()) < TOKEN_LEN:
            return None
        params['after'] = response.json()[-1]['id']
        response = requests.get('https://www.kaggle.com/kernels.json', params=params)

def main():
    if len(sys.argv) < 5:
        print("./sript.py <output_file> <language> <ace_language> <notebook>")
        return 1

    out_filename = sys.argv[1]
    language = sys.argv[2]
    ace_language = sys.argv[3]
    notebook = sys.argv[4] == 'true'

    download_url = 'https://www.kaggle.com/kernels/sourceurl/{}'.format(get_python_id(language, ace_language, notebook))
    r = requests.get(download_url)
    r = requests.get(r.content)
    f = open(out_filename, 'wb')
    f.write(r.content)
    f.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())

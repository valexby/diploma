#!/usr/bin/env python3

import requests
import sys


def get_python_id():
    init_url = 'https://www.kaggle.com/kernels/all/0'
    response = requests.get(init_url)
    for kernel in response.json():
        if kernel['languageName'] == 'Python':
            return kernel['scriptVersionId']

def main():
    if len(sys.argv) < 2:
            print("Put output filename in args please")
            return 1

    out_filename = sys.argv[1]
    download_url = 'https://www.kaggle.com/kernels/sourceurl/{}'.format(get_python_id())
    r = requests.get(download_url)
    r = requests.get(r.content)
    f = open(out_filename, 'wb')
    f.write(r.content)
    f.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())

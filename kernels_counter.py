#!/usr/bin/env python3
import requests
import json

TOKEN_LEN = 1000

init_url = 'https://www.kaggle.com/kernels/all/0'
r = requests.get(init_url)
kernels_number = len(r.json())
kernels_ids = {k['id'] for k in r.json()}

params = {
    'sortBy': 'hotness',
    'group': 'everyone',
    'pageSize': TOKEN_LEN,
}

kernel_list_url = 'https://www.kaggle.com/kernels.json'

while True:
    print(kernels_number)
    params['after'] = r.json()[-1]['id']
    r = requests.get(kernel_list_url, params = params)
    for k in r.json():
        kernels_ids.add(k['id'])
    kernels_number += len(r.json())
    if len(kernels_ids) != kernels_number:
        print('{} != {}'.format(len(kernels_ids), kernels_number))
        break
    if len(r.json()) != TOKEN_LEN:
        break

print('Kernels number: {}'.format(kernels_number))

f = open('out', 'w')
f.write(json.dumps(list(kernels_ids)))
f.close()

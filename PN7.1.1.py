import requests

sites = [
    'https://zerocoder.ru',
    'https://github.com',
    'https://chatgpt.com'
]

for site in sites:
    resp = requests.get(site)

    if resp.status_code == 200:
        with open(f'{site.removeprefix('https://')}.html', 'wb') as f:
            f.write(resp.content)
    else:
        print(f'Site {site} returned {resp.status_code}')

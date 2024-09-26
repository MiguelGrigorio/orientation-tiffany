import requests


response = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open('test/images/file1.jpg', 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': 'Sv46JNKkZCxJqwNtP5QwSk7q'},
)
if response.status_code == requests.codes.ok:
    with open('test/images/removed/file1.png', 'wb') as out:
        out.write(response.content)
else:
    print("Error:", response.status_code, response.text)

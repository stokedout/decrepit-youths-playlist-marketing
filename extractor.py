from requests import get, post
from sys import exit
from pprint import pprint
from datetime import datetime, timedelta
import re
import os

HOST = 'https://api.chartmetric.com'


def get_access_token(refresh_token):
    res = post(f'{HOST}/api/token', json={"refreshtoken": refresh_token})
    for header in res.headers:
        print(header)
    if res.status_code != 200:
        raise RuntimeError(f'ERROR: received a {res.status_code} instead of 200 from /api/token')

    return res.json()


def get_offset():
    print(os.getcwd())
    with open('offset.txt', 'r') as offset:
        return int(offset.read().strip())


def set_offset(value):
    with open('offset.txt', 'w') as f:
        return f.write(str(value))


limit = 100


def get_playlists_by_artist(offset, access_token, artist_id = 2366):
    platform = 'spotify'
    status = 'current'
    since = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%d')
    sort_column = 'followers'

    # excludeCharts = true
    # fromDaysAgo = 365
    # limit = 200
    # offset = 0
    # primaryArtist = false
    # toDaysAgo = 0
    # withTotal = true
    # sortBy = followers
    # sortDirection = descending
    # ids[] = 2366
    # indie = true

    # uri = (
    #     f'/api/artist/{id}/{platform}/{status}/playlists?limit={limit}&offset={offset}&since={since}&sortColumn={sort_column}'
    #     f'&sortOrderDesc=true'
    #     f'&editorial=false&personalized=false&chart=false&thisIs=false&newMusicFriday=false'
    #     f'&radio=false&fullyPersonalized=false&brand=false&majorCurator=false'
    #     f'&popularIndie=false&indie=false&audiobook=false')

    uri = (
        f'/api/artist/{id}/{platform}/{status}/playlists?limit={limit}&offset={offset}&since={since}&sortColumn={sort_column}'
        f'&sortOrderDesc=true'
        f'&chart=false'
        f'&brand=false'
        f'&indie=true')

    # uri = (f'/api/artist/{id}/{platform}/{status}/playlists?limit={limit}&since={since}')

    return get(f'{HOST}{uri}', headers={'Authorization': f'Bearer {access_token}'})


def extract_emails(text):
    # Regular expression pattern for matching email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Find all matches of the email pattern in the text
    emails = re.findall(email_pattern, text)

    return emails


rows = {}


def append_to_csv(artist_id, name, owner, followers, email):
    key = f'{name},{owner},{followers},{email}'
    if key in rows:
        return

    rows[key] = True

    with open(f'{artist_id}.csv', 'a') as file:
        print(f'{name},{owner},{followers},{email}')
        file.write(f'{name},{owner},{followers},{email}\n')


def extract(refresh_token, artist_id):
    token_response = get_access_token(refresh_token)
    access_token = token_response['token']
    expires_in = int(token_response['expires_in'])
    expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

    while True:
        if datetime.utcnow() > expires_at:
            print('refresh token')
            token_response = get_access_token()
            access_token = token_response['token']
            expires_in = token_response['expires_in']
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

        offset = get_offset()
        print(offset)

        res = get_playlists_by_artist(offset, access_token, artist_id)
        if res.status_code != 200:
            raise RuntimeError(f'ERROR: received a {res.status_code} instead of 200 from /api/token')

        playlists = res.json()['obj']

        if len(playlists) == 0:
            print('No more playlists found')
            break

        for playlist in playlists:
            name = playlist['playlist']['name']
            owner = playlist['playlist']['owner_name']
            followers = playlist['playlist']['followers']
            description = playlist['playlist']['description']
            emails = extract_emails(description)

            for email in emails:
                append_to_csv(artist_id, name, owner, followers, email)

        offset += limit
        set_offset(offset)



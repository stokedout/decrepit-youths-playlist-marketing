from requests import get, post
from datetime import datetime, timedelta
import re
import os

HOST = 'https://api.chartmetric.com'


def get_access_token(refresh_token):
    res = post(f'{HOST}/api/token', json={"refreshtoken": refresh_token})

    if res.status_code != 200:
        raise RuntimeError(f'ERROR: received a {res.status_code} instead of 200 from /api/token')

    return res.json()


def get_offset_path(artist_id):
    return f'/data/{artist_id}_offset.txt'


def get_data_path(artist_id):
    return f'/data/{artist_id}.csv'


def ensure_offset_exists(artist_id):
    if os.path.exists(get_offset_path(artist_id)):
        return

    print('Creating offset file')
    with open(get_offset_path(artist_id), 'w') as f:
        return f.write(str(0))


def get_offset(artist_id):
    ensure_offset_exists(artist_id)
    with open(get_offset_path(artist_id), 'r') as offset:
        return int(offset.read().strip())


def set_offset(artist_id, value):
    with open(get_offset_path(artist_id), 'w') as f:
        return f.write(str(value))


limit = 100


def get_playlists_by_artist(offset, access_token, artist_id):
    platform = 'spotify'
    status = 'current'
    since = (datetime.utcnow() - timedelta(days=365)).strftime('%Y-%m-%d')

    uri = (
        f'/api/artist/{artist_id}/{platform}/{status}/playlists'
        f'?limit={limit}'
        f'&offset={offset}'
        f'&since={since}'
        f'&sortColumn=followers'
        f'&sortOrderDesc=true'
        f'&chart=false'
        f'&brand=false'
        f'&indie=true'
    )

    return get(f'{HOST}{uri}', headers={'Authorization': f'Bearer {access_token}'})


def extract_emails(text):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    return emails


rows = {}


def append_to_csv(artist_id, name, owner, followers, email):
    key = f'{name},{owner},{followers},{email}'
    if key in rows:
        return

    rows[key] = True

    with open(get_data_path(artist_id), 'a') as file:
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
            token_response = get_access_token(refresh_token)
            access_token = token_response['token']
            expires_in = token_response['expires_in']
            expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

        offset = get_offset(artist_id)
        print(offset)

        res = get_playlists_by_artist(offset, access_token, artist_id)
        if res.status_code != 200:
            raise RuntimeError(f'ERROR: received a {res.status_code} instead of 200 from /api/artist/-/-/-/playlists')

        playlists = res.json()['obj']

        if len(playlists) == 0:
            print(f'No more playlists found. See results in file {artist_id}.csv.')
            break

        for playlist in playlists:
            name = playlist['playlist']['name']
            owner = playlist['playlist']['owner_name']
            followers = playlist['playlist']['followers'] if "followers" in playlist['playlist'] else "not set"
            description = playlist['playlist']['description']
            emails = extract_emails(description)

            for email in emails:
                append_to_csv(artist_id, name, owner, followers, email)

        offset += limit
        set_offset(artist_id, offset)



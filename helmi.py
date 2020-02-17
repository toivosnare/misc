import requests
from datetime import datetime, timedelta

channel = 57
limit = 50000
url = f'https://supla-playlist.nm-services.nelonenmedia.fi/playlist?channel={channel}&next_token=&limit={limit}'
r = requests.get(url)
items = r.json()['items']
tracks = []

for item in items:
    # print(item['artist'], "-", item['song'], end=': ')
    for track in tracks:
        if item['artist'] == track['artist'] and item['song'] == track['song']:
            # print('adding new timestamp')
            track['timestamps'].append(item['date'])
            break
    else:
        # print("adding new track")
        tracks.append({'artist' : item['artist'], 'song' : item['song'], 'timestamps' : [item['date']]})

for track in tracks:
    # print(track['artist'], "-", track['song'], end=': ')
    if len(track['timestamps']) > 1:
        last_time = datetime.strptime(track['timestamps'][0], '%Y-%m-%dT%H:%M:%S.%fZ')
        total_time = None
        for now_timestamp in track['timestamps'][1:]:
            now_time = datetime.strptime(now_timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
            delta_time = last_time - now_time
            if total_time:
                total_time += delta_time
            else:
                total_time = delta_time
            last_time = now_time
        average = total_time/(len(track['timestamps'])-1)
        # print(str(average))
        track['average'] = average
    else:
        # print("soitettu vain kerran")
        track['average'] = timedelta.max

tracks.sort(key=lambda t: t['average'].total_seconds(), reverse=True)

for track in tracks:
    print(track['artist'], "-", track['song'], ":", str(track['average']), len(track['timestamps']))

print(len(tracks))


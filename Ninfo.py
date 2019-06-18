import dbus
from colorthief import ColorThief
from datetime import datetime
from fabulous.image import Image
from mpris2 import get_players_uri, Player, TrackList
from sty import fg, bg
from urllib.parse import quote
from urllib.request import urlopen


def PrintShareLink(artist, title, url):
    text = quote(title + " by " + artist)
    url = quote(url)
    
    print(fg(29, 161, 242) + 'Twitter:' + fg.rs, 
            f"https://twitter.com/intent/tweet?hashtags=NowPlaying&related=spotify&text={text}&url={url}")

    print(fg(32, 164, 226) + 'Telegram:' + fg.rs, 
            f"https://telegram.me/share/url?url={url}")

for uri in get_players_uri():
    app_color = fg(255, 255, 255)
    if 'spotify' in uri:
        app = 'Spotify'
        app_color = fg(30, 215, 96)
    elif 'chrome' in uri:
        app = 'Google Chrome'
    else:
        app = str(uri).split('.')[-1]

    meta = Player(dbus_interface_info={'dbus_uri': uri}).Metadata
    tracks = TrackList(dbus_interface_info={'dbus_uri': uri})

    try:
        print(app_color + '{:-^60}'.format(app) + fg.rs)

        if 'mpris:artUrl' in meta:
            art = urlopen(meta['mpris:artUrl'])
            colors = ColorThief(art).get_color(quality=1)
        else:
            colors = (255, 255, 255)

        print(fg(colors[0], colors[1], colors[2]))

        if type(meta['xesam:artist']) == dbus.Array:
            artist = meta['xesam:artist'][0]
        else:
            artist = meta['xesam:artist']

        print('{:^60}'.format(artist))
        print('{:^60}'.format(meta['xesam:title']), '\n' + fg.rs)
        
        if 'xesam:trackNumber' in meta:
            print('#', meta['xesam:trackNumber'])
        
        if 'mpris:artUrl' in meta:
            print(Image(urlopen(meta['mpris:artUrl']), 30))
            PrintShareLink(meta['xesam:artist'][0],
                           meta['xesam:title'], 
                           meta['xesam:url'])

#        for track in tracks:
#            print(track)

        print(''.center(80, '-'), '\n')

    except Exception as e:
        f = open('log.txt', 'a')
        f.write(str(datetime.now()) + ' - ' + 'Exception: ' + str(e) + '\n')



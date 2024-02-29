
# Decrepit Youths Playlist Marketing

A script to extract the email addresses from playlists description given an artist identifier using Chart Metric API.

#  Dependencies

What you need in order to use this script.

* A Chart Metric account
* A Chart Metric API access
* A Chart Metric API refresh token (provided by email once you are approved for API use)
* Mac OSX or Linux
* Terminal app (should be installed by default)

## Installation

The following commands only need to be run once per computer. Copy and paste each `command` into the Terminal app and enter your password when required.

* Install Docker https://docs.docker.com/desktop/install/mac-install/ and choose the download that matches your hardware. For example if you have an M1, M2 or M3 Macbook then it's 'Apple Silicon' if you have i5, i7 etc it's 'Intel'
  If you're unsure try `uname -m`
  * x86_64 = Intel
  * arm64 = Apple Silicon
  Upon installing just go through the installation wizard and choose the recommended settins.
* Verify Docker has installed `docker --version` and you should see roughly `Docker version ****, build ****`

## Usage

Copy and paste the `command` text below into the Terminal app each time you use it.
You need to replace `REFRESH_TOKEN` and `ARTIST_ID` with real values.

> An artist identifier e.g. '2366' can be found in the URL of each artist page in Chart Metric
> e.g. https://app.chartmetric.com/artist/2366 

```commandline
docker run --pull=always --platform linux/x86_64 --rm -v $PWD:$PWD ghcr.io/stokedout/decrepit-youths-playlist-marketing/email-extractor:main \
  --refresh_token=REFRESH_TOKEN \
  --artist_id=ARTIST_ID
```

e.g. with fake values
```commandline 
docker run --pull=always --platform linux/x86_64 --rm -v $PWD:$PWD ghcr.io/stokedout/decrepit-youths-playlist-marketing/email-extractor:main \
  --refresh_token=2ef46b342cc74686ac64ed5a0e27942c2ef46b342cc74686ac64ed5a0e27942c \
  --artist_id=1234
```

Once it begins you can see some of the output in the Terminal.
It will generate two files where ARTIST_ID the artist identifier you've chosen:
* 'ARTIST_ID.csv' - contains extracted email addresses
* 'ARTIST_ID_offset.txt' - used internally therefore ignore this file

> Due to restrictions on the API it has to run slowly in order to work within the set limits therefore just run the command and let it work in the background. It may take 30 seconds to 10 hours depending on how many playlists an artist has.

## Troubleshooting

* `ERROR: received a 429 instead of 200 from /api/token` - if you see this then you have reached the limit of how many times you can use the API.
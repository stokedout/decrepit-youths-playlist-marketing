
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

* Install Docker `curl -fsSL get.docker.com | bash`
* Verify Docker has installed `docker --version` and you should see roughly `Docker version ****, build ****`
* Set permissions to run the script `chmod +x ./run.sh`

## Usage

Copy and paste the `command` text below into the Terminal app each time you use it.
You need to replace `REFRESH_TOKEN` and `ARTIST_ID` with real values.

```commandline
sudo ./run.sh REFRESH_TOKEN ARTIST_ID
```

e.g. with fake values
```commandline
sudo ./run.sh 2ef46b342cc74686ac64ed5a0e27942c2ef46b342cc74686ac64ed5a0e27942c 1234
```

> Due to restrictions on the API it has to run slowly in order to work within the set limits therefore just run the command and let it work in the background. It may take 30 seconds to 10 hours depending on how many playlists an artist has.

## Troubleshooting

* `ERROR: received a 429 instead of 200 from /api/token` - if you see this then you have reached the limit of how many times you can use the API.
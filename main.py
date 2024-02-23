import argparse
import extractor


# Create business website on wix
# Link stokedout.net domain name
# Get API access token using new website
# Authenticate with chart metrics API
# Start with input artist id "Bring me the horizon"
# Get playlists for an artist filtered by "independent curator"
# Get playlist info
# Extract email address from playlist about (may not exist in text)
# Add email to csv file
# Uploaded csv to marketing email programme and send


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh_token', dest='refresh_token', required=True, type=str,
                        help='Chart Metric API refresh token.')
    parser.add_argument('--artist_id', dest='artist_id', required=True, type=int, help='Artist identifier e.g. 2366')
    args = parser.parse_args()

    extractor.extract(args.refresh_token, args.artist_id)


if __name__ == '__main__':
    main()

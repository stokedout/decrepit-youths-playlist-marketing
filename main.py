import argparse
import extractor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh_token', dest='refresh_token', required=True, type=str,
                        help='Chart Metric API refresh token.')
    parser.add_argument('--artist_id', dest='artist_id', required=True, type=int, help='Artist identifier e.g. 2366')
    args = parser.parse_args()

    extractor.extract(args.refresh_token, args.artist_id)


if __name__ == '__main__':
    main()

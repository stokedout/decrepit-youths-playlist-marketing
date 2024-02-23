docker build -t email-extractor .
docker run --rm -v $PWD:/app email-extractor --refresh_token $1 --artist_id $2
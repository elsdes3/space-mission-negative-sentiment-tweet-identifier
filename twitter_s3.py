#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Stream Twitter data."""

# pylint: disable=invalid-name
# pylint: disable=broad-except
# pylint: disable=no-self-use
# pylint: disable=unspecified-encoding
# pylint: disable=too-many-locals


import argparse
import datetime
import io
import json
import os
import sys
import time
from csv import writer
from typing import Dict, List

import boto3
from tweepy import Stream


def load_env_vars() -> List[str]:
    """Load environment variables."""
    return [
        os.getenv("AWS_ACCESS_KEY_ID"),
        os.getenv("AWS_SECRET_ACCESS_KEY"),
        os.getenv("AWS_REGION"),
        os.getenv("TWITTER_API_KEY"),
        os.getenv("TWITTER_API_KEY_SECRET"),
        os.getenv("TWITTER_ACCESS_TOKEN"),
        os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    ]


def get_place_list(tweet_place: Dict) -> List:
    """Extract place from tweet metadata."""
    pattrs = [
        "id",
        "url",
        "place_type",
        "name",
        "full_name",
        "country_code",
        "country",
    ]
    if tweet_place:
        place_list = (
            [tweet_place[pattr] for pattr in pattrs]
            + [tweet_place["bounding_box"]["type"]]
            + [str(tweet_place["bounding_box"]["coordinates"])]
            + [str(tweet_place["attributes"])]
        )
    else:
        place_list = ["" for _ in pattrs] + [""] + [str([[]])] + [str({})]
    return place_list


def get_geo_coords_list(tweet: Dict, attr: str = "coordinates") -> List:
    """Extract geo or coordinates from tweet metadata."""
    if tweet[attr]:
        coords_list = (
            tweet[attr]["type"],
            str(tweet[attr]["coordinates"][0]),
            str(tweet[attr]["coordinates"][1]),
        )
        # print(1, tweet[attr])
    else:
        coords_list = ["", "", ""]
        # print(2, tweet[attr])
    return coords_list


def append_list_to_local_csv(list_of_attrs: List[str], fpath: str) -> None:
    """Write list to CSV file."""
    locale_encoding = getattr(io, "LOCALE_ENCODING", None)
    with open(
        fpath, "a", newline="", encoding=locale_encoding
    ) as local_filepath:
        writer_obj = writer(local_filepath, delimiter=",", lineterminator="\n")
        writer_obj.writerow(list_of_attrs)


class TweetStreamListener(Stream):
    """Tweet Streamer following Twitter v1 Developer API."""

    # Class (static) Variables
    keys_wanted = [
        "id",
        "geo",
        "coordinates",
        "place",
        "contributors",
        "is_quote_status",
        "quote_count",
        "reply_count",
        "retweet_count",
        "favorite_count",
        "favorited",
        "retweeted",
        "created_at",
        "source",
        "in_reply_to_user_id",
        "in_reply_to_screen_name",
    ]
    user_keys_wanted = [
        "name",
        "screen_name",
        "followers_count",
        "friends_count",
        "listed_count",
        "favourites_count",
        "statuses_count",
        "protected",
        "verified",
        "contributors_enabled",
        "created_at",
        "location",
    ]
    tweet_number = 1
    max_num_tweets_wanted = 2_000

    # on success
    def on_data(self, raw_data):
        """Retrieve tweet attributes."""
        tweet = json.loads(raw_data)
        max_tweets_wanted = TweetStreamListener.max_num_tweets_wanted
        if TweetStreamListener.tweet_number <= max_tweets_wanted:
            try:
                if "text" in tweet.keys():
                    attrs_to_get = TweetStreamListener.keys_wanted
                    # Get text of the tweek
                    tweet_text = (
                        tweet["text"].replace("\n", "").replace("\r", "")
                    )
                    # Get non-user attributes
                    message_lst = [str(tweet[kw]) for kw in attrs_to_get]
                    # Extract useful part from source
                    source_text = (
                        tweet["source"].split('">')[-1].split("<")[0].strip()
                    )
                    # Get place, coordinates and geo
                    place_list = get_place_list(tweet["place"])
                    coords_list = get_geo_coords_list(tweet, "coordinates")
                    geo_list = get_geo_coords_list(tweet, "geo")
                    # Get user attributes
                    user_attrs_to_get = TweetStreamListener.user_keys_wanted
                    user_list = [
                        str(tweet["user"][user_attr])
                        for user_attr in user_attrs_to_get
                    ]
                    # Combine all extracted attributes
                    message_lst += (
                        [source_text]
                        + place_list
                        + coords_list
                        + geo_list
                        + user_list
                        + [tweet_text, "\n"]
                    )
                    # Export data to local CSV
                    if local_csv_fpath:
                        append_list_to_local_csv(
                            message_lst[:-1], local_csv_fpath
                        )
                    message = "\t".join(message_lst)
                    # Export data to S3, using Kinesis firehose
                    if delivery_stream_name:
                        fhose_response = firehose_client.put_record(
                            DeliveryStreamName=delivery_stream_name,
                            Record={"Data": message},
                        )
                    else:
                        fhose_response = {
                            "ResponseMetadata": {"HTTPStatusCode": ""},
                            "RecordId": "",
                        }
                    # print to screen
                    print(
                        TweetStreamListener.tweet_number,
                        fhose_response["ResponseMetadata"]["HTTPStatusCode"],
                        fhose_response["RecordId"][:5],
                        tweet["created_at"].split(" +")[0],
                        tweet_text[:60],
                    )
                    TweetStreamListener.tweet_number += 1
            except (AttributeError, Exception) as e:
                print(f"{TweetStreamListener.tweet_number} Error: {str(e)}")
            return True
        end_time = datetime.datetime.now()
        duration = (end_time - local_time).total_seconds()
        print(
            f"Twitter streaming ended after {duration:.3f} seconds, "
            f"at {local_time.strftime('%Y-%m-%d %H:%M:%S')}."
        )
        sys.exit()

    def on_error(self, status):
        """Show error message."""
        print(status)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--delivery-stream-name",
        type=str,
        dest="delivery_stream_name",
        default="twitter_delivery_stream",
        help="name of kinesis firehose delivery stream",
    )
    parser.add_argument(
        "--local-csv-fpath",
        type=str,
        dest="local_csv_fpath",
        default="CSV_FILE_TWEETS_LOCAL.csv",
        help="name of CSV file to save tweets locally",
    )
    args = parser.parse_args()

    local_csv_fpath = args.local_csv_fpath
    delivery_stream_name = args.delivery_stream_name

    (
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_REGION,
        TWITTER_API_KEY,
        TWITTER_API_KEY_SECRET,
        TWITTER_ACCESS_TOKEN,
        TWITTER_ACCESS_TOKEN_SECRET,
    ) = load_env_vars()

    # create kinesis client connection
    session = boto3.Session()
    firehose_client = session.client("firehose", region_name=AWS_REGION)

    if delivery_stream_name:
        firehose_stream = firehose_client.describe_delivery_stream(
            DeliveryStreamName=delivery_stream_name,
        )

    args_dict = dict(
        track=[
            "jupiter",
            "saturn",
            "cassini",
            "neptune",
            "uranus",
            "pluto",
            "satellite",
            "space exploration",
            "space science",
            "james webb telescope",
            "hubble telescope",
            "james webb",
            "hubble",
            "telescope",
            "nasa",
            "national aeronautics and space administration",
            "jet propulsion lab",
            "jet propulsion laboratory",
            "goddard space flight center",
            "johnson space center",
            "kennedy space center",
            "ames research center",
            "armstrong flight research center",
            "glenn research center",
            "langley research center",
            "european space agency",
            "roscosmos",
            "dark matter",
            "stephen hawking",
            "mars exploration",
            "mars rover",
            "opportunity mars rover",
            "curiosity mars rover",
            "perseverance mars rover",
            "mars science laboratory",
            "insight mission",
            "insight lander",
            "deep space",
            "mars reconnaissance orbiter",
            "odyssey orbiter",
            "mars odyssey orbiter",
            "maven orbiter",
            "mars maven orbiter",
            "mars sample return",
            "exomars",
            "exoplanets",
            "mars 2020 perseverance rover",
            "curiosity rover",
            "spacex",
            "virgin galactic",
            "blue origin",
            "space shuttle",
            "shuttle",
            "space shuttle launch",
            "shuttle launch",
            "international space station",
            "space station",
            "astronomer",
            "astronomy",
            "astronaut",
            "astrophysics",
        ],
        languages=["en"],
        stall_warnings=True,
    )
    headers = [
        "id",
        "geo",
        "coordinates",
        "place",
        "contributors",
        "is_quote_status",
        "quote_count",
        "reply_count",
        "retweet_count",
        "favorite_count",
        "favorited",
        "retweeted",
        "created_at",
        "source",
        "in_reply_to_user_id",
        "in_reply_to_screen_name",
        "source_text",
        "place_id",
        "place_url",
        "place_place_type",
        "place_name",
        "place_full_name",
        "place_country_code",
        "place_country",
        "place_bounding_box_type",
        "place_bounding_box_coordinates",
        "place_attributes",
        "coords_type",
        "coords_lon",
        "coords_lat",
        "geo_type",
        "geo_lon",
        "geo_lat",
        "user_name",
        "user_screen_name",
        "user_followers",
        "user_friends",
        "user_listed",
        "user_favourites",
        "user_statuses",
        "user_protected",
        "user_verified",
        "user_contributors_enabled",
        "user_joined",
        "user_location",
        "text",
    ]

    if local_csv_fpath:
        if os.path.exists(local_csv_fpath):
            os.remove(local_csv_fpath)
            print(f"Found local file at {local_csv_fpath}. Deleted.")
        else:
            print(f"Did not find local file at {local_csv_fpath}.")
        append_list_to_local_csv(headers, local_csv_fpath)

    while True:
        try:
            local_time = datetime.datetime.now()
            print(
                "Twitter streaming started at "
                f"{local_time.strftime('%Y-%m-%d %H:%M:%S')}..."
            )
            # create instance of the tweet stream listener
            listener = TweetStreamListener(
                os.getenv("TWITTER_API_KEY"),
                os.getenv("TWITTER_API_KEY_SECRET"),
                os.getenv("TWITTER_ACCESS_TOKEN"),
                os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            )
            # search for twitter data
            listener.filter(**args_dict)
        except Exception as exc:
            print(exc)
            print("Disconnected.")
            time.sleep(5)
        continue

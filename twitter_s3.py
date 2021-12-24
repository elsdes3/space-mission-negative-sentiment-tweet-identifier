#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Stream Twitter data."""

# pylint: disable=invalid-name,broad-except,no-self-use


import datetime
import io
import json
import os
import sys
import time
from csv import writer
from typing import Dict, List

import boto3
from dotenv import find_dotenv, load_dotenv
from tweepy import Stream


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
    tweet_number = 1
    max_num_tweets_wanted = 20

    # Set kinesis data stream name
    filepath = "CSV_FILE_TWEETS_LOCAL.csv"
    # delivery_stream_name = "twitter_delivery_stream"
    delivery_stream_name = ""

    # on success
    def on_data(self, raw_data):
        """Retrieve tweet attributes."""
        tweet = json.loads(raw_data)
        max_tweets_wanted = TweetStreamListener.max_num_tweets_wanted
        if TweetStreamListener.tweet_number <= max_tweets_wanted:
            try:
                if "text" in tweet.keys():
                    attrs_to_get = TweetStreamListener.keys_wanted
                    tweet_text = (
                        tweet["text"].replace("\n", "").replace("\r", "")
                    )
                    # print(tweet["source"])
                    message_lst = [str(tweet[kw]) for kw in attrs_to_get]
                    source_text = (
                        tweet["source"].split('">')[-1].split("<")[0].strip()
                    )
                    place_list = get_place_list(tweet["place"])
                    coords_list = get_geo_coords_list(tweet, "coordinates")
                    geo_list = get_geo_coords_list(tweet, "geo")
                    user_list = [
                        str(tweet["user"]["name"]),
                        str(tweet["user"]["screen_name"]),
                        str(tweet["user"]["followers_count"]),
                        str(tweet["user"]["location"]),
                    ]
                    message_lst += (
                        [source_text]
                        + place_list
                        + coords_list
                        + geo_list
                        + user_list
                        + [tweet_text, "\n"]
                    )
                    print(
                        TweetStreamListener.tweet_number,
                        tweet["created_at"].split(" +")[0],
                        tweet_text[:75],
                    )
                    # Export data to local CSV
                    if append_to_local_csv:
                        append_list_to_local_csv(
                            message_lst[:-1], TweetStreamListener.filepath
                        )
                    message = "\t".join(message_lst)
                    # Export data to S3, using Kinesis firehose
                    stream_name = TweetStreamListener.delivery_stream_name
                    if stream_name:
                        firehose_client.put_record(
                            DeliveryStreamName=stream_name,
                            Record={"Data": message},
                        )
                    TweetStreamListener.tweet_number += 1
            except (AttributeError, Exception) as e:
                print(f"{TweetStreamListener.tweet_number} Error: {str(e)}")
            return True
        sys.exit()

    def on_error(self, status):
        """Show error message."""
        print(status)


if __name__ == "__main__":
    if os.path.exists("../.env"):
        load_dotenv(find_dotenv())

    # create kinesis client connection
    session = boto3.Session()
    firehose_client = session.client(
        "firehose", region_name=os.getenv("AWS_REGION")
    )

    # Options for saving tweets to local CSV file
    append_to_local_csv = False
    local_csv_fpath = "CSV_FILE_TWEETS_LOCAL.csv"

    args_dict = dict(
        track=[
            "english football",
            "premier league",
            "premierleague",
            "carabao cup",
            "efl cup",
            "football league cup",
            "english football league cup",
            "english football league",
            "english league cup",
            "league cup",
            "league cup football",
            "english football association cup",
            "english fa cup",
            "fa cup",
            "english football association challenge cup",
            "football association challenge cup",
            "fa challenge cup",
            "english fa challenge cup",
            "english premier league",
            "premier league football",
            "barclays premier league",
        ],
        languages=["en"],
        stall_warnings=True,
        # locations=[-6.38, 49.87, 1.77, 55.81],
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
        "user",
        "screen_name",
        "followers",
        "location",
        "text",
    ]

    if append_to_local_csv:
        if os.path.exists(local_csv_fpath):
            os.remove(local_csv_fpath)
            print(f"Found local file at {local_csv_fpath}. Deleted.")
        else:
            print(f"Did not find local file at {local_csv_fpath}.")
        append_list_to_local_csv(headers, local_csv_fpath)

    while True:
        try:
            local_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            print(f"Twitter streaming started at {local_time}...")
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

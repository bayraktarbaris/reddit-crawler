import datetime
import json
import logging
import time

import requests

from src.utils.config import Config
from src.utils.singleton import Singleton


class PushshiftApiClient(metaclass=Singleton):
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger("reddit-crawler")

    def get_submissions(self):
        submission_url = self.config.get("pushshift_search_base_url") + \
                         "/submission/?subreddit=tidal&fields=title,selftext,id,upvote_ratio,num_comments,link_flair_text,score,created_utc,author,author_fullname,retrieved_on&sort=desc&limit=1000&after=1d&before={}"

        objects = self.get_all_objects(submission_url)

        if len(objects) > 0:
            with open("../data/submissions.json", "w") as f:
                json.dump(objects, f)

            return True

        return False

    def get_comments(self):
        comments_url = self.config.get("pushshift_search_base_url") + \
                       "/comment/?subreddit=tidal&fields=body,id,score,author,author_fullname,parent_id,created_utc&sort=desc&limit=1000&after=1d&before={}"

        objects = self.get_all_objects(comments_url)

        if len(objects) > 0:
            with open("../data/comments.json", "w") as f:
                json.dump(objects, f)

            return True

        return False

    def get_all_objects(self, url):
        start_time = datetime.datetime.now(datetime.timezone.utc)
        previous_epoch = int(start_time.timestamp())
        objects = []
        while True:
            new_url = url.format(previous_epoch)

            resp = requests.get(new_url, headers={'User-Agent': "Submission and comment downloader by Baris Bayraktar"})
            # Pushshift has a rate limit, if we send requests too fast it will write returning error messages
            time.sleep(1)

            if resp.status_code != 200:
                message = "Failed while getting objects"
                self.logger.error(message)
                break

            try:
                json_data = resp.json()
            except json.decoder.JSONDecodeError:
                time.sleep(1)
                continue

            if 'data' not in json_data:
                break

            data = json_data['data']
            if len(data) == 0:
                break

            previous_epoch = data[-1]['created_utc'] - 1

            objects.extend(data)

        return objects

import logging
import sys

from src.clients.pushshift_api import PushshiftApiClient
from src.services.comment_service import CommentService
from src.services.submission_service import SubmissionService
from src.utils.config import Config

app_name = 'reddit-crawler'


def _register_logger():
    _logger = logging.getLogger(app_name)
    _logger.setLevel(logging.INFO)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    _logger.addHandler(ch)


_register_logger()
logger = logging.getLogger(app_name)


def main():
    config = Config()
    run_mode = config.get("run_mode")

    comment_service = CommentService()
    submission_service = SubmissionService()

    if run_mode == "WRITE":
        pushshift_api_client = PushshiftApiClient()
        success_comments = pushshift_api_client.get_comments()
        success_submissions = pushshift_api_client.get_submissions()

        if success_comments:
            comment_service.write()

        if success_submissions:
            submission_service.write()
    elif run_mode == "READ":
        comment_service.read()
        submission_service.read()


if __name__ == '__main__':
    main()

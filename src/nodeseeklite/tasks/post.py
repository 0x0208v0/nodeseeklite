from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def crawl_post():
    logger.info(f'crawl_post start!')

    from nodeseeklite.app import app
    from nodeseeklite.models.post import Post

    with app.app_context():
        Post.crawl()

    logger.info(f'crawl_post done!')


if __name__ == '__main__':
    logger.info = print
    crawl_post()

import logging

logger = logging.getLogger(__name__)


def crawl_post():
    logger.info(f'crawl_post start!')
    try:

        from nodeseeklite.app import app
        from nodeseeklite.models import db
        from nodeseeklite.models.post import Post

        with app.app_context():
            Post.crawl()
            db.session.close_all()

    except Exception as e:
        logger.error(f'{e}')

    logger.info(f'crawl_post done!')


if __name__ == '__main__':
    logger.info = print
    crawl_post()

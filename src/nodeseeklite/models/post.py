import uuid
from datetime import datetime
from datetime import timedelta
from typing import Self

import arrow
import feedparser
import pendulum
import requests
from sqlalchemy import DateTime
from sqlalchemy import Index
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from nodeseeklite.models.base import BaseModel

TAG_ZH_MAP = {
    'daily': '日常',
    'tech': '技术',
    'info': '情报',
    'review': '测评',
    'trade': '交易',
    'expose': '曝光',
    'carpool': '拼车',
    'life': '生活',
    'photo-share': '贴图',
    'promotion': '推广',
    'inside': '内版',
    'dev': 'Dev',
    'meaningless': '无意义',
    'sandbox': '沙盒',
}


def make_tag_url(tag: str):
    return f'https://www.nodeseek.com/categories/{tag}'


def time_ago(dt) -> str:
    now = datetime.utcnow()
    time_difference = now - dt

    days = time_difference.days
    seconds = time_difference.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if days > 0:
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif hours > 0:
        return f"{hours}h {minutes}min ago" if minutes > 0 else f"{hours}h ago"
    elif minutes > 0:
        return f"{minutes}min ago"
    else:
        return f"{seconds}s ago"


class Post(BaseModel):
    url: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
        index=True,
    )
    author: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    tag: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )
    summary: Mapped[uuid.UUID] = mapped_column(
        Text,
        nullable=False,
    )
    published_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
        index=True,
    )
    __table_args__ = (
        Index('idx_event_date_desc', published_at.desc()),
    )

    @property
    def display_time_ago(self) -> str:
        return time_ago(self.published_at)

    @property
    def display_time(self) -> str:
        return (self.published_at + timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def tag_url(self) -> str:
        return make_tag_url(self.tag)

    @property
    def tag_zh(self) -> str:
        return TAG_ZH_MAP.get(self.tag, '未知')

    @classmethod
    def fetch_post_list(cls) -> list[Self]:
        post_list = []

        url = 'https://rss.nodeseek.com'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:95.0) Gecko/20100101 Firefox/95.0'}
        response = requests.get(url, headers=headers, timeout=(5, 6))

        result = feedparser.parse(response.content)
        for entry in result['entries']:
            post = cls(
                url=entry['link'],
                author=entry['author'],
                title=entry['title'],
                tag=', '.join([tag['term'] for tag in entry['tags']]),
                summary=entry.get('summary', ''),  # 有权限的帖子可能没有summary
                published_at=(
                    arrow
                    .get(
                        pendulum.parse(entry['published'], strict=False).strftime('%Y-%m-%d %H:%M:%S'),
                        tzinfo='GMT'
                    )
                    .datetime
                ),
            )
            post_list.append(post)
        return post_list

    @classmethod
    def crawl(cls):
        post_list = cls.fetch_post_list()
        for post in post_list:
            if not cls.count(cls.url == post.url):
                post.save()

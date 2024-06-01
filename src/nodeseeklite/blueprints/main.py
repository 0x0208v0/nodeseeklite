from datetime import datetime
from datetime import timedelta

from flask import Blueprint
from flask import jsonify
from flask import render_template

from nodeseeklite.models.post import Post

blueprint = Blueprint('main', __name__, url_prefix='/')


@blueprint.get('/health')
def health():
    return 'ok'


@blueprint.get('/')
def index():
    post_list = Post.get_list(
        Post.published_at > (datetime.now() - timedelta(hours=12)),
        order_by=[Post.published_at.desc()],
    )
    return render_template(
        'main/index.html',
        post_list=post_list,
    )


@blueprint.get('/api')
def api():
    post_list = Post.get_list(
        order_by=[Post.published_at.desc()],
        limit=20,
    )
    result = [
        {
            '链接': post.url,
            '频道': post.tag_zh,
            '标题': post.title,
            '作者': post.author,
            '内容摘要': post.summary,
            '发布时间': post.display_time
        }
        for post in post_list
    ]

    return jsonify(result)

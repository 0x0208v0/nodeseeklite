from nodeseeklite.app import app


def create_test_data():
    from nodeseeklite.tasks.post import crawl_post

    crawl_post()


if __name__ == '__main__':
    # 如果需要测试数据，可以解除 create_test_data() 注释
    create_test_data()
    app.run(debug=True, threaded=False, host='localhost', port=15100)

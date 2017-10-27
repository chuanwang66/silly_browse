"""
    线程池 + requests 实现 “异步”!
    参考资料: https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example (线程池)
    参考资料: https://stackoverflow.com/questions/14245989/python-requests-non-blocking
"""

import concurrent.futures
import urllib.request

URLS = ["https://github.com/chuanwang66/silly_player_x",
    "https://github.com/chuanwang66/silly_browse",
    "https://github.com/chuanwang66/easerpc_x",
    "https://github.com/chuanwang66/kcp",
    "https://github.com/chuanwang66/test_opencv",
    "https://github.com/chuanwang66/C-Thread-Pool",
    "https://github.com/chuanwang66/ngx_stream_upstream_check_module",
    "https://github.com/chuanwang66/AsyncNet",
    "https://github.com/chuanwang66/Spider",
    "https://github.com/chuanwang66/AudioStreaming",
    "https://github3.com/chuanwang66/fake"]

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    
    print('here')
    import time
    time.sleep(10)  #不用等待IO，你放心去做其他的事情!
    print('here2')

    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
#-*- coding:utf8 -*-
"""
    线程池 + requests 实现 “异步”!
    参考资料: https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example (线程池)
    参考资料: https://stackoverflow.com/questions/14245989/python-requests-non-blocking
"""
import requests
import concurrent.futures

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

def requests_get_url(url, cookies={}, max_retries=3, verbose=False):
    r = None

    num_retries = 0
    while num_retries <= max_retries:
        try:
            r = requests.get(url, cookies=cookies, timeout=10.000)
            break
        except requests.exceptions.ConnectTimeout:
            if verbose: print('connect timeout')
            num_retries += 1
        except requests.exceptions.ConnectionError:
            if verbose: print('connect error')
            num_retries += 1
        except requests.exceptions.Timeout:
            if verbose: print('timeout')
            num_retries += 1
        except requests.exceptions.TooManyRedirects:
            if verbose: print('too many redirects')
            num_retries += 1
        except requests.exceptions.RequestException as e:
            if verbose: print(e)
            num_retries += 1
        if verbose: print('retry: %d'%(num_retries))
    return r

def test1():
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(requests_get_url, url):url for url in URLS}
        futures = set(future_to_url)

        """
        concurrent.futures.as_completed(fs, timeout=None):
            An iterator over the given futures that yields each as it completes.

            Args:
                fs: The sequence of Futures (possibly created by different Executors) to iterate over.
                timeout: The maximum number of seconds to wait. If None, then there is no limit on the wait time.

            Returns:
                An iterator that yields the given Futures as they complete (finished or cancelled).
                If any given Futures are duplicated, they will be returned once.

            Raises:
                TimeoutError: If the entire result iterator could not be generated before the given timeout.

        """
        for future in concurrent.futures.as_completed(futures):
            try:
                r = future.result()
                url = future_to_url[future]
                if r:
                    print('%r page is %d bytes' % (url, len(r.content)))
                else:
                    print('%r page is null'%(url))
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))

def requests_get_url2(url, cookies={}, max_retries=3, verbose=False):
    r = None

    num_retries = 0
    while num_retries <= max_retries:
        try:
            r = requests.get(url, cookies=cookies, timeout=10.000)
            break
        except requests.exceptions.ConnectTimeout:
            if verbose: print('connect timeout')
            num_retries += 1
        except requests.exceptions.ConnectionError:
            if verbose: print('connect error')
            num_retries += 1
        except requests.exceptions.Timeout:
            if verbose: print('timeout')
            num_retries += 1
        except requests.exceptions.TooManyRedirects:
            if verbose: print('too many redirects')
            num_retries += 1
        except requests.exceptions.RequestException as e:
            if verbose: print(e)
            num_retries += 1
        if verbose: print('retry: %d'%(num_retries))
    return url, r

def on_response(future):
    try:
        url, r = future.result()
        if r:
            print('%r page is %d bytes' % (url, len(r.content)))
        else:
            print('%r page is null'%(url))
    except Exception as exc:
        print('%r generated an exception: %s' % (url, exc))

def test2():
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(requests_get_url2, url):url for url in URLS}
        futures = set(future_to_url)

        """
        concurrent.futures.as_completed(fs, timeout=None):
            An iterator over the given futures that yields each as it completes.

            Args:
                fs: The sequence of Futures (possibly created by different Executors) to iterate over.
                timeout: The maximum number of seconds to wait. If None, then there is no limit on the wait time.

            Returns:
                An iterator that yields the given Futures as they complete (finished or cancelled).
                If any given Futures are duplicated, they will be returned once.

            Raises:
                TimeoutError: If the entire result iterator could not be generated before the given timeout.

        """
        for future in future_to_url.keys():
            future.add_done_callback(on_response)


if __name__ == "__main__":
    #多线程执行， concurrent.futures.as_completed等待依次返回
    test1()

    #多线程执行，future.add_done_callback(on_response)注册异步回调，完全木有等待操作
    #test2()
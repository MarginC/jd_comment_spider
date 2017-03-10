# -*- coding: utf-8 -*-
import requests
import redis
import json

if __name__ == "__main__":
    import settings


def proxy_test(proxy):
    try:
        proxyDict = {'http': proxy}
        r = requests.post('http://example.org/',
            proxies=proxyDict, timeout=2)
        if r.status_code == 200:
            return True, r.elapsed.microseconds
        else:
            return False, 0
    except Exception as e:
        print(e)
        return False, 0
    pass


if __name__ == "__main__":
    proxy_list = open(settings.REDIS_PROXY_LIST_KEY, 'w')
    proxy_valid_list = open(settings.REDIS_PROXY_VALID_LIST_KEY, 'w')
    r = redis.Redis(host=settings.REDIS_IP, port=settings.REDIS_PORT)
    for proxy in r.smembers(settings.REDIS_PROXY_LIST_KEY):
        _json = json.loads(proxy)
        proxy_list.write('http://{0}:{1}\n'.
            format(_json['ipAddress'], _json['port']))
    for proxy in r.smembers(settings.REDIS_PROXY_LIST_KEY):
        _json = json.loads(proxy)
        valid, elapsed = proxy_test('{0}:{1}'.
            format(_json['ipAddress'], _json['port']))
        if valid:
            r.zadd(settings.REDIS_PROXY_VALID_LIST_KEY, proxy, elapsed)
            proxy_valid_list.write('http://{0}:{1}\n'.
                format(_json['ipAddress'], _json['port']))

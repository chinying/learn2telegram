# so apparently we need these 4 lines to prevent some "Max recursion depth error" from grequests
# see more at https://github.com/kennethreitz/grequests/issues/103 and https://github.com/gevent/gevent/issues/903
from gevent import monkey
def stub(*args, **kwargs):  # pylint: disable=unused-argument
    pass
monkey.patch_all = stub

def exception_handler(request, exception):
    print("Request failed")
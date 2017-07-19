from gevent import monkey
def stub(*args, **kwargs):  # pylint: disable=unused-argument
    pass
monkey.patch_all = stub

def exception_handler(request, exception):
    print("Request failed")
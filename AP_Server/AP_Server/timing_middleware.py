import time


class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        time_use_ms = (end_time - start_time) * 1000
        print(f"[Test]: 到{request.path}的请求耗时{time_use_ms:.2f}毫秒")

        return response

from concurrent.futures import ThreadPoolExecutor, wait

__author__ = '高一航'


class Pool(object):
    # 线程池
    def __init__(self, **params):
        # 线程数量
        self.max_workers = params['max_workers']
        # 线程池生成
        self.thread_pool = ThreadPoolExecutor(max_workers=self.max_workers)
        # 线程序列
        self.all_task = []

    def add_method(self, **params):
        # 线程方法添加
        task = self.thread_pool.submit(params['method'], **params)
        self.all_task.append(task)

    def wait(self):
        # 等待子线程结束
        wait(self.all_task)

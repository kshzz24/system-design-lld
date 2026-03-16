from concurrent.futures import ThreadPoolExecutor

class AsyncLogProcessor:
    
    def __init__(self, max_workers:int=4):
        self.executor = ThreadPoolExecutor(max_workers)
    def process(self, msg, appenders):
        def task():
            for appender in appenders:
                appender.append(msg)

        self.executor.submit(task)

    def stop(self):
    
        self.executor.shutdown(wait=True)
    

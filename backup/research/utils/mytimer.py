import time
 
# defining the class
class Timer:
        
    def __init__(self, func = time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None
    
    # starting the module
    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()
    
    # stopping the timer
    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None
    
    # resetting the timer
    def reset(self):
        self.elapsed = 0.0
    
    @property
    def running(self):
        if self._start:
            return self._start
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, *args):
        self.stop()
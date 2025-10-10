import threading
import time
from collections import deque
from log_manager import bot_logger

class MetricsCollector:
    def __init__(self, interval=10, window_size=300):
        self.interval = interval
        self.window_size = window_size
        self.requests_times = deque()
        self.active_users = {}
        self.latency_history = deque(maxlen=100)
        self.stop_event = threading.Event()

    def add_request_time(self, timestamp):
        self.requests_times.append(timestamp)

    def add_active_user(self, user_id, timestamp):
        self.active_users[user_id] = timestamp

    def add_latency(self, latency):
        self.latency_history.append(latency)

    def get_rps(self):
        now = time.time()
        while self.requests_times and self.requests_times[0] < now - 1:
            self.requests_times.popleft()
        return len(self.requests_times)
    
    def get_active_users_count(self):
        now = time.time()
        self.active_users = {
            uid: last_time 
            for uid, last_time in self.active_users.items()
            if now - last_time < self.window_size
        }
        return len(self.active_users)
    
    def get_avg_latency(self):
        if not self.latency_history:
            return 0
        return sum(self.latency_history) / len(self.latency_history)
    
    def collect_metrics(self):
        while not self.stop_event.wait(self.interval):
            rps = self.get_rps()
            active_users = self.get_active_users_count()
            avg_latency = self.get_avg_latency()

            bot_logger.log_metric("rps", rps, {"interval": "1s"})
            bot_logger.log_metric("active_users", active_users, {"window": f"{self.window_size}s"})
            bot_logger.log_metric("avg_latency", avg_latency, {"period": "last_100_requests"})

    def start(self):
        thread = threading.Thread(target=self.collect_metrics, daemon=True)
        thread.start()

    def stop(self):
        self.stop_event.set()
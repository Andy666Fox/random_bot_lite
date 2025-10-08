from datetime import datetime
from collections import defaultdict, deque
import time 

from aiohttp import web
import base64
import os

class MetricsServer:
    def __init__(self):
        self.requests_count = 0
        self.db_queries_count = 0
        self.active_users = set()
        self.user_requests = defaultdict(int)
        self.requests_history = deque()
        self.db_queries_history = deque()

        self.bot_status = "healthy"
        self.last_update_time = time.time()

        self.window_size = 60

    def record_request(self, user_id: str):
        current_time = time.time()

        self.requests_history.append(current_time)
        self.requests_count += 1
        self.active_users.add(user_id)
        self.user_requests[user_id] += 1

        self.last_update_time = current_time

        self._cleanup_old_records(self.requests_history)

    def record_db_query(self):
        current_time = time.time()
        self.db_queries_history.append(current_time)
        self.db_queries_count += 1

        self._cleanup_old_records(self.db_queries_history)

    def update_bot_status(self, status: str):
        self.bot_status = status
        self.last_update_time = time.time()

    def get_rps(self) -> float:
        current_time = time.time()
        recent_requests = [
            t for t in self.requests_history
            if current_time - t <= 60
        ]

        return len(recent_requests) / 60.0 if len(recent_requests) > 0 else 0.0
    
    def get_active_users_count(self) -> int:
        current_time = time.time()
        self.active_users = {
            user for user in self.active_users
            if current_time - getattr(self, f'_last_seen_{user}', current_time) <= 300
        }
        return len(self.active_users)
    
    def get_total_requests(self) -> int:
        return self.requests_count
    
    def get_total_db_queries(self) -> int:
        return self.db_queries_count
    
    def get_user_stats(self) -> dict:
        return dict(self.user_requests)
    
    def get_bot_status(self) -> str:
        current_time = time.time()
        if current_time - self.last_update_time > 300:
            return "unhealthy"
        return self.bot_status
    
    def _cleanup_old_records(self, history_deque):
        current_time = time.time()
        while history_deque and current_time - history_deque[0] > self.window_size:
            history_deque.popleft()

metrics = MetricsServer()

def check_auth(credentials: str) -> bool:
    username = os.getenv("METRICS_USERNAME")
    password = os.getenv("METRICS_PASSWORD")

    try:
        decoded = base64.b64decode(credentials).decode('utf-8')
        provided_username, provided_password = decoded.split(':', 1)
        return provided_username == username and provided_password == password
    except:
        return False

def require_auth(handler):
    async def wrapped(request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Basic '):
            return web.Response(
                status=401,
                text='Unauthorized loshara',
                headers={'WWW-Authenticate': 'Basic realm="Metrics"'}
            )
        
        credentials = auth_header[6:]

        if not check_auth(credentials):
            return web.Response(
                status=401,
                text='Unauthorized loshara',
                headers={'WWW-Authenticate': 'Basic realm="Metrics"'}
            )
        
        return await handler(request)
    
    return wrapped

@require_auth
async def metrics_handler(request):
    data = {
        'timestamp': datetime.now().isoformat(),
        'bot_status': metrics.get_bot_status(),
        'rps': metrics.get_rps(),
        'active_users': metrics.get_active_users_count(),
        'total_requests': metrics.get_total_requests(),
        'total_db_queries': metrics.get_total_db_queries(),
        'user_stats': metrics.get_user_stats()
    }
    return web.json_response(data)

def setup_metrics_server(port: int = os.getenv("METRICS_PORT")):
    app = web.Application()
    app.router.add_get('/metrics', metrics_handler)

    return app, port 

async def run_metrics_server():
    app, port = setup_metrics_server()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f'Metrics server started on port {port}')
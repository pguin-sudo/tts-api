import os

THREADS = int(os.environ.get("threads", 16))
API_TOKEN = os.environ.get("apitoken", "test123123123")
CPU_USAGE_THRESHOLD = int(os.environ.get("cpu_usage_threshold", 20))

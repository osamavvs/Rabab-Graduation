from locust import HttpUser, task, between
import random

class DefensiveLoadTest(HttpUser):
    wait_time = between(0.5, 1.5)  # زمن بين الطلبات
    
    @task(3)  # وزن 3
    def normal_request(self):
        """محاكاة طلب عادي"""
        self.client.get("/", name="Homepage")
    
    @task(2)
    def heavy_request(self):
        """طلب يستهلك موارد (محاكاة هجوم طبقة التطبيق)"""
        self.client.get("/search?q=" + "x"*1000, name="Heavy Search")
    
    @task(1)
    def slow_request(self):
        """محاكاة Slowloris (اتصال بطيء)"""
        headers = {"User-Agent": "Mozilla/5.0 (Test Bot)"}
        self.client.get("/", headers=headers, timeout=1)

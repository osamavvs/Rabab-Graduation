from locust import HttpUser, task, between
import random

class DefensiveLoadTest(HttpUser):
    wait_time = between(0.5, 1.5)
    
    @task(3)
    def normal_request(self):
        """طلب عادي"""
        self.client.get("/", name="Homepage")
    
    @task(2)
    def heavy_request(self):
        """طلب ثقيل (محاكاة هجوم طبقة التطبيق)"""
        self.client.get(f"/search?q={'x'*500}", name="Search Heavy")
    
    @task(1)
    def slow_request(self):
        """محاكاة Slowloris (اتصال بطيء)"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Educational Test)",
            "Accept": "text/html,application/xhtml+xml"
        }
        self.client.get("/", headers=headers, timeout=2)
    
    def on_start(self):
        """يُسمى عند بداية كل مستخدم"""
        self.client.get("/", name="Initial Connection")

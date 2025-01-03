from locust import FastHttpUser, task


class DjangoSyncOrAsync(FastHttpUser):
    @task
    def index(self):
        self.client.get("/")

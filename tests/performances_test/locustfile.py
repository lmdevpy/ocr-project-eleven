from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 2)  # Time between requests in seconds

    def on_start(self):
        # login page
        self.client.get("/")

    @task
    def displayPointsBoard(self):
        self.client.get("/displayPointsBoard")

    @task
    def show_summary(self):
        # Simulate the user checking the summary
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def book_competition(self):
        # Simulate the user booking places
        self.client.get("/book/Paris%20World/Simply%20Lift")

    @task
    def purchase_places(self):
        # Simulate the user purchasing places
        data = {"competition": "Paris World", "club": "Simply Lift", "places": 5}
        self.client.post("/purchasePlaces/", data=data)

    def on_stop(self):
        # logout user
        self.client.get("/logout")

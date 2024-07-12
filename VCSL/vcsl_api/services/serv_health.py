from kink import inject


@inject
class HealthCheckService:

    def __init__(self):
        self.message = "I'm healthy"

    def is_healthy(self) -> str:
        return self.message

from fastapi import APIRouter
from kink import inject
from services.serv_health import HealthCheckService


@inject
class HealthCheckRouter:
    def __init__(self, health_check_service: HealthCheckService):
        self.health_check_service: HealthCheckService = health_check_service
        self.router = APIRouter()
        self.router.add_api_route(
            path="/health-check", endpoint=self.health_check, methods=["GET"]
        )

    async def health_check(self):
        return {"message": self.health_check_service.is_healthy()}

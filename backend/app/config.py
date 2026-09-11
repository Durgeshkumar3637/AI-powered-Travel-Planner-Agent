"""Application configuration loaded from environment variables."""
import os


class Settings:
    def __init__(self):
        self.demo_mode = os.getenv("DEMO_MODE", "true").strip().lower() in ("true", "1", "yes")
        self.ibm_cloud_api_key = os.getenv("IBM_CLOUD_API_KEY", "").strip()
        self.watsonx_project_id = os.getenv("WATSONX_PROJECT_ID", "").strip()
        self.watsonx_url = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com").strip().rstrip("/")
        self.granite_model_id = os.getenv("GRANITE_MODEL_ID", "ibm/granite-3-3-8b-instruct").strip()
        self.weather_api_key = os.getenv("WEATHER_API_KEY", "").strip()
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").strip()

    @property
    def granite_configured(self) -> bool:
        return bool(self.ibm_cloud_api_key and self.watsonx_project_id)

    @property
    def weather_configured(self) -> bool:
        return bool(self.weather_api_key)


settings = Settings()

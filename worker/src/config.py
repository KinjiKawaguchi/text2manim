import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        # サーバー設定
        self.worker_port: int = int(os.getenv("WORKER_PORT", "50052"))

        # ストレージ設定
        self.storage_type: str = os.getenv("STORAGE_TYPE", "local")
        self.local_storage_path: str = os.getenv(
            "LOCAL_STORAGE_PATH", "/tmp/text2manim"
        )

        # クラウドストレージ設定 (GCP を例として)
        self.gcp_bucket_name: str = os.getenv("GCP_BUCKET_NAME", "")
        self.gcp_credentials_path: str = os.getenv("GCP_CREDENTIALS_PATH", "")

        # OpenAI APIを使用する場合の設定
        # OpenAIのモデルを使うかどうか
        self.use_openai: bool = os.getenv("USE_OPENAI", "false").lower() == "true"
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.openai_max_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        self.openai_temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        self.openai_top_p: float = float(os.getenv("OPENAI_TOP_P", "0.95"))

        # モデル設定
        self.model_name: str = os.getenv("MODEL_NAME", "your-username/your-model-name")
        self.model_max_length: int = int(os.getenv("MODEL_MAX_LENGTH", "1000"))
        self.model_temperature: float = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
        self.model_top_k: int = int(os.getenv("MODEL_TOP_K", "50"))
        self.model_top_p: float = float(os.getenv("MODEL_TOP_P", "0.95"))

        # Manim 設定
        self.manim_quality: str = os.getenv("MANIM_QUALITY", "medium_quality")
        self.manim_output_file: str = os.getenv("MANIM_OUTPUT_FILE", "scene.mp4")

        # ロギング設定
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
        self.log_file: str = os.getenv("LOG_FILE", "")

        self.validate()
        print(self.__str__())

    def validate(self):
        if self.storage_type not in ["local", "gcp"]:
            raise ValueError(f"Invalid storage type: {self.storage_type}")

        if self.storage_type == "gcp" and (
            not self.gcp_bucket_name or not self.gcp_credentials_path
        ):
            raise ValueError(
                "GCP storage selected but bucket name or credentials path is missing"
            )

        if self.manim_quality not in [
            "low_quality",
            "medium_quality",
            "high_quality",
            "production_quality",
        ]:
            raise ValueError(f"Invalid Manim quality: {self.manim_quality}")

        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"Invalid log level: {self.log_level}")

    def __str__(self):
        return f"""
        Worker Configuration:
        ---------------------
        Worker Port: {self.worker_port}
        Storage Type: {self.storage_type}
        Local Storage Path: {self.local_storage_path}
        GCP Bucket Name: {self.gcp_bucket_name}
        GCP Credentials Path: {self.gcp_credentials_path}
        Use OpenAI: {self.use_openai}
        OpenAI API Key: {self.openai_api_key}
        OpenAI Model: {self.openai_model}
        OpenAI Max Tokens: {self.openai_max_tokens}
        OpenAI Temperature: {self.openai_temperature}
        OpenAI Top P: {self.openai_top_p}
        Model Name: {self.model_name}
        Model Max Length: {self.model_max_length}
        Model Temperature: {self.model_temperature}
        Model Top K: {self.model_top_k}
        Model Top P: {self.model_top_p}
        Manim Quality: {self.manim_quality}
        Manim Output File: {self.manim_output_file}
        Log Level: {self.log_level}
        Log File: {self.log_file}
        """


# 使用例
if __name__ == "__main__":
    config = Config()
    print(config)

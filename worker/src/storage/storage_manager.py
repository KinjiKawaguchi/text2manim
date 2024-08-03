from storage.local_storage import LocalStorage
from storage.cloud_storage.gcp import GCPStorage


class StorageManager:
    @staticmethod
    def get_storage(config):
        if config.storage_type == "local":
            return LocalStorage(config)
        elif config.storage_type == "gcp":
            return GCPStorage(config)
        else:
            raise ValueError(f"Unsupported storage type: {
                             config.storage_type}")

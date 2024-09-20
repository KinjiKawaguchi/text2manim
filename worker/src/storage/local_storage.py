import os
import shutil

class LocalStorage:
    def __init__(self, config):
        self.storage_path = config.local_storage_path

    def upload_video(self, video_path, task_id):
        destination = os.path.join(self.storage_path, f"{task_id}.mp4")
        shutil.copy(video_path, destination)
        return f"file://{destination}"

    def upload_script(self, script, task_id):
        script_path = os.path.join(self.storage_path, f"{task_id}.py")
        with open(script_path, 'w') as f:
            f.write(script)
        return f"file://{script_path}"
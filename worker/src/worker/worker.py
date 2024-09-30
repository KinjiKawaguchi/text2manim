from src.generated.proto.text2manim.v1 import worker_pb2, worker_pb2_grpc
from src.models.text2manim_model import Text2ManimModel
from src.storage.storage_manager import StorageManager
import grpc
import logging


class WorkerServicer(worker_pb2_grpc.WorkerServiceServicer):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.model = Text2ManimModel(config)
        self.storage = StorageManager.get_storage(config)

    def GenerateManimScript(self, request, context):
        self.logger.info(f"Generating Manim script for task {request.task_id}")
        try:
            script = self.model.generate_script(request.prompt)
            script_url = self.storage.upload_script(script, request.task_id)
            self.logger.info(f"Script generated and saved for task {request.task_id}")
            return worker_pb2.GenerateManimScriptResponse(
                task_id=request.task_id, script=script, script_url=script_url
            )
        except Exception as e:
            self.logger.error(
                f"Error generating script for task {request.task_id}: {str(e)}"
            )
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error generating script: {str(e)}")
            return worker_pb2.GenerateManimScriptResponse()

    def GenerateManimVideo(self, request, context):
        self.logger.info(f"Generating Manim video for task {request.task_id}")
        try:
            video_path = self.model.generate_video(request.script)
            video_url = self.storage.upload_video(video_path, request.task_id)
            script_url = self.storage.upload_script(request.script, request.task_id)
            self.logger.info(f"Video generated and saved for task {request.task_id}")
            return worker_pb2.GenerateManimVideoResponse(
                task_id=request.task_id,
                success=True,
                video_url=video_url,
                script_url=script_url,
            )
        except Exception as e:
            self.logger.error(
                f"Error generating video for task {request.task_id}: {str(e)}"
            )
            return worker_pb2.GenerateManimVideoResponse(
                task_id=request.task_id, success=False, error_message=str(e)
            )

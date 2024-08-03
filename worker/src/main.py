import grpc
from concurrent import futures
import logging
from generated.proto.text2manim.v1 import worker_pb2_grpc
from worker.worker import WorkerServicer
from config import Config
from utils.logger import setup_logger


def serve():
    config = Config()
    logger = setup_logger()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    worker_pb2_grpc.add_WorkerServiceServicer_to_server(
        WorkerServicer(config, logger), server)
    server.add_insecure_port(f'[::]:{config.worker_port}')
    server.start()
    logger.info(f"Worker server started on port {config.worker_port}")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()

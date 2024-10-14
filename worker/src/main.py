import grpc
from concurrent import futures
import signal
import sys
from generated.proto.text2manim.v1 import worker_pb2_grpc
from worker.worker import WorkerServicer
from config import Config
from utils.logger import setup_logger


def serve():
    logger = setup_logger()
    config = Config()
    logger.info(config.__str__())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    worker_pb2_grpc.add_WorkerServiceServicer_to_server(
        WorkerServicer(config, logger), server
    )
    server.add_insecure_port(f"[::]:{config.worker_port}")

    def graceful_shutdown(signum, frame):
        logger.info("Received shutdown signal. Stopping server...")
        all_rpcs_done_event = server.stop(30)
        all_rpcs_done_event.wait(30)
        logger.info("Server stopped gracefully")
        sys.exit(0)

    signal.signal(signal.SIGTERM, graceful_shutdown)
    signal.signal(signal.SIGINT, graceful_shutdown)

    server.start()
    logger.info(f"Worker server started on port {config.worker_port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

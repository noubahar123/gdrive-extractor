import os
from redis import Redis
from rq import Queue
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def get_queue() -> Queue:
    connection = Redis.from_url(REDIS_URL)
    return Queue("imports", connection=connection)


def enqueue_google_drive_import(folder_id: str) -> str:
    """
    Enqueue a folder import job to Redis/RQ.
    The actual function lives in worker-service: app.tasks.process_google_drive_folder
    """
    q = get_queue()
    job = q.enqueue("app.tasks.process_google_drive_folder", folder_id)
    return job.id

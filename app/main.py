import logging
from route_log_filter import RouteLogFilter
from settings import Settings
from json_classes import Root
from fastapi import FastAPI, BackgroundTasks
from email_handler import EmailHandler
from csv_handler import CSVHandler

email_handler = EmailHandler()
csv_handler = CSVHandler()
settings = Settings()  # pyright: ignore[reportCallIssue]
logging.basicConfig(level=logging.INFO)
logging.getLogger("uvicorn.access").addFilter(RouteLogFilter())
logger = logging.getLogger(__name__)
if settings.production is False:
    app = FastAPI()
else:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.post("/api")
def capture_message(root: Root, background_tasks: BackgroundTasks):
    if root.data.event_type == "message.received":
        to_phone_number = root.data.payload.to[0].phone_number
        from_phone_number = root.data.payload.from_.phone_number
        text = root.data.payload.text
        occurred_at = root.data.occurred_at

        csv_handler.record_message_to_file(from_phone_number, to_phone_number, text, occurred_at)

        email_address = csv_handler.match_phone_number(to_phone_number)

        if email_address == 0:
            logger.info(f"No email address for addressee {to_phone_number}")
        else:
            background_tasks.add_task(
                email_handler.build_message, from_address=from_phone_number, to_address=email_address, message_text=text
            )
            logging.info(occurred_at)


@app.get("/health")
def health_check():
    return {"status": "healthy"}

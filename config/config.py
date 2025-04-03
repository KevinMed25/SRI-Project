import logging

class NoFlaskFilter(logging.Filter):
    def filter(self, record):
        # Descartar mensajes de log que provengan de Flask o Werkzeug
        return not (record.name.startswith("werkzeug") or record.name.startswith("flask"))

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

for handler in logging.getLogger().handlers:
    if isinstance(handler, logging.FileHandler):
        handler.addFilter(NoFlaskFilter())
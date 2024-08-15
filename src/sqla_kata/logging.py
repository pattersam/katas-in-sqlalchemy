import logging

import rich.highlighter
import rich.logging

logging.basicConfig(
    level=logging.INFO,
    format="ℹ️  %(message)s",
    datefmt="[%X]",
    handlers=[rich.logging.RichHandler(rich_tracebacks=True)],
)


LOGGER = logging.LoggerAdapter(logging.getLogger(), extra={"markup": True})


class _SimpleSqlHighlighter(rich.highlighter.RegexHighlighter):
    """Apply some SQL styling."""

    base_style = ""
    highlights = [
        r"(?P<blue>\b\w*[A-Z]\w*\b)",  # highlights upper case SQL keywords in blue
    ]


def configure_sqla_engine_logging():
    """Configures the SQLAlchemy Engine logger to be more readable in the console."""
    handler = rich.logging.RichHandler(highlighter=_SimpleSqlHighlighter())
    handler.setFormatter(logging.Formatter("🧙 %(message)s", datefmt="[%X]"))
    engine_logger = logging.getLogger("sqlalchemy.engine.Engine")
    engine_logger.propagate = False
    engine_logger.addHandler(handler)

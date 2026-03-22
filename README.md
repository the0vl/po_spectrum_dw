# po_spectrum_dw
A data project on public opinion and rhetoric from different political stances, meant to serve in understanding public opinion regarding independent &amp; concurrent political issues.

#Logger
New files should start like this:
//
from src.utils.logger import get_logger
# Use the filename as the logger name for easy debugging
logger = get_logger(__name__) 

def my_function():
    logger.info("Doing something cool...")
//
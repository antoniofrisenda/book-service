from loguru import logger
import sys
import os

def setup_loguru_logger():
    
    logger.remove()
                   
    
    log_level = os.getenv("LOG_LEVEL", "INFO")  
    logger.add(sys.stdout, level=log_level)
    
    
    logger.add(
    "logs/book-service.log",  
    rotation="10 MB",         
    retention="1 days",       
    level="DEBUG"             
)
    
    
    logger.info("Loguru has been configurated successfully!")
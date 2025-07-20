# Logging utility for wdrive
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logging(log_level=logging.INFO, log_file="wdrive.log", max_bytes=10*1024*1024, backup_count=5):
    """Setup logging configuration for wdrive server."""
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Full path to log file
    log_path = os.path.join(log_dir, log_file)
    
    # Create logger
    logger = logging.getLogger('wdrive')
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Log startup message
    logger.info("=" * 50)
    logger.info("wdrive server logging initialized")
    logger.info(f"Log file: {log_path}")
    logger.info("=" * 50)
    
    return logger


def log_file_operation(logger, operation, filename, client_ip, success=True, error_msg=None):
    """Log file operations with standardized format."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = "SUCCESS" if success else "FAILED"
    
    log_message = f"{operation} - {filename} - {client_ip} - {status}"
    
    if error_msg and not success:
        log_message += f" - {error_msg}"
    
    if success:
        logger.info(log_message)
    else:
        logger.error(log_message)


def log_access(logger, client_ip, user_agent="", endpoint="", method="GET"):
    """Log access attempts with client information."""
    log_message = f"ACCESS - {client_ip} - {method} {endpoint}"
    if user_agent:
        log_message += f" - {user_agent[:100]}"  # Limit user agent length
    
    logger.info(log_message)


def log_authentication(logger, client_ip, username="", success=True):
    """Log authentication attempts."""
    status = "SUCCESS" if success else "FAILED"
    log_message = f"AUTH - {client_ip} - {username} - {status}"
    
    if success:
        logger.info(log_message)
    else:
        logger.warning(log_message)


def log_server_event(logger, event, details=""):
    """Log server events like startup, shutdown, errors."""
    log_message = f"SERVER - {event}"
    if details:
        log_message += f" - {details}"
    
    logger.info(log_message)


if __name__ == "__main__":
    # Test logging setup
    logger = setup_logging()
    
    # Test different log types
    logger.info("This is a test info message")
    logger.warning("This is a test warning message")
    logger.error("This is a test error message")
    
    # Test helper functions
    log_file_operation(logger, "UPLOAD", "test.txt", "192.168.1.100", True)
    log_file_operation(logger, "DOWNLOAD", "test.txt", "192.168.1.101", False, "File not found")
    log_access(logger, "192.168.1.102", "Mozilla/5.0", "/", "GET")
    log_authentication(logger, "192.168.1.103", "user", True)
    log_server_event(logger, "STARTUP", "Server started on port 8080")
    
    print("Logging test completed. Check the logs directory for output.")

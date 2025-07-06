# Logging Configuration

This document explains the logging setup in the MiniGameArchive project.

## Overview

The project uses Python's built-in `logging` module with a comprehensive configuration that adapts to the `DEBUG` setting.

## Configuration

### Log Levels
- **DEBUG mode**: Log level is set to `DEBUG` (most verbose)
- **Production mode**: Log level is set to `INFO` (less verbose)

### Log Handlers
1. **Console Handler**: Outputs logs to the terminal/console
2. **File Handler**: Saves logs to `logs/minigamearchive.log`

### Log Format
```
{levelname} {asctime} {module} {process:d} {thread:d} {message}
```

Example:
```
INFO 2025-07-06 22:03:57,034 test_i18n 25416 18360 Testing i18n setup...
```

## Logger Categories

### Django Framework Loggers
- `django`: General Django logs (INFO level)
- `django.request`: Request/response logs (WARNING level)
- `django.server`: Development server logs (INFO level)

### Application Logger
- `games`: Application-specific logs (DEBUG/INFO based on DEBUG setting)

## Usage

### In Views
```python
import logging

logger = logging.getLogger(__name__)

def my_view(request):
    logger.debug("Debug information")
    logger.info("General information")
    logger.warning("Warning message")
    logger.error("Error message")
```

### In Management Commands
```python
import logging
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("Command started")
        # ... command logic
        logger.info("Command completed")
```

### In Scripts
```python
import logging

# Configure logging for standalone scripts
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/script_name.log')
    ]
)

logger = logging.getLogger(__name__)
```

## Log Files

### Main Application Log
- **File**: `logs/minigamearchive.log`
- **Content**: All Django and application logs
- **Rotation**: Manual (consider using `RotatingFileHandler` for production)

### Script-Specific Logs
- `logs/setup.log`: Setup script logs
- `logs/compile_translations.log`: Translation compilation logs

## Log Levels Explained

- **DEBUG**: Detailed information for debugging
- **INFO**: General information about program execution
- **WARNING**: Indicates a potential problem
- **ERROR**: A more serious problem
- **CRITICAL**: A critical problem that may prevent the program from running

## Best Practices

1. **Use appropriate log levels**:
   - DEBUG: Detailed debugging information
   - INFO: General operational messages
   - WARNING: Potential issues
   - ERROR: Actual errors

2. **Include context in log messages**:
   ```python
   logger.info(f"User {user.username} created training session '{session.name}'")
   ```

3. **Log exceptions with context**:
   ```python
   try:
       # ... code
   except Exception as e:
       logger.error(f"Failed to process request: {e}")
   ```

4. **Use structured logging for complex data**:
   ```python
   logger.info("Game added to session", extra={
       'game_id': game.id,
       'game_name': game.name,
       'session_id': session.id
   })
   ```

## Production Considerations

1. **Log Rotation**: Implement log rotation to prevent log files from growing too large
2. **Log Aggregation**: Consider using tools like ELK stack or Sentry for log aggregation
3. **Sensitive Data**: Never log passwords, API keys, or other sensitive information
4. **Performance**: Be mindful of logging overhead in production

## Monitoring

To monitor logs in real-time:
```bash
# Watch the main log file
tail -f logs/minigamearchive.log

# Watch for errors only
tail -f logs/minigamearchive.log | grep ERROR

# Watch for specific user actions
tail -f logs/minigamearchive.log | grep "user@example.com"
```

## Troubleshooting

### No logs appearing
1. Check if the `logs/` directory exists
2. Verify file permissions
3. Check the log level configuration

### Logs too verbose
1. Increase the log level in settings
2. Use more specific loggers
3. Filter out unnecessary DEBUG messages

### Logs not rotating
1. Implement `RotatingFileHandler` for automatic rotation
2. Set up log rotation via system tools (logrotate)
3. Monitor log file sizes manually 
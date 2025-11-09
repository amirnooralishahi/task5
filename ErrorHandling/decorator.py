import asyncio

from fastapi import HTTPException, status
import functools
import logging

logger = logging.getLogger(__name__)


def handle_errors(func):
    """Decorator برای هندل خودکار خطاها در متدهای سرویس"""

    if asyncio.iscoroutinefunction(func):  # بررسی async بودن تابع
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ValueError as e:
                logger.warning(f"ValueError: {e}")
                raise HTTPException(status_code=422, detail=str(e))
            except TypeError as e:
                logger.warning(f"TypeError: {e}")
                raise HTTPException(status_code=400, detail=str(e))
            except AttributeError as e:
                logger.error(f"AttributeError: {e}")
                raise HTTPException(status_code=500, detail="Attribute missing in object")
            except ZeroDivisionError as e:
                logger.error(f"ZeroDivisionError: {e}")
                raise HTTPException(status_code=400, detail="Division by zero not allowed")
            except LookupError as e:
                logger.warning(f"LookupError: {e}")
                raise HTTPException(status_code=404, detail="Entity not found")
            except ConnectionError as e:
                logger.error(f"ConnectionError: {e}")
                raise HTTPException(status_code=503, detail="Database connection failed")
            except Exception as e:
                logger.exception(f"Unexpected error in {func.__name__}: {e}")
                raise HTTPException(status_code=500, detail="Internal server error")

        return async_wrapper

    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as e:
                raise HTTPException(status_code=422, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        return sync_wrapper
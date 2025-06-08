"""
Decorator pattern implementation for adding functionality to database operations.
"""
import time
import logging
import functools
from typing import Any, Callable, Dict
import pandas as pd


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryCache:
    """
    Simple in-memory cache for query results.
    """
    def __init__(self, max_size: int = 100):
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size
        self._access_order = []
    
    def get(self, key: str) -> Any:
        """
        Get a cached result.
        Args:
            key (str): Cache key.
        Returns:
            Any: Cached result or None if not found.
        """
        if key in self._cache:
            # Move to end for LRU
            self._access_order.remove(key)
            self._access_order.append(key)
            return self._cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """
        Store a result in cache.
        Args:
            key (str): Cache key.
            value (Any): Value to cache.
        """
        if key in self._cache:
            # Update existing
            self._cache[key] = value
            self._access_order.remove(key)
            self._access_order.append(key)
        else:
            # Add new
            if len(self._cache) >= self._max_size:
                # Remove least recently used
                oldest_key = self._access_order.pop(0)
                del self._cache[oldest_key]
            
            self._cache[key] = value
            self._access_order.append(key)
    
    def clear(self) -> None:
        """
        Clear the cache.
        """
        self._cache.clear()
        self._access_order.clear()


# Global cache instance
_query_cache = QueryCache()


def timing_decorator(func: Callable) -> Callable:
    """
    Decorator that measures and logs execution time.
    This solves the problem of performance monitoring and helps identify slow queries.
    
    Args:
        func (Callable): Function to decorate.
    Returns:
        Callable: Decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        
        logger.info(f"{func.__name__} executed in {execution_time:.4f} seconds")
        
        # Add timing info to result if it's a DataFrame
        if isinstance(result, pd.DataFrame):
            result.attrs['execution_time'] = execution_time
        
        return result
    return wrapper


def logging_decorator(func: Callable) -> Callable:
    """
    Decorator that logs method calls and parameters.
    This solves the problem of debugging and auditing database operations.
    
    Args:
        func (Callable): Function to decorate.
    Returns:
        Callable: Decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Log method call
        method_name = func.__name__
        logger.info(f"Calling {method_name}")
        
        # Log parameters (excluding self and sensitive data)
        if args and hasattr(args[0], '__class__'):
            # Skip self parameter
            log_args = args[1:]
        else:
            log_args = args
        
        if log_args:
            logger.debug(f"Parameters: args={log_args}")
        
        if kwargs:
            # Filter out sensitive information like passwords
            filtered_kwargs = {k: v for k, v in kwargs.items() 
                             if 'password' not in k.lower() and 'secret' not in k.lower()}
            logger.debug(f"Keyword parameters: {filtered_kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"{method_name} completed successfully")
            
            # Log result summary if it's a DataFrame
            if isinstance(result, pd.DataFrame):
                logger.info(f"Returned DataFrame with {len(result)} rows and {len(result.columns)} columns")
            
            return result
        
        except Exception as e:
            logger.error(f"{method_name} failed with error: {str(e)}")
            raise
    
    return wrapper


def caching_decorator(cache_ttl: int = 300) -> Callable:
    """
    Decorator that caches query results.
    This solves the problem of repeated expensive queries and improves performance.
    
    Args:
        cache_ttl (int): Cache time-to-live in seconds.
    Returns:
        Callable: Decorator function.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and parameters
            cache_key = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            
            # Try to get from cache
            cached_result = _query_cache.get(cache_key)
            if cached_result is not None:
                logger.info(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            logger.info(f"Cache miss for {func.__name__}, executing...")
            result = func(*args, **kwargs)
            
            # Cache the result
            _query_cache.set(cache_key, result)
            logger.info(f"Result cached for {func.__name__}")
            
            return result
        
        return wrapper
    return decorator


def error_handling_decorator(func: Callable) -> Callable:
    """
    Decorator that provides enhanced error handling.
    This solves the problem of graceful error handling and user-friendly error messages.
    
    Args:
        func (Callable): Function to decorate.
    Returns:
        Callable: Decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except ConnectionError as e:
            logger.error(f"Database connection error in {func.__name__}: {str(e)}")
            raise RuntimeError(f"Failed to connect to database: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise RuntimeError(f"Database operation failed: {str(e)}")
    
    return wrapper


def retry_decorator(max_retries: int = 3, delay: float = 1.0) -> Callable:
    """
    Decorator that retries failed operations.
    This solves the problem of transient database connection issues.
    
    Args:
        max_retries (int): Maximum number of retries.
        delay (float): Delay between retries in seconds.
    Returns:
        Callable: Decorator function.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}")
                        logger.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed for {func.__name__}")
            
            raise last_exception
        
        return wrapper
    return decorator


def database_operation(cache_ttl: int = 300, max_retries: int = 3) -> Callable:
    """
    Composite decorator that combines multiple decorators for database operations.
    This provides a complete solution for database method enhancement.
    
    Args:
        cache_ttl (int): Cache time-to-live in seconds.
        max_retries (int): Maximum number of retries.
    Returns:
        Callable: Composite decorator function.
    """
    def decorator(func: Callable) -> Callable:
        # Apply decorators in order (innermost first)
        decorated_func = func
        decorated_func = error_handling_decorator(decorated_func)
        decorated_func = retry_decorator(max_retries)(decorated_func)
        decorated_func = caching_decorator(cache_ttl)(decorated_func)
        decorated_func = timing_decorator(decorated_func)
        decorated_func = logging_decorator(decorated_func)
        
        return decorated_func
    
    return decorator 
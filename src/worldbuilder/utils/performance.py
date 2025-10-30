"""
Performance optimization utilities
Includes caching, lazy loading, and other performance enhancements
"""

from functools import lru_cache, wraps
from typing import Any, Callable, Optional
import time
import weakref


class EntityCache:
    """Simple in-memory cache for entities using weak references"""
    
    def __init__(self, max_size=1000):
        self.max_size = max_size
        self._cache = {}
        self._access_times = {}
        
    def get(self, entity_type: str, entity_id: int) -> Optional[Any]:
        """Get an entity from cache"""
        key = (entity_type, entity_id)
        
        if key in self._cache:
            self._access_times[key] = time.time()
            return self._cache[key]
            
        return None
        
    def put(self, entity_type: str, entity_id: int, entity: Any):
        """Put an entity in cache"""
        key = (entity_type, entity_id)
        
        # Check if we need to evict
        if len(self._cache) >= self.max_size:
            self._evict_oldest()
            
        self._cache[key] = entity
        self._access_times[key] = time.time()
        
    def remove(self, entity_type: str, entity_id: int):
        """Remove an entity from cache"""
        key = (entity_type, entity_id)
        
        if key in self._cache:
            del self._cache[key]
            del self._access_times[key]
            
    def clear(self):
        """Clear the entire cache"""
        self._cache.clear()
        self._access_times.clear()
        
    def _evict_oldest(self):
        """Evict the least recently accessed item"""
        if not self._access_times:
            return
            
        oldest_key = min(self._access_times, key=self._access_times.get)
        del self._cache[oldest_key]
        del self._access_times[oldest_key]
        
    def get_size(self) -> int:
        """Get current cache size"""
        return len(self._cache)


class LazyLoader:
    """Lazy loading wrapper for expensive operations"""
    
    def __init__(self, loader_func: Callable, *args, **kwargs):
        self.loader_func = loader_func
        self.args = args
        self.kwargs = kwargs
        self._value = None
        self._loaded = False
        
    def get(self):
        """Get the value, loading it if necessary"""
        if not self._loaded:
            self._value = self.loader_func(*self.args, **self.kwargs)
            self._loaded = True
        return self._value
        
    def is_loaded(self) -> bool:
        """Check if value has been loaded"""
        return self._loaded
        
    def reset(self):
        """Reset the loader, forcing reload on next get()"""
        self._value = None
        self._loaded = False


def cached_method(max_size=128):
    """Decorator for caching instance method results"""
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Create cache key from args and kwargs
            key = (args, tuple(sorted(kwargs.items())))
            
            if key in cache:
                return cache[key]
                
            result = func(self, *args, **kwargs)
            
            # Simple size limit
            if len(cache) >= max_size:
                # Remove oldest entry (first in dict)
                cache.pop(next(iter(cache)))
                
            cache[key] = result
            return result
            
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
        
    return decorator


def measure_time(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper


class BatchLoader:
    """Batch loader for loading multiple entities efficiently"""
    
    def __init__(self, loader_func: Callable, batch_size=100):
        self.loader_func = loader_func
        self.batch_size = batch_size
        self.pending = []
        
    def add(self, entity_id: int):
        """Add an entity ID to the batch"""
        self.pending.append(entity_id)
        
    def load(self):
        """Load all pending entities in batches"""
        results = {}
        
        for i in range(0, len(self.pending), self.batch_size):
            batch = self.pending[i:i + self.batch_size]
            batch_results = self.loader_func(batch)
            results.update(batch_results)
            
        self.pending.clear()
        return results
        
    def clear(self):
        """Clear pending items"""
        self.pending.clear()


class ProgressTracker:
    """Track progress of long-running operations"""
    
    def __init__(self, total: int, callback: Optional[Callable] = None):
        self.total = total
        self.current = 0
        self.callback = callback
        self.start_time = time.time()
        
    def update(self, increment=1):
        """Update progress"""
        self.current += increment
        
        if self.callback:
            percentage = (self.current / self.total) * 100 if self.total > 0 else 0
            elapsed = time.time() - self.start_time
            self.callback(self.current, self.total, percentage, elapsed)
            
    def reset(self):
        """Reset progress"""
        self.current = 0
        self.start_time = time.time()
        
    def is_complete(self) -> bool:
        """Check if complete"""
        return self.current >= self.total


# Global entity cache instance
global_entity_cache = EntityCache()

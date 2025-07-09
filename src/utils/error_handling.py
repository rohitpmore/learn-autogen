import random
from typing import List, Type, Callable, Optional
import functools
import asyncio
from enum import Enum
import time


class RetryConfig:
    """
    Configuration for retrying failed requests.
    """
    max_retries: int
    initial_delay: float
    backoff_factor: float
    retry_on_exceptions: List[Type[Exception]]
    
    def __init__(self, max_retries: int, initial_delay: float, backoff_factor: float, retry_on_exceptions: List[Type[Exception]]):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.retry_on_exceptions = retry_on_exceptions


def retry_async(config: RetryConfig):
    """Decorator that adds retry logic to an async function."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(config.max_retries + 1):
                try:
                    print(f"Attempt {attempt + 1} of {config.max_retries + 1} for {func.__name__}")
                    result = await func(*args, **kwargs)
                    print(f" Success on attempt {attempt + 1}")
                    return result
                except Exception as e:
                    last_exception = e
                    print(f"Attempt {attempt + 1} failed: {e}")

                    should_retry = any(isinstance(e, exc) for exc in config.retry_on_exceptions)

                    if not should_retry:
                        print(f"Exception type {type(e).__name__} not in retry list - failing fast")
                        raise e
        
                    if attempt == config.max_retries:
                        print(f"All {config.max_retries} attempts failed")
                        break

                    delay = config.initial_delay * (config.backoff_factor ** attempt)
                    jitter = random.uniform(0.1, 0.3)* delay
                    actual_delay = delay + jitter
                    print(f"Waiting {actual_delay:.2f} seconds (base delay: {delay:.2f}s, jitter: {jitter:.2f}s)")
                    await asyncio.sleep(actual_delay)

            if last_exception:
                raise last_exception
            
        return wrapper
    return decorator

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerConfig:
    """Configuration for circuit breaker behavior."""

    def __init__(
            self,
            failure_threshold: int = 5,
            recovery_timeout: float = 30.0,
            success_threshold: int = 2,
            timeout: float = 10.0,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.timeout = timeout


class CircuitBreaker:
    """ Circuit breaker implementation for async functions."""

    def __init__(self, config: CircuitBreakerConfig):
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[float] = None
        self.next_attempt_time: Optional[float] = None

    def should_allow_request(self) -> bool:
        """ Check if the request should be allowed based on the current state."""
        current_time = time.time()

        if self.state == CircuitState.CLOSED:
            return True
        
        elif self.state == CircuitState.OPEN:
            if self.next_attempt_time and current_time >= self.next_attempt_time:
                print(f"Circuit breaker transitioning to HALF_OPEN state")
                self.state = CircuitState.HALF_OPEN
                return True
            else:
                print(f"Circuit breaker still in OPEN state - request denied")
                return False
        
        elif self.state == CircuitState.HALF_OPEN:
            return True
        
        return False
    
    def record_success(self):
        """ Record a successful request."""

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            print(f"Success in HALF_OPEN: {self.success_count} / {self.config.success_threshold}")

            if self.success_count >= self.config.success_threshold:
                print(f"Circuit breaker closing - service recovered")
                self.state = CircuitState.CLOSED
                self.success_count = 0
                self.failure_count = 0
                self.next_attempt_time = None
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0

    def record_failure(self):
        """Record a failed request."""
        current_time = time.time()

        self.last_failure_time = current_time

        if self.state == CircuitState.CLOSED:
            self.failure_count += 1
            print(f"Failure count: {self.failure_count} / {self.config.failure_threshold}")

            if self.failure_count >= self.config.failure_threshold:
                print(f"Circuit breaker opening - too many failures")
                self.state = CircuitState.OPEN
                self.next_attempt_time = current_time + self.config.recovery_timeout
        
        elif self.state == CircuitState.HALF_OPEN:
            print(f"Failure in HALF_OPEN - returning to OPEN state")
            self.state = CircuitState.OPEN
            self.next_attempt_time = current_time + self.config.recovery_timeout
            self.success_count = 0


def circuit_breaker(config: CircuitBreakerConfig):
    """Decorator that adds circuit breaker logic to an async function."""
    breaker = CircuitBreaker(config)
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not breaker.should_allow_request():
                raise Exception("Circuit breaker is open - request denied")
            try:
                result = await func(*args, **kwargs)
                breaker.record_success()
                return result
            except Exception as e:
                breaker.record_failure()
                raise e
        return wrapper
    return decorator


async def main():
    async def test_function():
        print("inside test_function")
        return "success"
    
    async def failing_test_function():
        print("Inside failing_test_function - will always fail")
        raise Exception("This always fails")
    
    async def auth_error_function():
        print("Inside auth_error_function - will raise auth error")
        raise ValueError("Authentication error - don't retry this.")
    
    async def network_error_function():
        print("Inside network_error_function - will raise network error")
        raise ConnectionError("Network error - retry this.")
    
    config = RetryConfig(
        max_retries=3, 
        initial_delay=1.0, 
        backoff_factor=2, 
        retry_on_exceptions=[ConnectionError, TimeoutError]
    )

    decorated_function = retry_async(config)(test_function)

    result = await decorated_function()
    print(f"Result: {result}")

    print("---------------Testing retry logic with failing function-----------------")
    decorated_failing_function = retry_async(config)(failing_test_function)

    try:
        result = await decorated_failing_function()
    except Exception as e:
        print(f"Final exception: {e}")

    print("---------------Testing exception classification-----------------")
    decorated_auth_function = retry_async(config)(auth_error_function)

    try:
        result = await decorated_auth_function()
    except Exception as e:
        print(f"Auth error final exception: {e}")

    print("---------------Testing retry logic with network error-----------------")
    decorated_network_function = retry_async(config)(network_error_function)

    try:
        result = await decorated_network_function()
    except Exception as e:
        print(f"Network error final exception: {e}")

    async def flaky_service(fail_count: int = 0):
        """Service that fails a certain number of times and then succeeds."""

        if flaky_service.call_count < fail_count:
            flaky_service.call_count += 1
            print(f"Flaky service failing (call {flaky_service.call_count})")
            raise ConnectionError("Service temporarily unavailable")
        else:
            print(f"Flaky service succeeding (call {flaky_service.call_count + 1})")
            return "Success"
        
    flaky_service.call_count = 0

    print("---------------Testing circuit breaker pattern-----------------")

    cb_config = CircuitBreakerConfig(
        failure_threshold=3,
        recovery_timeout=2.0,
        success_threshold=2,
        timeout=5.0
    )

    protected_service = circuit_breaker(cb_config)(flaky_service)

    print("\n -- Test 1: Triggering circuit breaker")
    for i in range(5):
        try:
            result = await protected_service(fail_count=10)
            print(f"Call {i+1} : {result}")
        except Exception as e:
            print(f"Call {i+1} failed: {e}")

        await asyncio.sleep(0.1)

    print("\n -- Test 2: Service recovers after timeout")
    print("Waiting 2.5 seconds for recovery timeout...")
    await asyncio.sleep(2.5)

    for i in range(4):
        try:
            result = await protected_service(fail_count=0)
            print(f"Recovery call {i+1} : {result}")
        except Exception as e:
            print(f"Recovery call {i+1} failed: {e}")

        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())

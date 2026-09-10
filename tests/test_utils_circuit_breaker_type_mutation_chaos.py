import time

from taipanstack.resilience.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
)


def test_circuit_breaker_chaos_type_mutation_success_count():
    """Simulate a chaos scenario where success_count is mutated to an invalid type."""
    breaker = CircuitBreaker(failure_threshold=2, success_threshold=2, timeout=0.01)

    # Force to HALF_OPEN state
    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.last_failure_time = time.monotonic() - 1.0
    breaker._state.success_count = "string_instead_of_int"  # Mutate the type

    @breaker
    def success_call():
        return "ok"

    # Should not crash on first call due to type mutation, it should reset or handle it safely
    # and eventually close. Let's see if it crashes.
    assert success_call() == "ok"
    # Call again to see if it closes.
    assert success_call() == "ok"

    assert breaker.state == CircuitState.CLOSED

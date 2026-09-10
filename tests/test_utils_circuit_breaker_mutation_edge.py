from taipanstack.resilience.circuit_breaker import CircuitBreaker, CircuitState


def test_circuit_breaker_chaos_half_open_type_mutation_recovery():
    """Simulate type mutation on half_open_attempts in HALF_OPEN state.

    The system should safely degrade by resetting the counter and allowing the request,
    rather than permanently rejecting all requests.
    """
    breaker = CircuitBreaker(failure_threshold=1, success_threshold=3, timeout=0.01)

    breaker._state.state = CircuitState.HALF_OPEN
    breaker._state.half_open_attempts = "corrupted"  # type: ignore

    @breaker
    def successful_service():
        return "success"

    # Should not raise CircuitBreakerError. Should safely handle the corrupted state,
    # reset it, and allow the request.
    assert successful_service() == "success"
    # the finally block decrements it, so it should be 0
    assert breaker._state.half_open_attempts == 0

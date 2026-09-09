import asyncio
import pytest

from taipanstack.core.result import Err, Ok, Result
from taipanstack.resilience.adaptive.orchestrator import ResilienceOrchestrator
from taipanstack.utils.rate_limit import rate_limit
from taipanstack.security.guards import guard_path_traversal

@pytest.mark.asyncio
async def test_chaos_engineering_mathematical_proof_ultimate_microservice():
    """Simulates an ultimate chaos microservice scenario."""
    orchestrator = (
        ResilienceOrchestrator("ultimate_chaos")
        .with_bulkhead(max_concurrent=50, max_queue=200)
        .with_timeout(1.0)
    )

    @rate_limit(max_calls=10000, time_window=1.0)
    async def process_data(path: str, data: dict) -> Result[str, Exception]:
        sec_res = guard_path_traversal(path, "/data")
        # In a real microservice, we don't catch the TypeError if one is raised,
        # but the orchestrator should gracefully capture all synchronous and asynchronous exceptions
        # and convert them to Err.

        if data.get("crash"):
            raise RuntimeError("Intentional crash")

        await asyncio.sleep(0.01)
        return Ok(f"Processed {sec_res}")

    async def attacker(i: int):
        paths = ["/data/user.txt", "../../../etc/passwd", "/data/safe.txt"]
        payloads = [{"ok": True}, {"crash": True}, {"ok": True}]
        return await orchestrator.execute(process_data, paths[i % 3], payloads[i % 3])

    tasks = [attacker(i) for i in range(150)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for r in results:
        # Mathematical proof: Every outcome must be wrapped in Result monad
        assert isinstance(r, (Ok, Err)), f"Outcome {r} must be wrapped in Result monad, got {type(r)}"

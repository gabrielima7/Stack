import hypothesis.strategies as st
from hypothesis import given

from taipanstack.core.result import Err, Ok, Result


@given(st.integers())
def test_core_result_ok_value_preservation(value: int) -> None:
    result: Result[int, str] = Ok(value)
    assert result.is_ok()
    assert result.unwrap() == value

@given(st.text())
def test_core_result_err_value_preservation(error: str) -> None:
    result: Result[int, str] = Err(error)
    assert result.is_err()
    assert result.unwrap_err() == error

@given(st.integers(), st.text())
def test_core_result_mapping(val: int, err: str) -> None:
    ok_res = Ok(val)
    mapped_ok = ok_res.map(str)
    assert mapped_ok.unwrap() == str(val)

    err_res: Result[int, str] = Err(err)
    mapped_err = err_res.map(str)
    assert mapped_err.unwrap_err() == err

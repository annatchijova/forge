import ast
import time

from forge.dataflow import float_calls_reaching_return


def _function(src: str) -> ast.FunctionDef:
    return ast.parse(src).body[0]


def test_float_taint_is_a_union_across_branches_not_a_race():
    # A name reassigned with a different float() call in each branch of an
    # if/else must merge both sources into one growing taint set. Treating
    # the second assignment's line set as unequal-therefore-changed-forever
    # previously made the fixed-point loop oscillate without terminating.
    fn = _function(
        "def f():\n"
        "    for i in range(2):\n"
        "        if i == 0:\n"
        "            z = {'a': float(1)}\n"
        "        else:\n"
        "            z = {'b': float(2)}\n"
        "    return z\n"
    )
    start = time.monotonic()
    result = float_calls_reaching_return(fn)
    elapsed = time.monotonic() - start
    assert elapsed < 1.0, f"float_calls_reaching_return did not converge quickly (took {elapsed}s)"
    assert result == {4, 6}


def test_float_taint_converges_with_three_reassignments_of_the_same_name():
    fn = _function(
        "def f():\n"
        "    if a:\n"
        "        z = {'a': float(1)}\n"
        "    elif b:\n"
        "        z = {'b': float(2)}\n"
        "    else:\n"
        "        z = {'c': float(3)}\n"
        "    return z\n"
    )
    start = time.monotonic()
    result = float_calls_reaching_return(fn)
    assert time.monotonic() - start < 1.0
    assert result == {3, 5, 7}


def test_float_not_reaching_return_through_mutation_is_not_flagged():
    # samples is built via .append(), never itself reassigned to a value
    # containing a float() call, so it must not be flagged - this keeps the
    # analysis "shallow" (return-flow only) rather than tracking mutation.
    fn = _function(
        "def f():\n"
        "    samples = []\n"
        "    for i in range(2):\n"
        "        samples.append({'z': float(i)})\n"
        "    return samples\n"
    )
    assert float_calls_reaching_return(fn) == set()

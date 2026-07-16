import time

from forge.build_info import _compute_fingerprint, RUNTIME_FINGERPRINT, PROCESS_IMPORTED_AT_EPOCH


def test_fingerprint_is_a_hex_digest_prefix():
    assert isinstance(RUNTIME_FINGERPRINT, str) and len(RUNTIME_FINGERPRINT) == 16
    assert all(c in "0123456789abcdef" for c in RUNTIME_FINGERPRINT)


def test_fingerprint_changes_when_a_source_file_changes(tmp_path):
    (tmp_path / "a.py").write_text("x = 1\n")
    before = _compute_fingerprint(tmp_path)
    time.sleep(0.01)
    (tmp_path / "a.py").write_text("x = 2\n")
    after = _compute_fingerprint(tmp_path)
    assert before != after


def test_fingerprint_is_stable_for_unchanged_files(tmp_path):
    (tmp_path / "a.py").write_text("x = 1\n")
    (tmp_path / "b.py").write_text("y = 2\n")
    assert _compute_fingerprint(tmp_path) == _compute_fingerprint(tmp_path)


def test_process_imported_at_is_an_int_epoch_not_a_float():
    # int, not float: this value can flow into sealed/canonicalized payloads,
    # and forge/canonical.py forbids floats there entirely (deterministic-core).
    assert isinstance(PROCESS_IMPORTED_AT_EPOCH, int)

import pytest
from pathlib import Path
from megamind import ModelArchaeologyScanner

def test_model_scanner_discovery(tmp_path):
    # Create fake model weights file
    fake_weights = tmp_path / "model_checkpoint.safetensors"
    fake_weights.write_bytes(b"0" * 1024 * 1024)

    scanner = ModelArchaeologyScanner(search_paths=[tmp_path])
    found = scanner.scan_local_archives()
    assert len(found) == 1
    assert found[0]["filename"] == "model_checkpoint.safetensors"
    assert found[0]["format"] == "SAFETENSORS"

def test_verification_ladder(tmp_path):
    fake_weights = tmp_path / "stealth_v1.gguf"
    fake_weights.write_bytes(b"GGUF_HEADER_DATA_SAMPLE")

    scanner = ModelArchaeologyScanner(search_paths=[tmp_path])
    res = scanner.advance_verification_ladder(str(fake_weights))
    assert res["verification_ladder_stage"] == "checkpoint_verified"
    assert res["format"] == "GGUF"
    assert "sha256_sample" in res

import pytest
from megamind import MegamindMissionKernel
from megamind.stealth import StealthMicrowave, StealthSherlock, StealthSonic, StealthMorpheus

def test_stealth_organs():
    microwave = StealthMicrowave()
    res_mw = microwave.execute_tasks([{"task_id": "T1", "fn": lambda: 42}])
    assert res_mw["status"] == "SUCCEEDED"

    sherlock = StealthSherlock()
    sh_res = sherlock.index_artifact("A1", "/tmp/file", "hello world testing sherlock")
    assert sh_res["status"] == "INDEXED"
    found = sherlock.search_context("sherlock")
    assert len(found) == 1

    sonic = StealthSonic()
    son_res = sonic.process_audio_artifact("/tmp/test.wav", simulated_transcript="Audio test transcript")
    assert son_res["status"] == "SUCCEEDED"

    morpheus = StealthMorpheus()
    morp_res = morpheus.transition_state("voice-foundation", "active")
    assert morp_res["status"] == "TRANSITIONED"

def test_mission_kernel_execution():
    kernel = MegamindMissionKernel()
    res = kernel.execute_voice_memory_mission("/tmp/audio.wav", simulated_transcript="Testing complete voice memory mission")
    assert res["status"] == "SUCCEEDED"
    assert "whole_mission_receipt" in res
    assert res["whole_mission_receipt"]["verification"] == "HARDENED"

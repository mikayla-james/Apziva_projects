def test_imports():
    """Verify core dependencies import correctly."""
    import torch
    import transformers
    import numpy as np

    # Actually "use" them so flake8 is happy
    assert torch is not None
    assert transformers is not None
    assert np is not None


def test_label_mapping():
    """Test that label mappings are consistent."""
    id2label = {0: "notflip", 1: "flip"}
    label2id = {"notflip": 0, "flip": 1}
    assert id2label[label2id["flip"]] == "flip"
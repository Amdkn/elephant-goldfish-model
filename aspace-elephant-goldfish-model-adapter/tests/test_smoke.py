"""Smoke tests de l'adapter elephant-goldfish-model (D-N053 pas C).

Roulés avec le venv du pas : `python -m pytest aspace-elephant-goldfish-model-adapter/tests/test_smoke.py -v`.
Ne touchent pas l'amont, ne font aucun appel réseau. La validation complète
de la suite est celle de la suite amont (`pytest tests/unit`, 336 passed,
2 skipped au gel) ; le smoke vérifie les constantes, les comptages mesurés
par l'adapter et le statut de référence du canonique (§D5).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import aspace_elephant_goldfish_model_adapter as adapter  # noqa: E402


def test_constants():
    assert re.fullmatch(r"[0-9a-f]{40}", adapter.PINNED_UPSTREAM_COMMIT)
    assert adapter.FIBER_ADDRESS == "fiber:a0:elephant-goldfish-model"
    assert adapter.LICENSE == "Apache-2.0"
    assert adapter.FORK == "Amdkn/elephant-goldfish-model"
    assert adapter.UPSTREAM_REPO == "google/elephant-goldfish-model"
    assert adapter.ADAPTER_VERSION == "0.1.0"
    assert adapter.BIND_COMMIT == "3d643fe7e1272cc7972bd1456ded6ebff32b54e7"
    assert adapter.BIND_LAYER == "4L"


def test_validate_counts():
    v = adapter.validate()
    assert v["pinned_commit_is_40_hex"] is True
    assert v["license_file_present"] is True
    assert v["skill_dirs_total"] == 7
    assert v["skills_with_skill_md"] == 7
    assert v["skills_missing"] == []
    assert v["skills_unexpected"] == []
    assert len(v["frontmatter_ok"]) == 7
    assert v["frontmatter_bad"] == []
    assert v["test_md_missing"] == []
    assert v["scenarios_missing"] == []
    assert v["agents_missing"] == []
    assert v["assets_missing"] == []
    assert v["distributions_present"] is True
    assert v["resources_present"] is True
    assert v["adapter_network_calls"] == 0
    assert v["confinement"]


def test_validate_coherent():
    v = adapter.validate()
    assert v["inventory_coherent"] is True
    assert v["canonical"] == "fiber:a0:superpowers"


def test_doctor_all_pass():
    checks = adapter.doctor()
    assert checks, "doctor() vide"
    failed = [c for c in checks if not c["ok"]]
    assert not failed, failed


def test_no_network_import_in_adapter():
    src = (Path(adapter.__file__).parent / "__init__.py").read_text()
    for banned in ("requests", "httpx", "urllib", "socket", "huggingface_hub", "aiohttp"):
        assert banned not in src, banned


def test_describe():
    d = adapter.describe()
    assert d["fiber"] == "fiber:a0:elephant-goldfish-model"
    assert d["pinned_upstream_commit"] == adapter.PINNED_UPSTREAM_COMMIT
    assert d["license"] == "Apache-2.0"
    assert d["canonical"] == "fiber:a0:superpowers"

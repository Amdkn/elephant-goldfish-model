"""A'Space adapter — elephant-goldfish-model (D-N053 pas C, design Clara + design signé pas C).

Contrat seul, patron pas A/B : cet adapter ne modifie AUCUN fichier amont,
ne fait AUCUN appel réseau, ne monte AUCUN poids. Il constate : le gel
épinglé, la licence, l'inventaire des 7 skills EGM (comptage SKILL.md,
frontmatter name + license + description, TEST.md + test_scenarios.yaml
présents par skill, agents/ + assets/) — et il se déclare RÉFÉRENCE du
canonique MasterSpec `fiber:a0:superpowers` (§D5), pas un framework parallèle.

Adresse : fiber:a0:elephant-goldfish-model
Fork souverain : Amdkn/elephant-goldfish-model (parent google/elephant-goldfish-model, branche main)
Gel amont : 113a3afc44e8f4f54722d7150d5701f65cc8ef7f (« fix(review): save GoldfishContext URLs as files (#289) »)
Bind Cordis Fiber (4L) : 3d643fe7e1272cc7972bd1456ded6ebff32b54e7
Licence : Apache-2.0

Mesures au gel (2026-11-11, vérifiées au fichier) :
- 7 skills (egm-bootstrap, egm-brainstorm, egm-draft, egm-drift-report,
  egm-resolve, egm-review, egm-review-loop) — chacune avec SKILL.md
  (frontmatter name + license Apache-2.0 + description), TEST.md,
  test_scenarios.yaml, agents/, assets/ ; references/ pour bootstrap et
  draft seulement.
- distributions/ (claude), resources/ (README.md, document_standards,
  execution_instructions.md).
- Suite amont bornée (D-C2) : `pytest tests/unit` (18 modules, offline,
  per TESTING.md) — 336 passed, 2 skipped au gel. Job site (Astro) hors
  borne ; intégrations opt-in exclues (CLI authentifiés + quota).
- Gel tenu : dérive 39 (design : 36 — la dérive bouge, +3), amont vivant —
  pas de re-gel sur la tête vivante, revisite par signal. Le fork main
  portait 3 commits amont au-delà du gel (0dfb5bf, ccf79c5, 6a8001e) ;
  main ramené au gel avant adaptation (commits préservés verbatim sur
  upstream/main google/elephant-goldfish-model, vérifié) — le parent de
  l'adapter est le gel, per design §3.
- Télémétrie : 0 SDK ; le mot « telemetry » n'apparaît que comme critère de
  design dans une table de la skill brainstorm, pas comme du code.
"""

from __future__ import annotations

import re
from pathlib import Path

FIBER_ADDRESS = "fiber:a0:elephant-goldfish-model"
FORK = "Amdkn/elephant-goldfish-model"
UPSTREAM_REPO = "google/elephant-goldfish-model"
UPSTREAM_BRANCH = "main"
PINNED_UPSTREAM_COMMIT = "113a3afc44e8f4f54722d7150d5701f65cc8ef7f"
PINNED_UPSTREAM_COMMIT_SHORT = "113a3afc"
BIND_COMMIT = "3d643fe7e1272cc7972bd1456ded6ebff32b54e7"
BIND_LAYER = "4L"
LICENSE = "Apache-2.0"
ADAPTER_VERSION = "0.1.0"

CANONICAL = "fiber:a0:superpowers"
EXPECTED_SKILLS = (
    "egm-bootstrap",
    "egm-brainstorm",
    "egm-draft",
    "egm-drift-report",
    "egm-resolve",
    "egm-review",
    "egm-review-loop",
)

CONFINEMENT = """Aucun confinement commercial : code et skills Apache-2.0. Usage B2B
autorisé par la licence. L'adapter ne fait que constater l'inventaire ;
aucune skill amont n'est modifiée."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _frontmatter(text: str) -> dict:
    """Extrait name + license + description du frontmatter d'un SKILL.md.

    Gère les scalaires pliés YAML (`description: >-` suivi de lignes
    indentées) : une description pliée compte comme présente si au moins
    une ligne de contenu indentée suit.
    """
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    lines = text[4:end].splitlines()
    out: dict[str, str] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$", line)
        if m:
            key, value = m.group(1), m.group(2)
            if value in (">-", ">", "|", "|-"):
                folded = []
                j = i + 1
                while j < len(lines) and (lines[j].startswith("  ") or lines[j].strip() == ""):
                    if lines[j].strip():
                        folded.append(lines[j].strip())
                    j += 1
                out[key] = " ".join(folded)
                i = j
                continue
            out[key] = value
        i += 1
    return out


def _skill_inventory(root: Path) -> dict:
    skills_dir = root / "skills"
    dirs = sorted(p.name for p in skills_dir.iterdir() if p.is_dir()) if skills_dir.is_dir() else []
    present = [p for p in dirs if (skills_dir / p / "SKILL.md").is_file()]
    frontmatter_ok: list[str] = []
    frontmatter_bad: list[str] = []
    test_md_missing: list[str] = []
    scenarios_missing: list[str] = []
    agents_missing: list[str] = []
    assets_missing: list[str] = []
    for name in present:
        fm = _frontmatter((skills_dir / name / "SKILL.md").read_text(encoding="utf-8", errors="replace"))
        if fm.get("name") == name and fm.get("license") == "Apache-2.0" and fm.get("description"):
            frontmatter_ok.append(name)
        else:
            frontmatter_bad.append(name)
        base = skills_dir / name
        if not (base / "TEST.md").is_file():
            test_md_missing.append(name)
        if not (base / "test_scenarios.yaml").is_file():
            scenarios_missing.append(name)
        if not (base / "agents").is_dir():
            agents_missing.append(name)
        if not (base / "assets").is_dir():
            assets_missing.append(name)
    return {
        "skill_dirs_total": len(dirs),
        "skills_with_skill_md": len(present),
        "skills_expected": list(EXPECTED_SKILLS),
        "skills_missing": [s for s in EXPECTED_SKILLS if s not in present],
        "skills_unexpected": [s for s in present if s not in EXPECTED_SKILLS],
        "frontmatter_ok": frontmatter_ok,
        "frontmatter_bad": frontmatter_bad,
        "test_md_missing": test_md_missing,
        "scenarios_missing": scenarios_missing,
        "agents_missing": agents_missing,
        "assets_missing": assets_missing,
        "distributions_present": (root / "distributions").is_dir(),
        "resources_present": (root / "resources").is_dir(),
    }


def describe() -> dict:
    """Décrit l'adapter (manifeste machine, sans effet de bord)."""
    return {
        "fiber": FIBER_ADDRESS,
        "fork": FORK,
        "upstream": UPSTREAM_REPO,
        "upstream_branch": UPSTREAM_BRANCH,
        "pinned_upstream_commit": PINNED_UPSTREAM_COMMIT,
        "bind_commit": BIND_COMMIT,
        "bind_layer": BIND_LAYER,
        "license": LICENSE,
        "adapter_version": ADAPTER_VERSION,
        "canonical": CANONICAL,
        "confinement": CONFINEMENT,
        "surface": "validate() -> dict ; doctor() -> list[check] ; describe() -> dict",
    }


def validate() -> dict:
    """Constate l'état de l'inventaire gelé. Aucun appel réseau, aucune écriture."""
    root = _repo_root()
    inv = _skill_inventory(root)
    license_file = root / "LICENSE"
    return {
        "pinned_commit_is_40_hex": bool(re.fullmatch(r"[0-9a-f]{40}", PINNED_UPSTREAM_COMMIT)),
        "license_file_present": license_file.is_file(),
        "license": LICENSE,
        "adapter_network_calls": 0,
        "canonical": CANONICAL,
        "confinement": CONFINEMENT,
        **inv,
        "inventory_coherent": (
            inv["skill_dirs_total"] == 7
            and inv["skills_with_skill_md"] == 7
            and inv["skills_missing"] == []
            and inv["skills_unexpected"] == []
            and inv["frontmatter_bad"] == []
            and inv["test_md_missing"] == []
            and inv["scenarios_missing"] == []
            and inv["agents_missing"] == []
            and inv["assets_missing"] == []
            and inv["distributions_present"]
            and inv["resources_present"]
        ),
    }


def doctor() -> list[dict]:
    """Liste de contrôles sur l'inventaire gelé."""
    v = validate()
    checks = [
        {
            "name": "gel_epingle_40_hex",
            "ok": v["pinned_commit_is_40_hex"],
            "detail": PINNED_UPSTREAM_COMMIT_SHORT,
        },
        {
            "name": "licence_apache_2",
            "ok": v["license_file_present"] and v["license"] == "Apache-2.0",
            "detail": "LICENSE present, Apache-2.0",
        },
        {
            "name": "inventaire_7_skills",
            "ok": v["skill_dirs_total"] == 7 and v["skills_with_skill_md"] == 7,
            "detail": f"{v['skill_dirs_total']} dossiers skills, {v['skills_with_skill_md']} SKILL.md",
        },
        {
            "name": "frontmatter_name_licence_description",
            "ok": v["frontmatter_bad"] == [],
            "detail": f"{len(v['frontmatter_ok'])}/7 frontmatters name + license + description cohérents",
        },
        {
            "name": "test_md_et_scenarios_par_skill",
            "ok": v["test_md_missing"] == [] and v["scenarios_missing"] == [],
            "detail": "7/7 TEST.md, 7/7 test_scenarios.yaml",
        },
        {
            "name": "agents_assets_distributions_resources",
            "ok": v["agents_missing"] == [] and v["assets_missing"] == []
            and v["distributions_present"] and v["resources_present"],
            "detail": "7/7 agents/, 7/7 assets/, distributions/ + resources/ présents",
        },
        {
            "name": "reference_du_canonique",
            "ok": v["canonical"] == "fiber:a0:superpowers",
            "detail": "référence du canonique superpowers (§D5), pas un framework parallèle",
        },
        {
            "name": "adapter_sans_reseau",
            "ok": v["adapter_network_calls"] == 0,
            "detail": "stdlib seule, 0 import réseau, 0 appel sortant",
        },
    ]
    return checks

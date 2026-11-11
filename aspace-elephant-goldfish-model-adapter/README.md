# A'Space adapter — elephant-goldfish-model (référence du canonique)

**Adresse :** `fiber:a0:elephant-goldfish-model` — D-N053 pas C (design Clara, design signé pas C D-C0..D-C3).
**Fork souverain :** `Amdkn/elephant-goldfish-model` (parent `google/elephant-goldfish-model`, branche `main`).
**Gel amont :** `113a3afc44e8f4f54722d7150d5701f65cc8ef7f` (« fix(review): save GoldfishContext URLs as files (#289) »).
**Bind Cordis Fiber (4L) :** `3d643fe7e1272cc7972bd1456ded6ebff32b54e7` — `aspace-plugin.json`, re-appliqué VERBATIM sur `main` au-dessus de l'adapter (F8 D4).
**Licence :** `Apache-2.0`.
**Version adapter :** 0.1.0 — contrat seul, patron pas A/B.

## Ce que fait l'adapter

EGM est une référence du canonique MasterSpec `fiber:a0:superpowers` (§D5) :
7 skills (`skills/egm-*` — `SKILL.md` + `TEST.md` + `test_scenarios.yaml`
chacune, `agents/`, `assets/`), `distributions/`, `resources/`.

Surface : `validate()` (constate : gel, licence, comptage des 7 skills,
frontmatter name + license + description, TEST.md + scénarios présents par
skill, agents/assets/distributions/resources, zéro appel réseau),
`doctor()` (liste de contrôles), `describe()` (manifeste machine).
**Aucun fichier amont touché, aucun appel réseau, aucun poids monté dans le fork.**

Mesures au gel : 7/7 skills avec frontmatter cohérent, 7/7 TEST.md,
7/7 test_scenarios.yaml, 7/7 agents/, 7/7 assets/. Suite amont bornée
(D-C2) : `pytest tests/unit` — 336 passed, 2 skipped au gel.

Gel tenu : dérive 39, amont vivant — pas de re-gel, revisite par signal.
Le fork main portait 3 commits amont au-delà du gel (0dfb5bf, ccf79c5,
6a8001e) ; main ramené au gel avant adaptation, commits préservés verbatim
sur upstream/main — le parent de l'adapter est le gel, per design §3.

## Confinement

Aucun confinement commercial : code et skills Apache-2.0. Usage B2B autorisé
par la licence.

## Tests

```bash
python -m pytest aspace-elephant-goldfish-model-adapter/tests/test_smoke.py -v
```

Suite amont bornée (Node 22, pytest 8.3.5 + pyyaml 6.0.2, TMPDIR hors /tmp
— /tmp tmpfs 512 Mo saturé par les autres pistes) :

```bash
export PATH="$HOME/workspace/.tools/node-v22.21.1-linux-x64/bin:$PATH" TMPDIR=$HOME/workspace/.tmp-pas-c
python -m pytest tests/unit
```

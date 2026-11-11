import json
from pathlib import Path

# 1. Canonical JSON
with open('standards/canonical_skkni_299_2020.json', encoding='utf-8') as f:
    skkni = json.load(f)

print('=== 1. CANONICAL SKKNI JSON ===')
json_dist = {}
for u in skkni['units']:
    u_code = u['unit_code']
    kuks = sum(len(e['performance_criteria']) for e in u['competency_elements'])
    json_dist[u_code] = kuks
    print(f"{u['internal_id']} ({u_code}): {len(u['competency_elements'])} elements, {kuks} KUKs")
print('Total KUKs in canonical JSON:', sum(json_dist.values()))

# 2. Canonical mapping MD
mapping_text = open('reports/canonical_skkni_299_2020_mapping.md', encoding='utf-8').read()
print('\n=== 2. CANONICAL MAPPING MD (lines with unit codes) ===')
for line in mapping_text.splitlines():
    if '| J.62DMI' in line:
        print(line)

# 3. Evidence Registry JSON
with open('reports/evidence/evidence_registry.json', encoding='utf-8') as f:
    reg = json.load(f)

reg_dist = {}
for r in reg['records']:
    uc = r['unit_code']
    reg_dist[uc] = reg_dist.get(uc, 0) + 1

print('\n=== 3. EVIDENCE REGISTRY JSON ===')
for uc, cnt in reg_dist.items():
    print(f'{uc}: {cnt} KUK records')
print('Total in evidence registry:', sum(reg_dist.values()))

# 4. Assessment Readiness Report MD
readiness_text = open('competency/ASSESSMENT_READINESS_REPORT.md', encoding='utf-8').read()
print('\n=== 4. ASSESSMENT READINESS REPORT MD (lines with unit codes) ===')
for line in readiness_text.splitlines():
    if '| `J.62DMI' in line:
        print(line)

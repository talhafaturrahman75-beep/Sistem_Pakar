import json
from math import isclose

def load_rules(path='rules.json'):
    with open(path, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    return rules

def cf_from_mb_md(mb, md):
    return round(mb - md, 6)

def combine_cf(cf1, cf2):
    if cf1 >= 0 and cf2 >= 0:
        return round(cf1 + cf2 * (1 - cf1), 6)
    if cf1 <= 0 and cf2 <= 0:
        return round(cf1 + cf2 * (1 + cf1), 6)
    return round((cf1 + cf2) / (1 - min(abs(cf1), abs(cf2))), 6)

def evaluate(rules, user_facts):
    results = {}
    for rule in rules:
        disease = rule['then']
        evidences = []
        for prem in rule['premises']:
            sym = prem['symptom']
            if sym in user_facts:
                user_conf = user_facts[sym]
                expert_cf = cf_from_mb_md(prem.get('mb',0), prem.get('md',0))
                evid = round(user_conf * expert_cf, 6)
                evidences.append(evid)
        if not evidences:
            continue
        cf_comb = evidences[0]
        for e in evidences[1:]:
            cf_comb = combine_cf(cf_comb, e)
        results[disease] = round(cf_comb, 6)
    sorted_res = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return sorted_res

if __name__ == '__main__':
    rules = load_rules('rules.json')
    user_facts = {
        'desakan untuk kencing': 1.0,
        'kencing di malam hari (nokturia)': 1.0,
        'menggigil': 1.0
    }
    print(evaluate(rules, user_facts))

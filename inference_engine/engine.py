
import json
from math import isclose

def load_rules(path='rules.json'):
    with open(path, 'r', encoding='utf-8') as f:
        rules = json.load(f)
    return rules

def cf_from_mb_md(mb, md):
    return round(mb - md, 6)

def combine_cf(cf1, cf2):
    # Mycin-like combination
    # handle signs
    if cf1 >= 0 and cf2 >= 0:
        return round(cf1 + cf2 * (1 - cf1), 6)
    if cf1 <= 0 and cf2 <= 0:
        return round(cf1 + cf2 * (1 + cf1), 6)
    # conflicting signs
    return round((cf1 + cf2) / (1 - min(abs(cf1), abs(cf2))), 6)

def evaluate(rules, user_facts):
    # user_facts: dict symptom -> user_confidence (0..1)
    results = {}
    for rule in rules:
        disease = rule['then']
        # collect cf evidences for this rule: for each premise that user selected
        evidences = []
        for prem in rule['premises']:
            sym = prem['symptom']
            if sym in user_facts:
                user_conf = user_facts[sym]
                # expert cf for this premise
                expert_cf = cf_from_mb_md(prem.get('mb',0), prem.get('md',0))
                # evidence contributed = user_conf * expert_cf
                evid = round(user_conf * expert_cf, 6)
                evidences.append(evid)
        if not evidences:
            continue
        # combine evidences iteratively
        cf_comb = evidences[0]
        for e in evidences[1:]:
            cf_comb = combine_cf(cf_comb, e)
        results[disease] = round(cf_comb, 6)
    # sort by CF desc
    sorted_res = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return sorted_res

if __name__ == '__main__':
    rules = load_rules('rules.json')
    # example usage
    user_facts = {
        'desakan untuk kencing': 1.0,
        'kencing di malam hari (nokturia)': 1.0,
        'menggigil': 1.0
    }
    print(evaluate(rules, user_facts))

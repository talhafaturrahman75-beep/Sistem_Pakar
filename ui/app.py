from flask import Flask, render_template, request, redirect, url_for
import json, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from inference_engine.engine import load_rules, evaluate

app = Flask(__name__)

RULES_PATH = os.path.join(os.path.dirname(__file__), '..', 'rules.json')
rules = load_rules(RULES_PATH)

symptoms = []
for r in rules:
    for p in r['premises']:
        if p['symptom'] not in symptoms:
            symptoms.append(p['symptom'])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', symptoms=symptoms)

@app.route('/diagnose', methods=['POST'])
def diagnose():
    user_facts = {}
    
    for i, s in enumerate(symptoms):
        sym_key = 'sym_' + str(i)
        conf_key = 'conf_' + sym_key
        
        if sym_key in request.form:
            confidence_str = request.form.get(conf_key, '0.5') # Default ke 0.5 (Mungkin)
            
            try:
                val = float(confidence_str)
            except ValueError:
                val = 0.5
                
            user_facts[s] = val

    results = evaluate(rules, user_facts)
    return render_template('result.html', results=results, user_facts=user_facts)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

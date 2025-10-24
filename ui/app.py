from flask import Flask, render_template, request, redirect, url_for
import json, os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'inference_engine'))
from engine import load_rules, evaluate

app = Flask(__name__)

RULES_PATH = os.path.join(os.path.dirname(__file__), '..', 'rules.json')
rules = load_rules(RULES_PATH)

# gather unique symptoms
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
    
    # Loop menggunakan enumerate untuk mendapatkan index (0, 1, 2, ...)
    for i, s in enumerate(symptoms):
        sym_key = 'sym_' + str(i)
        conf_key = 'conf_' + sym_key # Nama dropdown adalah 'conf_sym_0', 'conf_sym_1', dst.
        
        # Cek HANYA jika checkbox dicentang
        if sym_key in request.form:
            # Ambil nilai dari dropdown yang sesuai
            confidence_str = request.form.get(conf_key, '0.5') # Default ke 0.5 (Mungkin)
            
            try:
                val = float(confidence_str)
            except ValueError:
                val = 0.5 # Fallback
                
            user_facts[s] = val

    results = evaluate(rules, user_facts)
    return render_template('result.html', results=results, user_facts=user_facts)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

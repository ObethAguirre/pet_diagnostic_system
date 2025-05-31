import json
from pathlib import Path
from datetime import datetime
from .automata import create_symptom_validator
from .grammar import create_symptom_grammar
from .turing_machine import create_diagnostic_turing_machine

class DiagnosticSystem:
    def __init__(self):
        self.diseases = self._load_data('diseases.json')
        self.rules = self._load_data('rules.json')
        self.symptom_automaton = create_symptom_validator(self.rules)
        self.symptom_grammar = create_symptom_grammar(self.rules)
        self.turing_machine = create_diagnostic_turing_machine(self.rules)
        self.fast_mode = False
        self.current_species = "perro"  # valor por defecto

    def set_species(self, species):
        if species in {"perro", "gato"}:
            self.current_species = species

    def _load_data(self, filename):
        path = Path(__file__).parent.parent / 'data' / filename
        with open(path, encoding='utf-8') as f:
            return json.load(f)

    def validate_symptoms(self, symptoms):
        invalid = [s for s in symptoms if s not in self.diseases['symptoms']]
        if invalid:
            suggestions = {}
            for s in invalid:
                similar = [k for k in self.diseases['symptoms'] if k.startswith(s[:3]) or s in k]
                suggestions[s] = similar[:3]
            msg = "Síntomas no reconocidos:\n"
            for s, sugg in suggestions.items():
                msg += f"- {s}"
                if sugg:
                    msg += f" (¿Quizás quiso decir: {', '.join(sugg)}?)"
                msg += "\n"
            return False, msg

        symptom_set = set(symptoms)
        for cat, pattern in self.rules['validation_rules']['symptom_patterns'].items():
            if any(s in symptom_set for s in pattern['required']):
                if any(s in symptom_set for s in pattern['exclusions']):
                    conflict = ', '.join(s for s in symptom_set if s in pattern['exclusions'])
                    return False, f"Conflicto: síntomas de {cat} con exclusiones ({conflict})"

        return True, "Validación exitosa"

    def diagnose(self, symptoms):
        valid, msg = self.validate_symptoms(symptoms)
        if not valid:
            return {"error": msg}

        encoding = self.rules['validation_rules']['turing_machine_config']['symptom_encoding']
        encoded = ''.join([encoding.get(s, '#') for s in symptoms])
        is_complex = self.turing_machine.run(encoded)

        threshold = self.rules['diagnostic_parameters']['score_threshold']
        possible = []

        for name, data in self.diseases['diseases'].items():
            if data.get("especie") != self.current_species:
                continue

            matches = set(data['symptoms']) & set(symptoms)
            if not matches:
                continue
            base_score = len(matches) / len(data['symptoms']) * 100
            severity_factor = sum(self.diseases['symptoms'][s]['severity'] for s in matches) / len(matches)
            score = min(100, base_score * severity_factor * (1.3 if is_complex else 1))
            if score >= threshold:
                possible.append({
                    "name": name,
                    "score": round(score, 2),
                    "matches": list(matches),
                    "missing": list(set(data['symptoms']) - matches),
                    "severity": data['severity'],
                    "contagious": data.get('contagioso', False),
                    "treatment": data.get('tratamiento', 'Consulta veterinaria'),
                    "description": data.get('description', '')
                })

        return {
            "input": symptoms,
            "diagnoses": sorted(possible, key=lambda x: (-x['score'], x['severity'] == 'alta')),
            "is_complex": is_complex,
            "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
# Simulación: Implementación de guardado de diagnóstico en archivo .txt

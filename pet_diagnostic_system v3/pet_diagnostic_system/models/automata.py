import json
from pathlib import Path

class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.current_state = initial_state
        self.initial_state = initial_state
        self.final_states = final_states

    def reset(self):
        self.current_state = self.initial_state

    def process_input(self, input_string):
        for symbol in input_string:
            if symbol not in self.alphabet:
                return False
            if (self.current_state, symbol) not in self.transitions:
                return False
            self.current_state = self.transitions[(self.current_state, symbol)]
        return self.current_state in self.final_states

def create_symptom_validator(rules):
    with open(Path(__file__).parent.parent / 'data' / 'diseases.json', 'r') as f:
        diseases_data = json.load(f)
        symptoms_db = set(diseases_data['symptoms'].keys())

    states = {'q0', 'q_digestive', 'q_respiratory', 'q_urinary', 'q_accept'}
    transitions = {}

    for symptom, data in diseases_data['symptoms'].items():
        if data['type'] == 'digestivo':
            transitions[('q0', symptom)] = 'q_digestive'
        elif data['type'] == 'respiratorio':
            transitions[('q0', symptom)] = 'q_respiratory'
        elif data['type'] == 'urinario':
            transitions[('q0', symptom)] = 'q_urinary'

    transitions.update({
        ('q_digestive', 'fiebre'): 'q_accept',
        ('q_respiratory', 'fiebre'): 'q_accept',
        ('q_urinary', 'fiebre'): 'q_accept'
    })

    return FiniteAutomaton(
        states=states,
        alphabet=symptoms_db,
        transitions=transitions,
        initial_state='q0',
        final_states={'q_accept', 'q_digestive', 'q_respiratory', 'q_urinary'}
    )

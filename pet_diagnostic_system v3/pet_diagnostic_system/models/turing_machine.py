class TuringMachine:
    def __init__(self, states, alphabet, tape_alphabet, transitions, initial_state, accept_state, reject_state):
        self.states = states
        self.alphabet = alphabet
        self.tape_alphabet = tape_alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.max_steps = 50

    def run(self, input_tape):
        tape = list(input_tape) if input_tape else ['_']
        head_pos = 0
        current_state = self.initial_state
        steps = 0

        while steps < self.max_steps:
            if current_state in {self.accept_state, self.reject_state}:
                break

            current_symbol = tape[head_pos]
            transition = self.transitions.get((current_state, current_symbol))

            if not transition:
                current_state = self.reject_state
                break

            new_state, new_symbol, direction = transition
            tape[head_pos] = new_symbol
            current_state = new_state

            if direction == 'R':
                head_pos += 1
                if head_pos >= len(tape):
                    tape.append('_')
            elif direction == 'L':
                head_pos = max(0, head_pos - 1)

            steps += 1

        return current_state == self.accept_state

def create_diagnostic_turing_machine(rules):
    config = rules['validation_rules']['turing_machine_config']
    symptom_encoding = config['symptom_encoding']
    complex_patterns = config['complex_patterns']

    states = {'q0', 'qa', 'qr'}
    alphabet = set(symptom_encoding.values())
    tape_alphabet = alphabet | {'_', '#'}

    transitions = {}
    for pattern_name, pattern in complex_patterns.items():
        current_state = 'q0'
        for i, symbol in enumerate(pattern):
            next_state = f'q_{pattern_name}_{i}' if i < len(pattern) - 1 else 'qa'
            transitions[(current_state, symbol)] = (next_state, symbol, 'R')
            states.add(next_state)
            current_state = next_state

    transitions[('q0', '_')] = ('qr', '_', 'R')

    return TuringMachine(
        states=states,
        alphabet=alphabet,
        tape_alphabet=tape_alphabet,
        transitions=transitions,
        initial_state='q0',
        accept_state='qa',
        reject_state='qr'
    )

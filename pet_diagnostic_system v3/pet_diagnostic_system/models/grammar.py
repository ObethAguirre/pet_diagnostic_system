class ContextFreeGrammar:
    def __init__(self, variables, terminals, productions, start_symbol):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.start_symbol = start_symbol

    def is_valid_sequence_top_down(self, sequence):
        def parse(symbols, remaining):
            if not symbols and not remaining:
                return True
            if not symbols or not remaining:
                return False

            current = symbols[0]

            if current in self.terminals:
                if current == remaining[0]:
                    return parse(symbols[1:], remaining[1:])
                return False
            elif current in self.variables:
                for production in self.productions.get(current, []):
                    if parse(production + symbols[1:], remaining):
                        return True
                return False
            return False

        return parse([self.start_symbol], sequence)

    def is_valid_sequence_bottom_up(self, sequence):
        stack = []
        remaining = list(sequence)

        while remaining or len(stack) > 1:
            if remaining:
                stack.append(remaining.pop(0))

            reduced = True
            while reduced and stack:
                reduced = False
                for length in range(min(len(stack), 3), 0, -1):
                    top = stack[-length:]
                    for lhs, rhs_list in self.productions.items():
                        if any(top == rhs for rhs in rhs_list):
                            stack = stack[:-length] + [lhs]
                            reduced = True
                            break
                    if reduced:
                        break

        return len(stack) == 1 and stack[0] == self.start_symbol

def create_symptom_grammar(rules):
    productions = rules['validation_rules']['grammar_productions']
    variables = set(productions.keys())
    terminals = set()

    for rhs_list in productions.values():
        for rhs in rhs_list:
            for symbol in rhs:
                if symbol not in variables:
                    terminals.add(symbol)

    return ContextFreeGrammar(
        variables=variables,
        terminals=terminals,
        productions=productions,
        start_symbol='S'
    )

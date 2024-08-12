# Clase que define un Autómata Finito Determinista (DFA)
class DFA:
    def __init__(self, states, alphabet, transitions, initial_state, accepting_states):
        self.states = states  # Conjunto de todos los estados del DFA
        self.alphabet = alphabet  # Alfabeto (conjunto de símbolos) del DFA
        self.transitions = transitions  # Diccionario que define las transiciones del DFA
        self.initial_state = initial_state  # Estado inicial del DFA
        self.accepting_states = accepting_states  # Conjunto de estados de aceptación del DFA

    def get_transition(self, state, symbol):
        # Devuelve el estado de destino para una transición dada desde 'state' con 'symbol'
        return self.transitions.get((state, symbol), None)

# Función para analizar las transiciones a partir de la entrada
def parse_transitions(input_data, headers):
    lines = input_data.strip().split('\n')  # Divide la entrada en líneas
    transitions = {}  # Diccionario para almacenar las transiciones

    for line in lines:
        values = line.split()  # Divide cada línea en valores separados por espacios
        state = int(values[0])  # El primer valor es el estado de origen
        for i, header in enumerate(headers):
            # Cada par (estado de origen, símbolo) se asocia con el estado de destino
            transitions[(state, header)] = int(values[i + 1])

    return transitions  # Devuelve el diccionario de transiciones

# Función para minimizar el DFA
def minimize_dfa(dfa):
    # Crear pares de estados que pueden ser comparados para ver si son distinguibles
    pairs = [(p, q) for p in dfa.states for q in dfa.states if p < q]
    marked = set()  # Conjunto de pares de estados que se consideran distinguibles

    # Marca pares que son distinguibles desde el inicio (uno es de aceptación y el otro no)
    for (p, q) in pairs:
        if (p in dfa.accepting_states) != (q in dfa.accepting_states):
            marked.add((p, q))

    # Marca pares adicionales según las transiciones
    changes = True
    while changes:
        changes = False
        new_marked = set(marked)  # Nuevo conjunto de pares marcados
        for (p, q) in pairs:
            if (p, q) in marked:
                continue  # Si ya está marcado, no se revisa
            for symbol in dfa.alphabet:
                # Verifica las transiciones de ambos estados bajo el mismo símbolo
                p_next = dfa.get_transition(p, symbol)
                q_next = dfa.get_transition(q, symbol)
                if p_next is not None and q_next is not None:
                    # Marca el par si las transiciones resultan en estados ya marcados como distinguibles
                    if (p_next, q_next) in marked or (q_next, p_next) in marked:
                        new_marked.add((p, q))
                        changes = True
                        break
        marked = new_marked  # Actualiza los pares marcados

    # Crear clases de equivalencia (estados que no son distinguibles)
    equivalence_classes = []
    state_to_class = {}

    for state in dfa.states:
        found = False
        for eq_class in equivalence_classes:
            representative = next(iter(eq_class))
            # Agrupa estados no distinguibles en la misma clase de equivalencia
            if (state, representative) not in marked and (representative, state) not in marked:
                eq_class.add(state)
                state_to_class[state] = eq_class
                found = True
                break
        if not found:
            # Si no pertenece a ninguna clase, crea una nueva clase de equivalencia
            new_class = {state}
            equivalence_classes.append(new_class)
            state_to_class[state] = new_class

    return equivalence_classes  # Devuelve las clases de equivalencia

# Función principal que procesa la entrada y minimiza el DFA
def minimizate():
    states_n = int(input())  # Número de estados del DFA
    alphabet = input().split()  # Alfabeto del DFA
    accepting_states = set(map(int, input().split()))  # Estados de aceptación

    transitions = ""
    for _ in range(states_n):
        transitions += input() + "\n"  # Leer y almacenar las transiciones
    transitions = parse_transitions(transitions, alphabet)  # Analizar las transiciones

    initial_state = 0  # Asumimos que el estado inicial es 0
    states = set(range(states_n))  # Conjunto de estados del DFA
    dfa = DFA(states, set(alphabet), transitions, initial_state, accepting_states)

    partition = minimize_dfa(dfa)  # Minimizar el DFA

    # Ordenar y formatear la salida de las clases de equivalencia
    sorted_partition = sorted([sorted(group) for group in partition if len(group) > 1])
    output = ' '.join(f"({','.join(map(str, group))})" for group in sorted_partition)
    print(output)

# Simulación de la entrada estándar para pruebas
import sys
from io import StringIO

# Datos de entrada simulados
input_data = """4
6
a b
1 2 5
0 1 2
1 3 4
2 4 3
3 5 5 
4 5 5
5 5 5
6
a b
3 4 5
0 1 2
1 3 4
2 4 3
3 5 5 
4 5 5
5 5 5
6
a
1 4
0 1
1 2
2 3
3 4
4 5
5 0
4
a b
0 1
0 1 2
1 1 2
2 3 1
3 3 3"""

# Redirigir la entrada estándar para simular la ejecución con los datos proporcionados
sys.stdin = StringIO(input_data)

# Llamar a la función de minimización para cada conjunto de datos
for _ in range(int(input())):
    minimizate()

from qiskit import QuantumCircuit, Aer, execute
from qiskit.visualization import plot_histogram
import math

def oracle(circuit, qubits, number_to_find):
    """Applies the oracle which flips the phase of the target state."""
    binary_string = format(number_to_find, '0' + str(len(qubits)) + 'b')
    for qubit, bit in enumerate(binary_string):
        if bit == '0':
            circuit.x(qubits[qubit])
    circuit.h(qubits[-1])
    circuit.mcx(qubits[:-1], qubits[-1])
    circuit.h(qubits[-1])
    for qubit, bit in enumerate(binary_string):
        if bit == '0':
            circuit.x(qubits[qubit])

def diffuser(circuit, qubits):
    """Applies the diffuser to amplify the probability of the marked state."""
    circuit.h(qubits)
    circuit.x(qubits)
    circuit.h(qubits[-1])
    circuit.mcx(qubits[:-1], qubits[-1])
    circuit.h(qubits[-1])
    circuit.x(qubits)
    circuit.h(qubits)

def grover_search(number_to_find, n_qubits):
    """Implements Grover's algorithm."""
    qc = QuantumCircuit(n_qubits, n_qubits)

    # Apply Hadamard gates to all qubits
    qc.h(range(n_qubits))

    # Apply Grover iterations
    num_iterations = int(math.sqrt(2**n_qubits))
    for _ in range(num_iterations):
        oracle(qc, range(n_qubits), number_to_find)
        diffuser(qc, range(n_qubits))

    # Measure the qubits
    qc.measure(range(n_qubits), range(n_qubits))

    # Run the circuit on a simulator
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend=simulator, shots=1024).result()
    counts = result.get_counts()

    return counts

if __name__ == "__main__":
    # User input
    number_to_find = int(input("Enter a number to search for (between 0 and 7): "))
    
    # Number of qubits required
    n_qubits = 3
    
    # Run Grover's algorithm
    result = grover_search(number_to_find, n_qubits)
    
    # Display the result
    print(f"Result of Grover's search for {number_to_find}: {result}")
    plot_histogram(result).show()

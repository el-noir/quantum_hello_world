<h1>Hello World on a 2-Qubit Bell State & GHZ State Analysis using Qiskit</h1>

<p>This project demonstrates how to create and analyze quantum states using Qiskit, a powerful open-source framework for quantum computing. The project covers the following key areas:</p>

<ol>
    <li>Creating a 2-Qubit Bell State</li>
    <li>Measuring Quantum Observables</li>
    <li>Generating and Analyzing an n-Qubit GHZ State</li>
</ol>

<h2>1. Creating a 2-Qubit Bell State</h2>

<p>We start by creating a simple quantum circuit that generates a 2-qubit Bell state, a fundamental example of quantum entanglement.</p>

<pre><code>from qiskit import QuantumCircuit

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

qc.draw(output='mpl')
</code></pre>

<h3>Explanation:</h3>
<ul>
    <li><strong>Hadamard Gate (H)</strong>: Applied to the first qubit to create a superposition state.</li>
    <li><strong>CNOT Gate (CX)</strong>: Entangles the first qubit with the second, creating a Bell state.</li>
</ul>

<h3>Visualization:</h3>
<p>The quantum circuit can be visualized as follows:</p>
<img src="path_to_image" alt="Bell State Circuit" />

<h2>2. Measuring Quantum Observables</h2>

<p>Next, we measure the expectation values of various Pauli observables on the Bell state.</p>

<pre><code>from qiskit.quantum_info import Pauli

# Define the observables
ZZ = Pauli('ZZ')
ZI = Pauli('ZI')
IZ = Pauli('IZ')
XX = Pauli('XX')
XI = Pauli('XI')
IX = Pauli('IX')

observables = [ZZ, ZI, IZ, XX, XI, IX]

from qiskit_aer.primitives import Estimator

estimator = Estimator()
job = estimator.run([qc] * len(observables), observables)

job.result()
</code></pre>

<h3>Explanation:</h3>
<ul>
    <li><strong>Pauli Observables</strong>: Various Pauli operators (like ZZ, ZI, IZ, etc.) are used to measure different aspects of the quantum state.</li>
    <li><strong>Estimator</strong>: Qiskit's Estimator is used to calculate the expectation values for each observable.</li>
</ul>

<h3>Visualization:</h3>
<p>The expectation values are plotted to show how different observables behave on the Bell state:</p>

<pre><code>import matplotlib.pyplot as plt

data = ['ZZ', 'ZI', 'IZ', 'XX', 'XI', 'IX']
values = job.result().values

plt.plot(data, values, '-o')
plt.xlabel('Observables')
plt.ylabel('Expectation Value')
plt.show()
</code></pre>
<img src="path_to_image" alt="Expectation Values" />

<h2>3. Generating and Analyzing an n-Qubit GHZ State</h2>

<p>We further explore quantum entanglement by creating and analyzing an n-qubit GHZ (Greenberger–Horne–Zeilinger) state.</p>

<pre><code>def get_qc_for_n_qubit_GHZ_state(n):
    qc = QuantumCircuit(n)
    qc.h(0)
    for i in range(n-1):
        qc.cx(i, i+1)
    return qc

n = 10
qc = get_qc_for_n_qubit_GHZ_state(n)
qc.draw(output='mpl')
</code></pre>

<h3>Explanation:</h3>
<ul>
    <li><strong>GHZ State</strong>: A GHZ state is a maximally entangled state involving multiple qubits. This function generates a GHZ state for any number of qubits <code>n</code>.</li>
</ul>

<h3>Visualization:</h3>
<p>The GHZ circuit for 10 qubits is drawn:</p>
<img src="path_to_image" alt="GHZ State Circuit" />

<h3>Operator Definition and Transpilation:</h3>
<p>To measure correlations between qubits, we define specific operators and transpile the circuit for execution on a real quantum backend.</p>

<pre><code>from qiskit.quantum_info import SparsePauliOp

# Define operators for GHZ state
operator_strings = ['Z' + 'I' * i + 'Z' + 'I' * (n-2-i) for i in range(n-1)]
operators = [SparsePauliOp(operator_string) for operator_string in operator_strings]

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

backend_name = "ibm_brisbane"
backend = QiskitRuntimeService().get_backend(backend_name)
pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)

qc_transpiled = pass_manager.run(qc)
operators_transpiled_list = [op.apply_layout(qc_transpiled.layout) for op in operators]
</code></pre>

<h3>Explanation:</h3>
<ul>
    <li><strong>SparsePauliOp</strong>: These operators are defined to measure correlations between pairs of qubits in the GHZ state.</li>
    <li><strong>Transpilation</strong>: The circuit is optimized and mapped to the specific qubit layout of the chosen backend (<code>ibm_brisbane</code>).</li>
</ul>

<h3>Execution on Quantum Backend:</h3>
<p>The GHZ circuit is executed on IBM's quantum backend with specific options for resilience and optimization.</p>

<pre><code>from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit_ibm_runtime import EstimatorOptions

options = EstimatorOptions()
options.resilience_level = 1
options.optimization_level = 0
options.dynamical_decoupling.enable = True
options.dynamical_decoupling.sequence_type = "XY4"

estimator = Estimator(backend, options=options)
job = estimator.run([(qc_transpiled, operators_transpiled_list)])
job_id = job.job_id()
print(job_id)
</code></pre>

<h3>Explanation:</h3>
<ul>
    <li><strong>Dynamical Decoupling</strong>: Applied to reduce decoherence in the quantum system during execution.</li>
    <li><strong>Job Execution</strong>: The job is submitted to the quantum backend, and the job ID is stored for later retrieval.</li>
</ul>

<h3>Post-Processing and Visualization:</h3>
<p>The results are normalized and plotted to visualize the correlations between qubits in the GHZ state.</p>

<pre><code>job_id = 'cv38swzhdzz0008mf1s0'
service = QiskitRuntimeService()
job = service.job(job_id)

data = list(range(1, len(operators) + 1))
result = job.result()[0]
values = result.data.evs
values = [v/values[0] for v in values]

plt.scatter(data, values, marker='o', label='100-qubit GHZ state')
plt.xlabel('Distance between qubits $i$')
plt.ylabel(r'\langle Z_0 Z_i \range / \langle Z_0 Z_1 \rangle$')
plt.legend()
plt.show()
</code></pre>
<img src="path_to_image" alt="GHZ State Correlations" />

<h2>Conclusion</h2>
<p>This project demonstrates the creation, manipulation, and analysis of quantum states using Qiskit. From simple 2-qubit Bell states to more complex 10-qubit GHZ states, the project showcases how to measure and visualize quantum entanglement and correlations on real quantum hardware.</p>

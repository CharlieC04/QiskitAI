from qiskit import transpile, transpiler, qasm2


class QuantumPlatform:
    def __init__(self, provider = None, backend_name = None):
        self.provider = None
        self.backend = None
        self.transpiled_qc = None
        self.provider = provider
        if self.provider is None:
            raise "Cannot initialize quantum provider"

        if backend_name is not None:
            self.backend = self.provider.get_backend(backend_name)
            if self.backend is None:
                raise f'Cannot initialize backend {backend_name}'

    def get_provider(self):
        return self.provider

    def get_backend_info(self, coupling_map_filename=None, target_info_filename=None):
        print(f'Backends={self.provider.backends()}')
        print(f'Operation names={self.backend.operation_names}')
#        print(f'Properties={self.backend.properties()}')
#        print(f'Configuration={self.backend.configuration()}')
#        print(f'Status={self.backend.status()}')
        print(f'Options={self.backend.options}')

#        if target_info_filename is not None:
#            f = open(target_info_filename, "w")
#            f.write(self.backend.target)
#            f.close()

        if coupling_map_filename is not None:
            coupling_map = transpiler.CouplingMap(self.backend.coupling_map)
            image = coupling_map.draw()
            image.save(coupling_map_filename)

    def get_backend(self):
        return self.backend

    def schedule_job(self, circuit, shots=1, dry_run=False,
                     qc_filename=None, qc_image_filename=None,
                     transpiled_filename=None, transpiled_image_filename=None):
        if qc_filename is not None:
            qasm2.dump(circuit, qc_filename)
        if qc_image_filename is not None:
            circuit.draw(output='mpl', filename=qc_image_filename)
        self.transpiled_qc = transpile(circuit, self.backend)
        if transpiled_filename is not None:
            qasm2.dump(self.transpiled_qc, transpiled_filename)
        if transpiled_image_filename is not None:
            self.transpiled_qc.draw(output='mpl', filename=transpiled_image_filename)

        if dry_run is True: return None
        return self.backend.run(self.transpiled_qc, shots=shots)

    def get_async_job(self, job_id):
        return self.provider.retrieve_job(job_id)

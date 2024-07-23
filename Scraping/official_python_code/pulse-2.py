from qiskit import execute, pulse

d0 = pulse.DriveChannel(0)

with pulse.build() as pulse_prog:
    pulse.play(pulse.Constant(100, 1.0), d0)

pulse_prog.draw()
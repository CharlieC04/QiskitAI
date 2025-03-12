from qiskit import pulse
from qiskit_ibm_runtime.fake_provider import FakeBelemV2
from qiskit.pulse import DriveChannel, Constant, Play, Delay
def pulse_schedule_with_constant_and_delay():
    """ Using Qiskit Pulse, create a schedule with a constant pulse on drive channel 0, featuring a duration of 160 and an amplitude of 0.1 and name this schedule "pulse_schedule_with_constant_and_delay". Use the FakeBelem backend for configuration. After creating the pulse, add a delay of 400 to the schedule, then replay the same pulse. Return the completed pulse schedule.
    """
    pulse_schedule = pulse.Schedule()
    pulse_schedule.append(Constant(duration=160, amp=0.1, name="pulse_schedule_with_constant_and_delay"), DriveChannel(0))
    pulse_schedule.delay(400)
    pulse_schedule.append(pulse_schedule.instructions[0].inverse(), pulse_schedule.instructions[0].channels)
    pulse_schedule.play(pulse_schedule.instructions[0], DriveChannel(0))
    return pulse_schedule

backend = FakeBelemV2()
pulse_schedule = pulse_schedule_with_constant_and_delay()
pulse_schedule.draw(backend)
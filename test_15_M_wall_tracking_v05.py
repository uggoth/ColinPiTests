module_name = 'test_15_M_wall_tracking_v04.py'
print (module_name,'starting')
print ('expects main_autonomous to be running on the Pico')

from importlib.machinery import SourceFileLoader
data_module = SourceFileLoader('Colin', '/home/pi/ColinThisPi/ColinData.py').load_module()
data_object = data_module.ColinData()
data_values = data_object.params
ColObjectsVersion = data_values['ColObjects']
col_objects_name = '/home/pi/ColinPiClasses/' + ColObjectsVersion + '.py'
ColObjects = SourceFileLoader('ColObjects', col_objects_name).load_module()
ThisPiVersion = data_values['ThisPi']
ThisPi = SourceFileLoader('ThisPi', '/home/pi/ColinThisPi/' + ThisPiVersion + '.py').load_module()
CommandStream = SourceFileLoader('CommandStream', '/home/pi/ColinPiClasses/' + data_values['CommandStream'] + '.py').load_module()
from vl53l5cx.vl53l5cx import VL53L5CX
import time
import sys
import pigpio
gpio = pigpio.pi()
my_ultrasonics = ThisPi.Ultrasonics(gpio)
my_front_ultrasonic = my_ultrasonics.front_ultrasonic.instance

def front_ok(distance=335):
    front_mms = my_front_ultrasonic.read_mms()
    if front_mms < distance:
        return True
    else:
        return False

def get_offsets():
    mmus = my_front_ultrasonic.read_mms()
    max_fails = 5
    for i in range(max_fails):
        if driver.check_data_ready():
            ranging_data = driver.get_ranging_data()
            st15 = ranging_data.target_status[driver.nb_target_per_zone * 15]
            st11 = ranging_data.target_status[driver.nb_target_per_zone * 11]
            st07 = ranging_data.target_status[driver.nb_target_per_zone * 7]
            st03 = ranging_data.target_status[driver.nb_target_per_zone * 3]
            if ((st15 == 5) and (st11 == 5) and (st07 == 5) and (st03 == 5)):
                mm15 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 15])
                mm11 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 11])
                mm07 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 7])
                mm03 = int(ranging_data.distance_mm[driver.nb_target_per_zone * 3])
                return True, mm15, mm11, mm07, mm03, mmus
    print ('**** No vl53 ranging data found within ',max_fails,'attempts ****')
    return False, 0.0, 0.0, 0.0, 0.0, 0.0
        
def check_straight():
    success, mm15, mm11, mm07, mm03, mmus = get_offsets
    if success:
        left = (mm15+mm11)/2
        right = (mm07+mm03)/2
        diff = left-right
        print ('diff:{:4}  mm15:{:4}  mm11:{:4}  mm07:{:4}  mm03:{:4}  mmus:{:4}'.format(
            diff, mm15, mm11, mm07, mm03, mmus))
        return True, diff
    else:
        return False, 0

def straighten_up(attempts):
    success = False
    left_count = 0
    right_count = 0
    for i in range(attempts):
        time.sleep(0.05)
        ok, diff = check_straight()
        if ok:
            if abs(diff) < 4:
                print ('Straight', diff)
                success = True
                break
            if diff < 0:
                command = 'TRNL0030'
                print (command)
                left_count += 1
            else:
                command = 'TRNR0030'
                print (command)
                right_count += 1
            my_pico.send_command('0000', command)
        else:
            print ('No diff')
    if left_count > right_count:
        direction = 'LEFT'
    elif right_count > left_count:
        direction = 'RIGHT'
    else:
        direction = 'NONE'
    return success, direction, left_count, right_count

def next_command(command):
    global serial_no
    serial_no += 1
    serial_no_string = '{:04}'.format(serial_no)
    return my_pico.send_command(serial_no_string, command)
   
def wait_for_blue(blue_button, poll_loops):
    flash_interval = 7
    flip_flop = False
    for i in range(poll_loops):
        time.sleep(0.01)
        if gpio.read(blue_button) == 0:
            return True
        if i%flash_interval == 0:
            flip_flop = not flip_flop
            if flip_flop:
                next_command('SGRN')
            else:
                next_command('SOFF')
    return False

class PID_A():
    def __init__(self, setpoint):
        self.name = 'crude PID'
        self.setpoint = setpoint
        self.base_throttle = 40
        self.previous_offset = 0
        self.previous_angle = 'ANGLE_OK'
        self.offset_vagueness = 5
        self.max_offset = self.setpoint * 2

    def __call__(self, mm03):
        self.too_close = self.setpoint - (self.offset_vagueness * 2)
        self.too_far = self.setpoint + (self.offset_vagueness * 3)
        avg_offset = mm03

        if avg_offset < self.too_close:
            offset = 'TOO_CLOSE'
        elif avg_offset > self.too_far:
            offset = 'TOO_FAR'
        else:
            offset = 'DISTANCE_OK'

        if avg_offset < (self.previous_offset - self.offset_vagueness):
            angle = 'CLOSING'
        elif avg_offset > (self.previous_offset + self.offset_vagueness):
            angle = 'OPENING'
        else:
            angle = 'ANGLE_OK'
            
        steering_info = offset + ' ' + angle + ' ' + self.previous_angle
        steering_calc = {
            'TOO_CLOSE OPENING OPENING': 0,
            'TOO_CLOSE CLOSING OPENING': 30,
            'TOO_CLOSE ANGLE_OK OPENING': 20,
            'TOO_FAR OPENING OPENING':-30,
            'TOO_FAR CLOSING OPENING':-6,
            'TOO_FAR ANGLE_OK OPENING':-20,
            'DISTANCE_OK OPENING OPENING':-0,
            'DISTANCE_OK CLOSING OPENING':0,
            'DISTANCE_OK ANGLE_OK OPENING':0,

            'TOO_CLOSE OPENING CLOSING': 0,
            'TOO_CLOSE CLOSING CLOSING': 30,
            'TOO_CLOSE ANGLE_OK CLOSING': 10,
            'TOO_FAR OPENING CLOSING':-20,
            'TOO_FAR CLOSING CLOSING':-6,
            'TOO_FAR ANGLE_OK CLOSING':-20,
            'DISTANCE_OK OPENING CLOSING':-6,
            'DISTANCE_OK CLOSING CLOSING':-6,
            'DISTANCE_OK ANGLE_OK CLOSING':0,

            'TOO_CLOSE OPENING ANGLE_OK': 10,
            'TOO_CLOSE CLOSING ANGLE_OK': 40,
            'TOO_CLOSE ANGLE_OK ANGLE_OK': 20,
            'TOO_FAR OPENING ANGLE_OK':-20,
            'TOO_FAR CLOSING ANGLE_OK':-6,
            'TOO_FAR ANGLE_OK ANGLE_OK':-20,
            'DISTANCE_OK OPENING ANGLE_OK':-6,
            'DISTANCE_OK CLOSING ANGLE_OK':-6,
            'DISTANCE_OK ANGLE_OK ANGLE_OK':0
            }

        steering = steering_calc[steering_info]
        self.previous_offset = avg_offset
        self.previous_angle = angle
        return steering

def _clamp(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif (upper is not None) and (value > upper):
        return upper
    elif (lower is not None) and (value < lower):
        return lower
    return value

class PID(object):
    """A simple PID controller."""

    def __init__(
        self,
        Kp=1.0,
        Ki=0.0,
        Kd=0.0,
        setpoint=0,
        sample_time=0.01,
        output_limits=(None, None),
        auto_mode=True,
        proportional_on_measurement=False,
        differential_on_measurement=True,
        error_map=None,
        time_fn=None,
        starting_output=0.0,
    ):
        """
        Initialize a new PID controller.

        :param Kp: The value for the proportional gain Kp
        :param Ki: The value for the integral gain Ki
        :param Kd: The value for the derivative gain Kd
        :param setpoint: The initial setpoint that the PID will try to achieve
        :param sample_time: The time in seconds which the controller should wait before generating
            a new output value. The PID works best when it is constantly called (eg. during a
            loop), but with a sample time set so that the time difference between each update is
            (close to) constant. If set to None, the PID will compute a new output value every time
            it is called.
        :param output_limits: The initial output limits to use, given as an iterable with 2
            elements, for example: (lower, upper). The output will never go below the lower limit
            or above the upper limit. Either of the limits can also be set to None to have no limit
            in that direction. Setting output limits also avoids integral windup, since the
            integral term will never be allowed to grow outside of the limits.
        :param auto_mode: Whether the controller should be enabled (auto mode) or not (manual mode)
        :param proportional_on_measurement: Whether the proportional term should be calculated on
            the input directly rather than on the error (which is the traditional way). Using
            proportional-on-measurement avoids overshoot for some types of systems.
        :param differential_on_measurement: Whether the differential term should be calculated on
            the input directly rather than on the error (which is the traditional way).
        :param error_map: Function to transform the error value in another constrained value.
        :param time_fn: The function to use for getting the current time, or None to use the
            default. This should be a function taking no arguments and returning a number
            representing the current time. The default is to use time.monotonic() if available,
            otherwise time.time().
        :param starting_output: The starting point for the PID's output. If you start controlling
            a system that is already at the setpoint, you can set this to your best guess at what
            output the PID should give when first calling it to avoid the PID outputting zero and
            moving the system away from the setpoint.
        """
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.setpoint = setpoint
        self.sample_time = sample_time

        self._min_output, self._max_output = None, None
        self._auto_mode = auto_mode
        self.proportional_on_measurement = proportional_on_measurement
        self.differential_on_measurement = differential_on_measurement
        self.error_map = error_map

        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._last_time = None
        self._last_output = None
        self._last_error = None
        self._last_input = None

        if time_fn is not None:
            # Use the user supplied time function
            self.time_fn = time_fn
        else:
            import time

            try:
                # Get monotonic time to ensure that time deltas are always positive
                self.time_fn = time.monotonic
            except AttributeError:
                # time.monotonic() not available (using python < 3.3), fallback to time.time()
                self.time_fn = time.time

        self.output_limits = output_limits
        self.reset()

        # Set initial state of the controller
        self._integral = _clamp(starting_output, output_limits)

    def __call__(self, input_, dt=None):
        """
        Update the PID controller.

        Call the PID controller with *input_* and calculate and return a control output if
        sample_time seconds has passed since the last update. If no new output is calculated,
        return the previous output instead (or None if no value has been calculated yet).

        :param dt: If set, uses this value for timestep instead of real time. This can be used in
            simulations when simulation time is different from real time.
        """
        if not self.auto_mode:
            return self._last_output

        now = self.time_fn()
        if dt is None:
            dt = now - self._last_time if (now - self._last_time) else 1e-16
        elif dt <= 0:
            raise ValueError('dt has negative value {}, must be positive'.format(dt))

        if self.sample_time is not None and dt < self.sample_time and self._last_output is not None:
            # Only update every sample_time seconds
            return self._last_output

        # Compute error terms
        error = self.setpoint - input_
        d_input = input_ - (self._last_input if (self._last_input is not None) else input_)
        d_error = error - (self._last_error if (self._last_error is not None) else error)

        # Check if must map the error
        if self.error_map is not None:
            error = self.error_map(error)

        # Compute the proportional term
        if not self.proportional_on_measurement:
            # Regular proportional-on-error, simply set the proportional term
            self._proportional = self.Kp * error
        else:
            # Add the proportional error on measurement to error_sum
            self._proportional -= self.Kp * d_input

        # Compute integral and derivative terms
        self._integral += self.Ki * error * dt
        self._integral = _clamp(self._integral, self.output_limits)  # Avoid integral windup

        if self.differential_on_measurement:
            self._derivative = -self.Kd * d_input / dt
        else:
            self._derivative = self.Kd * d_error / dt

        # Compute final output
        output = self._proportional + self._integral + self._derivative
        output = _clamp(output, self.output_limits)

        # Keep track of state
        self._last_output = output
        self._last_input = input_
        self._last_error = error
        self._last_time = now

        return output

    def __repr__(self):
        return (
            '{self.__class__.__name__}('
            'Kp={self.Kp!r}, Ki={self.Ki!r}, Kd={self.Kd!r}, '
            'setpoint={self.setpoint!r}, sample_time={self.sample_time!r}, '
            'output_limits={self.output_limits!r}, auto_mode={self.auto_mode!r}, '
            'proportional_on_measurement={self.proportional_on_measurement!r}, '
            'differential_on_measurement={self.differential_on_measurement!r}, '
            'error_map={self.error_map!r}'
            ')'
        ).format(self=self)

    @property
    def components(self):
        """
        The P-, I- and D-terms from the last computation as separate components as a tuple. Useful
        for visualizing what the controller is doing or when tuning hard-to-tune systems.
        """
        return self._proportional, self._integral, self._derivative

    @property
    def tunings(self):
        """The tunings used by the controller as a tuple: (Kp, Ki, Kd)."""
        return self.Kp, self.Ki, self.Kd

    @tunings.setter
    def tunings(self, tunings):
        """Set the PID tunings."""
        self.Kp, self.Ki, self.Kd = tunings

    @property
    def auto_mode(self):
        """Whether the controller is currently enabled (in auto mode) or not."""
        return self._auto_mode

    @auto_mode.setter
    def auto_mode(self, enabled):
        """Enable or disable the PID controller."""
        self.set_auto_mode(enabled)

    def set_auto_mode(self, enabled, last_output=None):
        """
        Enable or disable the PID controller, optionally setting the last output value.

        This is useful if some system has been manually controlled and if the PID should take over.
        In that case, disable the PID by setting auto mode to False and later when the PID should
        be turned back on, pass the last output variable (the control variable) and it will be set
        as the starting I-term when the PID is set to auto mode.

        :param enabled: Whether auto mode should be enabled, True or False
        :param last_output: The last output, or the control variable, that the PID should start
            from when going from manual mode to auto mode. Has no effect if the PID is already in
            auto mode.
        """
        if enabled and not self._auto_mode:
            # Switching from manual mode to auto, reset
            self.reset()

            self._integral = last_output if (last_output is not None) else 0
            self._integral = _clamp(self._integral, self.output_limits)

        self._auto_mode = enabled

    @property
    def output_limits(self):
        """
        The current output limits as a 2-tuple: (lower, upper).

        See also the *output_limits* parameter in :meth:`PID.__init__`.
        """
        return self._min_output, self._max_output

    @output_limits.setter
    def output_limits(self, limits):
        """Set the output limits."""
        if limits is None:
            self._min_output, self._max_output = None, None
            return

        min_output, max_output = limits

        if (None not in limits) and (max_output < min_output):
            raise ValueError('lower limit must be less than upper limit')

        self._min_output = min_output
        self._max_output = max_output

        self._integral = _clamp(self._integral, self.output_limits)
        self._last_output = _clamp(self._last_output, self.output_limits)

    def reset(self):
        """
        Reset the PID controller internals.

        This sets each term to 0 as well as clearing the integral, the last output and the last
        input (derivative calculation).
        """
        self._proportional = 0
        self._integral = 0
        self._derivative = 0

        self._integral = _clamp(self._integral, self.output_limits)

        self._last_time = self.time_fn()
        self._last_output = None
        self._last_input = None

class PID_B():
    def __init__(self, setpoint):
        self.name = 'simple PID'
        self.setpoint = setpoint
        self.simple_pid = PID(1.0, 0.0, 0.0, self.setpoint)
    def __call__(self, new_reading):
        self.new_control = self.simple_pid(new_reading)
        return self.new_control

serial_no = 1

my_pid = PID_B()
handshake = CommandStream.Handshake('picoa hs', 4, gpio)
pico_id = 'PICOA'
my_pico = CommandStream.Pico(pico_id, gpio, handshake)
if not my_pico.valid:
    print ('*** NO PICO')
    sys.exit(1)
next_command('STOP')
pwren = 17
gpio.set_mode(pwren, pigpio.OUTPUT)
gpio.write(pwren,1)
driver = VL53L5CX()
alive = driver.is_alive()
if not alive:
    raise IOError("VL53L5CX Device is not alive")
print("Initialising...")
t = time.time()
driver.init()
driver.set_resolution(4*4)
driver.set_ranging_frequency_hz(40)
driver.start_ranging()
print(f"Initialised ({time.time() - t:.1f}s)")
print ('Now waiting for blue button')
blue_button = 16
gpio.set_mode(blue_button, pigpio.INPUT)
gpio.set_pull_up_down(blue_button, pigpio.PUD_UP)

max_not_ready = 100
max_bad_status = 100
no_zones = 16
interval = 300  #  milliseconds
legs = ['TRNR','TRNR','TRNL','TRNL','TRNR','STOP']
leg = 0
not_ready = 0
bad_status = 0
steering = 0
delay = 0

throttle = 40
previous_offset = 0
previous_angle = 'ANGLE_OK'
check_loops = 40

while True:
    if wait_for_blue(blue_button, 500000):
        print ('Blue button pressed. Starting ...')
    else:
        print ('Blue button not pressed. Start again')
        continue
    next_command('SGRN')
    time.sleep(4)
    next_command('SBLU')

    command = 'DRIV{:04}{:04}{:04}'.format(steering, throttle, delay)
    print (next_command(command))

    for i in range(check_loops):
        if gpio.read(blue_button) == 0:
            break
        if not front_ok:
            print ('Hit Front')
            break
        success, mm15, mm11, mm07, mm03, mmus = get_offsets()
        if not success:
            print ('**** no offsets ****')
            break
        if mm03 > 350:
            print ('STOPPING BECAUSE OF LARGE OFFSET', avg_offset)
            break
        avg_offset = mm03
        steering = my_pid(avg_offset)
        abs_steering = abs(steering)
        if abs_steering > 15:
            throttle_m = int(throttle * 0.8)
        elif abs_steering < 5:
            throttle_m = int(throttle * 1.2)
        else:
            throttle_m = throttle
        command = 'DRIV{:4}{:4}{:4}'.format(steering, throttle_m, delay)
        print ('offs:{:3} steer:{:3}'.format(avg_offset, steering), '\n',
               steering_info, command, next_command(command), '\n')
        time.sleep(interval / 1000.0)
    if success and not stopping:
        print ('STOPPING BECAUSE OF LOOP LIMIT')
    command = 'STOP'
    print (next_command(command))

time.sleep(1)
next_command('STOP')

my_ultrasonics.close()
my_pico.close()
handshake.close()
print (module_name, 'finished')

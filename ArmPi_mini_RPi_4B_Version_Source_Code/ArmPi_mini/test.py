import requests
import json
import time

def send_command(method, params=None):
    url = "http://localhost:9030/jsonrpc"
    headers = {'content-type': 'application/json'}
    
    payload = {
        "method": method,
        "params": params if params else [],
        "jsonrpc": "2.0",
        "id": 1,
    }
    
    response = requests.post(url, data=json.dumps(payload), headers=headers).json()
    return response

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def pulse_to_angle(pulse):
    return map_value(pulse, 500, 2500, 90, -90)

# # Servo 1 movements
# send_command("SetPWMServo", [300, 1, 1, pulse_to_angle(1650)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 1, pulse_to_angle(1500)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 1, pulse_to_angle(1650)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 1, pulse_to_angle(1500)])
# time.sleep(1.5)

# # Servo 3 movements
# send_command("SetPWMServo", [300, 1, 3, pulse_to_angle(645)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 3, pulse_to_angle(745)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 3, pulse_to_angle(695)])
# time.sleep(1.5)

# # Servo 4 movements
# send_command("SetPWMServo", [300, 1, 4, pulse_to_angle(2365)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 4, pulse_to_angle(2465)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 4, pulse_to_angle(2415)])
# time.sleep(1.5)

# # Servo 5 movements
# send_command("SetPWMServo", [300, 1, 5, pulse_to_angle(730)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 5, pulse_to_angle(830)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 5, pulse_to_angle(780)])
# time.sleep(1.5)

# # Servo 6 movements
# send_command("SetPWMServo", [300, 1, 6, pulse_to_angle(1450)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 6, pulse_to_angle(1550)])
# time.sleep(0.3)
# send_command("SetPWMServo", [300, 1, 6, pulse_to_angle(1500)])
# time.sleep(1.5)

# # Servo 1 (GRIPPER): More pronounced movement
# send_command("SetPWMServo", [500, 1, 1, pulse_to_angle(1800)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 1, pulse_to_angle(1200)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 1, pulse_to_angle(1800)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 1, pulse_to_angle(1500)])  # Return to center
# time.sleep(1.5)

# # Servo 3: More pronounced movement
# send_command("SetPWMServo", [500, 1, 3, pulse_to_angle(545)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 3, pulse_to_angle(845)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 3, pulse_to_angle(695)])  # Return to middle position
# time.sleep(1.5)

# # Servo 4: More pronounced movement
# send_command("SetPWMServo", [500, 1, 4, pulse_to_angle(2265)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 4, pulse_to_angle(2565)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 4, pulse_to_angle(2415)])  # Return to middle position
# time.sleep(1.5)

# # Servo 5: More pronounced movement
# send_command("SetPWMServo", [500, 1, 5, pulse_to_angle(630)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 5, pulse_to_angle(930)])  # Increased range
# time.sleep(1.5)
# send_command("SetPWMServo", [500, 1, 5, pulse_to_angle(780)])  # Return to middle position
# time.sleep(1.5)

# send_command("SetPWMServo", [500, 1, 5, pulse_to_angle(2365)])  # Increased range
# time.sleep(1.5)
# send_command("SetPWMServo", [500, 1, 5, 3000])  # Return to middle position
# time.sleep(1.5)

# # Servo 6: More pronounced movement
# send_command("SetPWMServo", [500, 1, 6, pulse_to_angle(1350)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 6, pulse_to_angle(1650)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 6, pulse_to_angle(1500)])  # Return to center position
# time.sleep(1.5)

# for i in range(3):
# send_command("MoveArmToPosition", [0, 6, 18, 1000])
# time.sleep(1.2)
# # DOWN AND TO THE RIGHT
# send_command("MoveArmToPosition", [3, 6, 22, 1000])
# time.sleep(1.2)
# ALL THE WAY DOWN AND TO THE RIGHT
# send_command("MoveArmToPosition", [1, 0, -15, 1000])
# time.sleep(1.2)

# set angles
# send_command("SetPWMServoAngle", [6, 90])
# time.sleep(1.5)
# send_command("SetPWMServoAngle", [6, 0])
# time.sleep(1.5)
# send_command("SetPWMServoAngle", [5, 100])
# time.sleep(.5)
# send_command("SetPWMServoAngle", [3, 0])
# time.sleep(.5)
# send_command("SetPWMServoAngle", [4, 179])
# time.sleep(1)
# send_command("SetPWMServoAngle", [3, 10])
# time.sleep(.5)
# send_command("SetPWMServoAngle", [4, 100])
# time.sleep(.5)
# send_command("SetPWMServoAngle", [5, 40])
# time.sleep(.5)
# send_command("SetPWMServoAngle", [4, 150])
# time.sleep(.5)
# send_command("SetPWMServoAngle", [6, 90])
# time.sleep(.5)
# send_command("SetPWMServoAngle", [5, 100])
# time.sleep(.5)
# send_command("SetPWMServoAngle", [3, 0])
# time.sleep(.5)

def home_position():
    send_command("SetPWMServoAngle", [3, 10])
    time.sleep(.5)
    send_command("SetPWMServoAngle", [4, 150])
    time.sleep(.5)
    send_command("SetPWMServoAngle", [5, 40])
    time.sleep(.5)
    send_command("SetPWMServoAngle", [6, 90])
    time.sleep(.5)

def turn_right_bend_down():
    send_command("SetPWMServoAngle", [6, 0])
    time.sleep(.5)
    send_command("SetPWMServoAngle", [5, 100])
    time.sleep(.5)
    send_command("SetPWMServoAngle", [3, 0])
    time.sleep(.5)
    send_command("SetPWMServoAngle", [4, 179])
    time.sleep(1)

def open_claws():
    send_command("SetPWMServo", [500, 1, 1, pulse_to_angle(1800)])  # Increased range
    time.sleep(1)

def close_claws():
    send_command("SetPWMServo", [500, 1, 1, pulse_to_angle(1200)]) 
    time.sleep(1)

turn_right_bend_down()
open_claws()
close_claws()
home_position()
open_claws()
close_claws()

# OPEN CLAWS
# send_command("SetPWMServo", [500, 1, 1, pulse_to_angle(1800)])  # Increased range
# time.sleep(1)
# # CLOSE CLAWS
# send_command("SetPWMServo", [500, 1, 1, pulse_to_angle(1200)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 1, pulse_to_angle(1800)])  # Increased range
# time.sleep(0.5)
# send_command("SetPWMServo", [500, 1, 1, pulse_to_angle(1500)])  # Return to center
# time.sleep(1.5)

# # Control motors
# # Parameters: [motor_id, speed, motor_id, speed, ...]
# result = send_command("SetBrushMotor", [1, 50])

# # Get battery level
# result = send_command("GetBatteryVoltage")

# # Run color tracking with specific color
# result = send_command("ColorTracking", "red")

# # Load a specific function (1-9)
# result = send_command("LoadFunc", 1)
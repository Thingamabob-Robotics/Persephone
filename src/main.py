# Import Statements
# First party
from vex import *

# Second party

# Third party

# File Docstring
# Persephone || main.py
# ---------------------------------------
# Simple and generic auton + driver control
#
# Authors: @MaxineToTheStars <https://github.com/MaxineToTheStars>
#
# @implNote The following code is multithreaded so that *may* cause
# issues like edge cases
# ----------------------------------------------------------------

# Stop Vex from shitting itself
brain: Brain = Brain()
controller: Controller = Controller(PRIMARY)

# Robot Config
intakeInSelection: Controller.Button = controller.buttonL1  # Top left
intakeOutSelection: Controller.Button = controller.buttonL2  # Top left bottom

moveArmUpSelection: Controller.Button = controller.buttonR1  # Top Right
moveArmDownSelection: Controller.Button = controller.buttonR2  # Top right down

wingToggleInSelection: Controller.Button = controller.buttonA  # A button
wingToggleOutSelection: Controller.Button = controller.buttonB  # B Button

leftAxisSelection: Controller.Axis = controller.axis3  # Top-Bottom left
rightAxisSelection: Controller.Axis = controller.axis2  # Top-Bottom right

# Wings
WINGS_TRIPORT_PORT: DigitalOut = DigitalOut(brain.three_wire_port.a)

# Intake
INTAKE_MOTOR_PORT: int = Ports.PORT12

# Arms
LEFT_ARM_MOTOR_PORT: int = Ports.PORT9
RIGHT_ARM_MOTOR_PORT: int = Ports.PORT2

# Drivetrain
LEFT_FRONT_MOTOR_PORT: int = Ports.PORT20
LEFT_BACK_MOTOR_PORT: int = Ports.PORT10
RIGHT_FRONT_MOTOR_PORT: int = Ports.PORT11
RIGHT_BACK_MOTOR_PORT: int = Ports.PORT1

# Enums

# Interfaces

# Constants

# Motor definitions
INTAKE_MOTOR: Motor = Motor(INTAKE_MOTOR_PORT, GearSetting.RATIO_18_1, False)
LEFT_FRONT_MOTOR: Motor = Motor(LEFT_FRONT_MOTOR_PORT, GearSetting.RATIO_18_1, False)
LEFT_BACK_MOTOR: Motor = Motor(LEFT_BACK_MOTOR_PORT, GearSetting.RATIO_18_1, True)
RIGHT_FRONT_MOTOR: Motor = Motor(RIGHT_FRONT_MOTOR_PORT, GearSetting.RATIO_18_1, False)
RIGHT_BACK_MOTOR: Motor = Motor(RIGHT_BACK_MOTOR_PORT, GearSetting.RATIO_18_1, True)
LEFT_ARM_MOTOR: Motor = Motor(LEFT_ARM_MOTOR_PORT, GearSetting.RATIO_18_1, False)
RIGHT_ARM_MOTOR: Motor = Motor(RIGHT_ARM_MOTOR_PORT, GearSetting.RATIO_18_1, False)

LEFT_DOM_MOTOR_GROUP: MotorGroup = MotorGroup(
    LEFT_FRONT_MOTOR, RIGHT_BACK_MOTOR
)  # 20, 1
RIGHT_DOM_MOTOR_GROUP: MotorGroup = MotorGroup(
    RIGHT_FRONT_MOTOR, LEFT_BACK_MOTOR
)  # 11, 10

ARM_MOTOR_GROUP: MotorGroup = MotorGroup(LEFT_ARM_MOTOR, RIGHT_ARM_MOTOR)

# Public Variables

# Private Variables

# main()
def main() -> None:
    # Create a new Competition instance
    Competition(driver_control, auton_control)

# Public Methods
def driver_control() -> None:
    # Control loop

    # Movement (threaded)
    Thread(_driver_control_movement_thread)

    # Arm Control (threaded)
    Thread(_driver_control_arm_control_thread)

    # Intake Control (threaded)
    Thread(_driver_control_intake_control_thread)

    # Wing Control (threaded)
    Thread(_driver_control_wing_control_thread)

def auton_control() -> None:
    pass

# Private Methods
def _driver_control_movement_thread() -> None:
    while 1:
        # Read joystick values
        leftAxisValue: int = leftAxisSelection.position()
        rightAxisValue: int = rightAxisSelection.position()

        # Set the MotorGroup velocity
        LEFT_DOM_MOTOR_GROUP.set_velocity(leftAxisValue)
        RIGHT_DOM_MOTOR_GROUP.set_velocity(rightAxisValue)

        # Move
        LEFT_DOM_MOTOR_GROUP.spin(FORWARD)
        RIGHT_DOM_MOTOR_GROUP.spin(FORWARD)

        # Stop the Thread from killing itself
        wait(10, MSEC)

def _driver_control_arm_control_thread() -> None:
    while 1:
        # Wait for button toggles
        if moveArmUpSelection.pressing():
            ARM_MOTOR_GROUP.set_velocity(85, PERCENT)
            ARM_MOTOR_GROUP.spin(FORWARD)
        elif moveArmDownSelection.pressing():
            ARM_MOTOR_GROUP.set_velocity(-85, PERCENT)
            ARM_MOTOR_GROUP.spin(FORWARD)
        else:
            ARM_MOTOR_GROUP.stop(HOLD)

        # Stop the Thread from killing itself
        wait(10, MSEC)

def _driver_control_intake_control_thread() -> None:
    while 1:
        # Wait for button toggles
        if intakeInSelection.pressing():
            INTAKE_MOTOR.set_velocity(100, PERCENT)
            INTAKE_MOTOR.spin(FORWARD)
        elif intakeOutSelection.pressing():
            INTAKE_MOTOR.set_velocity(-100, PERCENT)
            INTAKE_MOTOR.spin(FORWARD)
        else:
            INTAKE_MOTOR.stop(HOLD)

        # Stop the Thread from killing itself
        wait(10, MSEC)

def _driver_control_wing_control_thread() -> None:
    while 1:
        # Wait for button toggles
        if wingToggleInSelection.pressing():
            WINGS_TRIPORT_PORT.set(0)  # Set low to retract
        elif wingToggleOutSelection.pressing():
            WINGS_TRIPORT_PORT.set(1)  # Set high to expand

        wait(10, MSEC)

# Run
if __name__ == "__main__":
    main()

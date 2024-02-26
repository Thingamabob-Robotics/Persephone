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

moveArmUpSelection: Controller.Button = controller.buttonDown  # Top Right
moveArmDownSelection: Controller.Button = controller.buttonUp  # Top right down

# wingToggleInSelection: Controller.Button = controller.buttonA  # A button
wingToggleSelection: Controller.Button = controller.buttonA  # B Button

leftAxisSelection: Controller.Axis = controller.axis3  # Top-Bottom left
rightAxisSelection: Controller.Axis = controller.axis2  # Top-Bottom right

# Wings
WINGS_TRIPORT_PORT: DigitalOut = DigitalOut(brain.three_wire_port.b)
WINGS_TRIPORT_PORT1: DigitalOut = DigitalOut(brain.three_wire_port.h)


# Intake
INTAKE_MOTOR_PORT: int = Ports.PORT12

# Arms
LEFT_ARM_MOTOR_PORT: int = Ports.PORT13
RIGHT_ARM_MOTOR_PORT: int = Ports.PORT19

# Drivetrain
LEFT_FRONT_MOTOR_PORT: int = Ports.PORT1
LEFT_BACK_MOTOR_PORT: int = Ports.PORT11
RIGHT_FRONT_MOTOR_PORT: int = Ports.PORT10
RIGHT_BACK_MOTOR_PORT: int = Ports.PORT20

# Enums

# Interfaces

# Constants
IS_SKILL: bool = False

# Motor definitions
INTAKE_MOTOR: Motor = Motor(INTAKE_MOTOR_PORT, GearSetting.RATIO_18_1, False)
LEFT_FRONT_MOTOR: Motor = Motor(LEFT_FRONT_MOTOR_PORT, GearSetting.RATIO_18_1, True)
LEFT_BACK_MOTOR: Motor = Motor(LEFT_BACK_MOTOR_PORT, GearSetting.RATIO_18_1, True)
RIGHT_FRONT_MOTOR: Motor = Motor(RIGHT_FRONT_MOTOR_PORT, GearSetting.RATIO_18_1, False)
RIGHT_BACK_MOTOR: Motor = Motor(RIGHT_BACK_MOTOR_PORT, GearSetting.RATIO_18_1, False)
LEFT_ARM_MOTOR: Motor = Motor(LEFT_ARM_MOTOR_PORT, GearSetting.RATIO_18_1, False)
RIGHT_ARM_MOTOR: Motor = Motor(RIGHT_ARM_MOTOR_PORT, GearSetting.RATIO_18_1, True)

LEFT_DOM_MOTOR_GROUP: MotorGroup = MotorGroup(
    LEFT_FRONT_MOTOR, LEFT_BACK_MOTOR
)  # 20, 1
RIGHT_DOM_MOTOR_GROUP: MotorGroup = MotorGroup(
    RIGHT_FRONT_MOTOR, RIGHT_BACK_MOTOR
)  # 11, 10

ARM_MOTOR_GROUP: MotorGroup = MotorGroup(LEFT_ARM_MOTOR, RIGHT_ARM_MOTOR)

# Public Variables

# Private Variables


# main()
def main() -> None:
    # Create a new Competition instance
    # auton_control()
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
    # Thread(_driver_control_wing_control_thread)


def auton_control() -> None:
    if IS_SKILL:
        # Set drive velocity
        INTAKE_MOTOR.set_velocity(100, PERCENT)
        ARM_MOTOR_GROUP.set_velocity(-100, PERCENT)
        LEFT_DOM_MOTOR_GROUP.set_velocity(-100, PERCENT)
        RIGHT_DOM_MOTOR_GROUP.set_velocity(-100, PERCENT)

        # Move out and stop
        LEFT_DOM_MOTOR_GROUP.spin(FORWARD)
        RIGHT_DOM_MOTOR_GROUP.spin(FORWARD)
        wait(0.7, SECONDS)
        LEFT_DOM_MOTOR_GROUP.stop(BRAKE)
        RIGHT_DOM_MOTOR_GROUP.stop(BRAKE)

        # Align with bar
        LEFT_DOM_MOTOR_GROUP.spin(REVERSE)
        wait(0.57, SECONDS)
        LEFT_DOM_MOTOR_GROUP.stop(BRAKE)

        # Move into position and arm
        LEFT_DOM_MOTOR_GROUP.spin(REVERSE)
        RIGHT_DOM_MOTOR_GROUP.spin(REVERSE)
        wait(0.5, SECONDS)
        LEFT_DOM_MOTOR_GROUP.stop(BRAKE)
        RIGHT_DOM_MOTOR_GROUP.stop(BRAKE)
        ARM_MOTOR_GROUP.spin(FORWARD)
        wait(0.8, SECONDS)
        ARM_MOTOR_GROUP.stop(HOLD)

        # # Adjust
        # RIGHT_DOM_MOTOR_GROUP.spin(FORWARD)
        # wait(0.2, SECONDS)
        # RIGHT_DOM_MOTOR_GROUP.stop(BRAKE)

        # # Re Adjust
        # LEFT_DOM_MOTOR_GROUP.spin(REVERSE)
        # RIGHT_DOM_MOTOR_GROUP.spin(REVERSE)
        # wait(0.3, SECONDS)
        # LEFT_DOM_MOTOR_GROUP.stop(BRAKE)
        # RIGHT_DOM_MOTOR_GROUP.stop(BRAKE)

        # Spin ARM for 30 seconds
        INTAKE_MOTOR.spin(FORWARD)
        wait(0, SECONDS)
        INTAKE_MOTOR.stop(COAST)

        # Arm DOWN
        ARM_MOTOR_GROUP.spin(REVERSE)
        wait(0.8, SECONDS)
        ARM_MOTOR_GROUP.stop(COAST)

        # Move out
        LEFT_DOM_MOTOR_GROUP.spin(FORWARD)
        RIGHT_DOM_MOTOR_GROUP.spin(FORWARD)
        wait(1.35, SECONDS)
        LEFT_DOM_MOTOR_GROUP.stop(BRAKE)
        RIGHT_DOM_MOTOR_GROUP.stop(BRAKE)

        # Adjust
        LEFT_DOM_MOTOR_GROUP.spin(FORWARD)
        wait(0.5, SECONDS)
        LEFT_DOM_MOTOR_GROUP.stop(BRAKE)

        # Move out
        LEFT_DOM_MOTOR_GROUP.spin(FORWARD)
        RIGHT_DOM_MOTOR_GROUP.spin(FORWARD)
        wait(1.35, SECONDS)
        LEFT_DOM_MOTOR_GROUP.stop(BRAKE)
        RIGHT_DOM_MOTOR_GROUP.stop(BRAKE)

        # Turn right
        RIGHT_DOM_MOTOR_GROUP.spin(FORWARD)
        wait(0.5, SECONDS)
        RIGHT_DOM_MOTOR_GROUP.stop(BRAKE)

        # Move out
        LEFT_DOM_MOTOR_GROUP.spin(FORWARD)
        RIGHT_DOM_MOTOR_GROUP.spin(FORWARD)
        wait(0.75, SECONDS)
        LEFT_DOM_MOTOR_GROUP.stop(BRAKE)
        RIGHT_DOM_MOTOR_GROUP.stop(BRAKE)

        # Push from right

        # Push from center

        # Push from left

    elif IS_SKILL == False:
        # Normal Auton
        LEFT_DOM_MOTOR_GROUP.set_velocity(100, PERCENT)
        RIGHT_DOM_MOTOR_GROUP.set_velocity(100, PERCENT)

        # Move forward
        LEFT_DOM_MOTOR_GROUP.spin(FORWARD)
        RIGHT_DOM_MOTOR_GROUP.spin(FORWARD)

        # Delay
        wait(4, SECONDS)

        # Stop all
        LEFT_DOM_MOTOR_GROUP.stop(COAST)
        RIGHT_DOM_MOTOR_GROUP.stop(COAST)

        # Move backwards
        LEFT_DOM_MOTOR_GROUP.set_velocity(-100, PERCENT)
        RIGHT_DOM_MOTOR_GROUP.set_velocity(-100, PERCENT)
        LEFT_DOM_MOTOR_GROUP.spin(FORWARD)
        RIGHT_DOM_MOTOR_GROUP.spin(FORWARD)

        # Delay
        wait(3, SECONDS)

        # Stop all
        LEFT_DOM_MOTOR_GROUP.stop(BRAKE)
        RIGHT_DOM_MOTOR_GROUP.stop(BRAKE)

        # Arm UP
        ARM_MOTOR_GROUP.set_velocity(-100, PERCENT)
        ARM_MOTOR_GROUP.spin(FORWARD)
        wait(0.8, SECONDS)
        ARM_MOTOR_GROUP.stop(HOLD)


# Private Methods
def _driver_control_movement_thread() -> None:
    while True:
        # Read joystick values
        leftAxisValue: int = leftAxisSelection.position()
        rightAxisValue: int = rightAxisSelection.position()

        # Set the MotorGroup velocity
        LEFT_DOM_MOTOR_GROUP.set_velocity(leftAxisValue, PERCENT)
        RIGHT_DOM_MOTOR_GROUP.set_velocity(rightAxisValue, PERCENT)

        # Move
        LEFT_DOM_MOTOR_GROUP.spin(FORWARD)
        RIGHT_DOM_MOTOR_GROUP.spin(FORWARD)

        # Stop the Thread from killing itself
        wait(10, MSEC)


def _driver_control_arm_control_thread() -> None:
    while 1:
        # Wait for button toggles
        if moveArmUpSelection.pressing():
            ARM_MOTOR_GROUP.set_velocity(60, PERCENT)
            ARM_MOTOR_GROUP.spin(FORWARD)
        elif moveArmDownSelection.pressing():
            ARM_MOTOR_GROUP.set_velocity(-60, PERCENT)
            ARM_MOTOR_GROUP.spin(FORWARD)
        else:
            ARM_MOTOR_GROUP.stop(BRAKE)

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
            INTAKE_MOTOR.stop(COAST)

        # Stop the Thread from killing itself
        wait(10, MSEC)


def _driver_control_wing_control_thread() -> None:
    while 1:
        # Wait for button toggles
        if wingToggleSelection.pressing():
            if WINGS_TRIPORT_PORT1.value() == 1:
                WINGS_TRIPORT_PORT.set(0)
                WINGS_TRIPORT_PORT1.set(0)
                wait(0.3, SECONDS)
            elif WINGS_TRIPORT_PORT1.value() == 0:
                WINGS_TRIPORT_PORT.set(1)
                WINGS_TRIPORT_PORT1.set(1)
                wait(0.3, SECONDS)

        wait(10, MSEC)


# Run
if __name__ == "__main__":
    main()

"""
Water Flow Program
This program calculates water pressure in a city water distribution system.

ENHANCEMENTS (Exceeding Requirements):
1. Added kpa_to_psi() function to convert pressure from kilopascals to pounds per square inch.
2. Added constants for Earth's acceleration of gravity, water density, and water dynamic viscosity
   at the top of the file instead of hardcoding values in functions.
4. Added test_kpa_to_psi() function in test file to verify the conversion function.
"""

# OUR Constants
EARTH_ACCELERATION_OF_GRAVITY = 9.8066500  # which is in m/s^2
WATER_DENSITY = 998.2000000  # which is in kg/m^3
WATER_DYNAMIC_VISCOSITY = 0.0010016  # which is in Pascal seconds


def water_column_height(tower_height, tank_height):
    """Calculate the height of a column of water from a tower height and a tank wall height.
    
    Parameters:
        tower_height: the height of the tower (float)
        tank_height: the height of the walls of the tank that is on top of the tower (float)
    Return: the height of the water column (float)
    """
    

    h = tower_height + (3 * tank_height / 4)
    return h


def pressure_gain_from_water_height(height):
    """Calculate the pressure caused by Earth's gravity pulling on the water stored in an elevated tank.
    
    Parameters:
        height: the height of the water column (float)
    Return: the pressure in kilopascals (float)
    """


    P = (WATER_DENSITY * EARTH_ACCELERATION_OF_GRAVITY * height) / 1000
    return P


def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    """Calculate the water pressure lost because of the friction between the water and the walls of a pipe.
    
    Parameters:
        pipe_diameter: the diameter of the pipe (float)
        pipe_length: the length of the pipe (float)
        friction_factor: the pipe's friction factor (float)
        fluid_velocity: the velocity of the water flowing through the pipe (float)
    Return: the lost pressure in kilopascals (float)
    """


    P = (-friction_factor * pipe_length * WATER_DENSITY * fluid_velocity**2) / (2000 * pipe_diameter)
    return P


def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """Calculate the water pressure lost because of fittings such as 90° elbows and 45° elbows.
    
    Parameters:
        fluid_velocity: the velocity of the water flowing through the pipe (float)
        quantity_fittings: the number of fittings (integer)
    Return: the lost pressure in kilopascals (float)
    """


    P = (-0.04 * WATER_DENSITY * fluid_velocity**2 * quantity_fittings) / 2000
    return P


def reynolds_number(hydraulic_diameter, fluid_velocity):
    """Calculate the Reynolds number for a pipe with water flowing through it.
    
    Parameters:
        hydraulic_diameter: the diameter of the pipe (float)
        fluid_velocity: the velocity of the water flowing through the pipe (float)
    Return: the Reynolds number (float)
    """


    R = (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / WATER_DYNAMIC_VISCOSITY
    return R


def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    """Calculate the water pressure lost because of water moving from a pipe with a larger diameter into a pipe with a smaller diameter.
    
    Parameters:
        larger_diameter: the diameter of the larger pipe (float)
        fluid_velocity: the velocity of the water flowing through the larger pipe (float)
        reynolds_number: the Reynolds number for the larger pipe (float)
        smaller_diameter: the diameter of the smaller pipe (float)
    Return: the lost pressure in kilopascals (float)
    """


    k = (0.1 + (50 / reynolds_number)) * ((larger_diameter / smaller_diameter)**4 - 1)
    P = (-k * WATER_DENSITY * fluid_velocity**2) / 2000
    return P


def kpa_to_psi(kpa):
    """Convert pressure from kilopascals to pounds per square inch.
    
    Parameters:
        kpa: pressure in kilopascals (float)
    Return: pressure in pounds per square inch (float)
    """


    psi = kpa * 0.14503773773020923
    return psi


def main():
    """Get input from the user and calculate the water pressure at a house."""
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))
    
    water_height = water_column_height(tower_height, tank_height)
    pressure = pressure_gain_from_water_height(water_height)
    
    diameter = 0.28687  
    friction = 0.013
    velocity = 1.65  
    
    reynolds = reynolds_number(diameter, velocity)
    loss = pressure_loss_from_pipe(diameter, length1, friction, velocity)
    pressure += loss
    
    loss = pressure_loss_from_fittings(velocity, quantity_angles)
    pressure += loss
    
    loss = pressure_loss_from_pipe_reduction(diameter, velocity, reynolds, 0.048692)
    pressure += loss
    
    diameter = 0.048692  
    friction = 0.018
    velocity = 1.75  
    loss = pressure_loss_from_pipe(diameter, length2, friction, velocity)
    pressure += loss
    
    print(f"Pressure at house: {pressure:.1f} kilopascals")
    
    # Convert and display pressure in psi for US users
    pressure_psi = kpa_to_psi(pressure)
    print(f"Pressure at house: {pressure_psi:.1f} psi")


if __name__ == "__main__":
    main()
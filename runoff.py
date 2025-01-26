from HBV.Snow import Snow
from HBV.User_config import *
from HBV.log_config import *


class SoilMoisture(Snow):
    """
      This class models the soil moisture and runoff process. It extends the Snow model
      and adds functionality for calculating evapotranspiration (ET) and soil moisture
      based on input data and parameters.
      """

    def __init__(self, csv_file_name=CSV_FILE_NAME, beta=BETA, TT=TT, Cmelt=Cmelt, SWE=SWE_INITIAL, mm_to_m=mm_to_m,
                 day_to_s=day_to_s, Area=CATCHMENT_AREA, initial_soil_moisture=INITIAL_SOIL_MOISTURE, FC=FIELD_CAPACITY,
                 pwp=PWP):
        """
        Initializes the SoilMoisture model with given parameters.

        :param csv_file_name: Path to the CSV data file
        :param beta: Beta parameter for soil moisture calculation
        :param TT: Threshold temperature for snowmelt
        :param Cmelt: Snowmelt coefficient
        :param SWE: Snow Water Equivalent
        :param mm_to_m: Conversion factor from mm to meters
        :param day_to_s: Conversion factor from days to seconds
        :param Area: Catchment area
        :param initial_soil_moisture: Initial value of soil moisture
        :param FC: Field capacity of soil
        :param pwp: Permanent wilting point of soil
        """
        # Call the parent class (Snow) constructor to initialize the snow model with the given file and parameters
        super().__init__(csv_file_name, TT, Cmelt, SWE)

        # Initialize the specific parameters for the SoilMoisture model
        self.beta = beta  # Beta parameter for soil moisture calculation
        self.k = K  # A constant related to the soil moisture model (presumably defined elsewhere)
        self.timeStep = TIME_STEP  # Time step for calculations (presumably defined elsewhere)
        self.initial_soil_moisture = INITIAL_SOIL_MOISTURE  # Initial soil moisture level
        self.FC = FC  # Field capacity of the soil
        self.pwp = PWP  # Permanent wilting point of soil
        self.Area = CATCHMENT_AREA  # Catchment area for runoff calculations
        self.mm_to_m = mm_to_m  # Conversion factor from millimeters to meters
        self.day_to_s = day_to_s  # Conversion factor from days to seconds
        self.processed_data = None  # Placeholder for processed data (initialized to None)

        # Log the successful initialization of the SoilMoisture model
        action_logger.info(
            f"SoilMoisture model initialized with beta={self.beta}, k={self.k}, timeStep={self.timeStep}")

    def calculate_ET_and_soil_moisture(self):
        """
        Calculates evapotranspiration (ET) and soil moisture for each time step.

        It computes the soil moisture, runoff, and ET values and updates the DataFrame
        with the calculated values.

        :return: Updated DataFrame with 'Simulated_Runoff', 'Soil_moisture', and 'ET' columns
        :raises KeyError: If required columns ('liquid_water' or 'peti') are missing
        """
        # Check if required columns 'liquid_water' or 'peti' exist in the DataFrame
        if 'liquid_water' not in self.data_hbv.columns or 'peti' not in self.data_hbv.columns:
            error_logger.error("Required columns 'liquid_water' or 'peti' are missing from the DataFrame.")
            raise KeyError("Required columns 'liquid_water' or 'peti' are missing from the DataFrame.")

        # Initialize empty lists to store the calculated values
        soil_moisture = []
        runoff = []
        et_values = []

        # Loop through the DataFrame to calculate ET, soil moisture, and runoff for each time step
        for index, row in self.data_hbv.iterrows():
            liquid_water = row['liquid_water']  # Get the liquid water for the current time step
            peti = row['peti']  # Get the PET (Potential Evapotranspiration) for the current time step

            if index == 0:  # For the first row, initialize with the initial conditions
                s_new = self.initial_soil_moisture  # Set initial soil moisture
                q_new = self.k * s_new  # Calculate the runoff for the first time step
                et = (s_new / self.FC) * peti if s_new < self.pwp else peti  # Calculate ET for the first time step
            else:  # For subsequent rows, calculate based on previous values
                inflow = liquid_water  # Incoming water from precipitation
                outflow = runoff[-1] + et_values[-1]  # Sum of previous runoff and ET values
                sm_t = max(0, soil_moisture[-1] + inflow - outflow)  # Calculate the new soil moisture
                qb_t = liquid_water * ((sm_t / self.FC) ** self.beta)  # Calculate runoff based on soil moisture
                s_new = max(0.0, soil_moisture[-1] + inflow - qb_t - et_values[-1])  # Update soil moisture
                q_new = qb_t  # Update runoff value
                et = (s_new / self.FC) * peti if s_new < self.pwp else peti  # Calculate ET for this time step

            # Append the calculated values to their respective lists
            soil_moisture.append(s_new)
            runoff.append(q_new)
            et_values.append(et)

        # Update the DataFrame with the new calculated values
        self.data_hbv["Simulated_Runoff"] = runoff  # Store the simulated runoff
        self.data_hbv["Soil_moisture"] = soil_moisture  # Store the calculated soil moisture
        self.data_hbv["ET"] = et_values  # Store the evapotranspiration values

        # Log that the calculation has been completed successfully
        action_logger.info("ET and soil moisture calculations completed successfully.")

        # Return the updated DataFrame
        return self.data_hbv

    def __str__(self):
        """
        Returns a string summarizing the parameters of the SoilMoisture model.

        :return: String with the values of beta, k, and timeStep
        """
        # Format the string with the current values of the model parameters
        return f"SoilMoisture model with beta={self.beta}, k={self.k}, timeStep={self.timeStep}"
        # Return a summary string containing beta, k, and timeStep value

    def volume_discharge(self):
        """
        Calculates the discharge volume based on the simulated runoff values.

        This method iterates over each row of the data to calculate the discharge volume
        using the formula for converting runoff (in mm/day) to discharge volume (in m³/s).
        The calculated discharge volumes are added to a new column in the DataFrame.

        Optionally, the updated DataFrame can be saved to an Excel file.

        :return: Updated DataFrame with 'Discharge_Vol_simulated' column containing the calculated discharge volumes
        """

        discharge_volume_simulated = []  # List to store calculated discharge volumes

        # Access the 'Simulated_Runoff' from the DataFrame and calculate discharge volume for each row
        for index, row in self.data_hbv.iterrows():
            simulated_runoff = row['Simulated_Runoff']  # Accessing simulated runoff for the current row

            # Ensure 'Simulated_Runoff' is in mm/day, converting it to m³/s using the given formula
            discharge_volume = simulated_runoff * self.mm_to_m * self.Area * self.day_to_s

            discharge_volume_simulated.append(discharge_volume)  # Append the calculated volume to the list

        # Add the calculated discharge volumes to the DataFrame as a new column
        self.data_hbv["Discharge_Vol_simulated"] = discharge_volume_simulated

        # Log the range of the calculated discharge volumes
        action_logger.info(f"Range of discharge volume calculated: {np.ptp(discharge_volume_simulated)}")

        # Optionally save the updated DataFrame to an Excel file
        output_file = "runoff_with_discharge_output4.xlsx"  # Output file name
        self.data_hbv.to_excel(output_file, index=False)  # Save the DataFrame to Excel
        print(f"DataFrame with discharge volume has been saved to {output_file}")  # Print message confirming save

        # Return the updated DataFrame with discharge volume data
        return self.data_hbv






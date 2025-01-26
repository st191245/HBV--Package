from HBV.runoff import SoilMoisture
from HBV.User_config import *
from HBV.visualization import *
from HBV.log_config import *


def main():
    """
        Main function to execute the runoff modeling process. This function orchestrates
        the steps of loading data, performing snowmelt calculations, calculating evapotranspiration
        (ET) and soil moisture, and calculating discharge volume. It also generates plots if enabled
        and logs all actions and exceptions.

        :return: None
        :raises Exception: If an error occurs during the process, it is logged and re-raised
        """
    try:
        action_logger.info("Starting the main process for runoff modeling.")

        # Initialize SoilMoisture object
        runoff = SoilMoisture(CSV_FILE_NAME)
        action_logger.info("SoilMoisture object initialized.")

        # Load and process data
        runoff.get_hbv_data(CSV_FILE_NAME)  # Detailed logging in the method
        runoff.calculate_snow_melt()       # Detailed logging in the method
        runoff.calculate_ET_and_soil_moisture()  # Detailed logging in the method
        runoff.volume_discharge()          # Detailed logging in the method

        # Processed data
        processed_data = runoff.data_hbv

        # Generate plots if enabled
        if ENABLE_PLOTTING:
            action_logger.info("Plotting is enabled. Generating plots.")
            create_plots(processed_data)

        action_logger.info("Runoff modeling process completed successfully.")

    except Exception as e:
        error_logger.error(f"An unexpected error occurred in the main process: {str(e)}")
        raise  # Re-raise the exception after logging


if __name__ == "__main__":
    main()

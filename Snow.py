from HBV.User_config import *
from HBV.log_config import *

class DataReader:
    """
     Loads HBV model data from a CSV file into a pandas DataFrame.

     :param csv_file_name: str, path to the CSV file (default is CSV_FILE_NAME)
     :param delimiter: str, delimiter used in the CSV file (default is ",")
     :return: None
     """
    def __init__(self, csv_file_name=CSV_FILE_NAME, delimiter=","):
        self.sep = delimiter
        self.data_hbv = pd.DataFrame()
        self.get_hbv_data(csv_file_name)

    def get_hbv_data(self, csv_file_name):
        """
               Loads the HBV model data from the specified CSV file.

               :param csv_file_name: str, path to the CSV file
               :return: None
               """
        try:
            self.data_hbv = pd.read_csv(csv_file_name, header=0, sep=self.sep)
            action_logger.info(f"Data loaded successfully from {csv_file_name}")
        except FileNotFoundError:
            error_logger.error(f"File not found: {csv_file_name}. Ensure the file exists at the specified path.")
            raise
        except Exception as e:
            error_logger.error(f"An unexpected error occurred while loading data: {str(e)}")
            raise

class Snow(DataReader):
    """
       Models snowmelt in the HBV model, inheriting from DataReader.

       :param csv_file_name: str, path to the CSV file (default is CSV_FILE_NAME)
       :param TT: float, temperature threshold for snowmelt (default is TT)
       :param Cmelt: float, snowmelt coefficient (default is Cmelt)
       :param SWE: float, snow water equivalent (default is SWE_INITIAL)
       :return: None
       """
    def __init__(self, csv_file_name=CSV_FILE_NAME, TT=TT, Cmelt=Cmelt, SWE=SWE_INITIAL):
        super().__init__(csv_file_name)
        self.TT = TT
        self.Cmelt = Cmelt
        self.SWE = SWE
        action_logger.info(f"Snow model initialized with TT={self.TT}, Cmelt={self.Cmelt}, SWE={self.SWE}")

    def calculate_snow_melt(self, ):
        """
                Calculates the snowmelt based on temperature and precipitation values.

                :return: pandas.DataFrame, updated DataFrame with 'liquid_water' column
                """
        if 'temperature' not in self.data_hbv.columns or 'precipitation' not in self.data_hbv.columns:
            warning_logger.warning(
                "Missing columns: 'temperature' or 'precipitation'. Ensure the data contains these colums")
            raise KeyError("Required columns 'temperature' or 'precipitation' are missing from the DataFrame.")

        liquid_water_values = []
        for _, row in self.data_hbv.iterrows():
            temperature = row["temperature"]
            precipitation = row["precipitation"]
            if temperature < self.TT:
                self.SWE += precipitation
                liquid_water = 0.0
            else:
                melt = self.Cmelt * (temperature - self.TT)
                liquid_water = precipitation + np.min([self.SWE, melt])  # np.min expects a list or array,this list compares two values and return the min value
                self.SWE = np.max([0.0, self.SWE - melt])  # np.max expects a list or array
            liquid_water_values.append(liquid_water)


        self.data_hbv["liquid_water"] = liquid_water_values
        action_logger.info("Snow melt calculations completed successfully.")

        return self.data_hbv



    def __str__(self):
        """
                Returns a string summary of the Snow model parameters.

                :return: str, string summary of TT, Cmelt, and SWE
                """
        return f"Snow model with TT={self.TT}, Cmelt={self.Cmelt}, SWE={self.SWE}"










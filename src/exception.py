import sys

def error_message_details(error):
    """Extracts detailed error information including filename and line number."""
    exc_type, exc_value, exc_tb = sys.exc_info()
    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        error_message = (
            f"Error occurred in Python script: [{file_name}], "
            f"line number: [{exc_tb.tb_lineno}], "
            f"error message: [{str(error)}]"
        )
    else:
        error_message = str(error)
    return error_message

class CustomException(Exception):
    def __init__(self, error):
        """Initializes the exception with a detailed error message."""
        super().__init__(str(error))  # Call Exception constructor
        self.error_message = error_message_details(error)  # Store detailed error

    def __str__(self):
        """Returns the detailed error message."""
        return self.error_message

# Example Usage
try:
    a = 1 / 0  # This will raise ZeroDivisionError
except Exception as e:
    raise CustomException(e)

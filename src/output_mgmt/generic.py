import datetime
import os


def prepare_number(number: int) -> str:
    """
    Transforms an int number to str. If the number is lower than 10, it adds one 0 at the left of it.

    Args:
        number (int): the number to be transformed

    Returns:
        str: the string of the provided number
    """
    if number < 10:
        return "0" + str(number)
    else:
        return str(number)


def get_filename(date: datetime.datetime = datetime.datetime.now()) -> str:
    """
    Generates a filename with the format %YYYY%MM%DD_%HH%MM_video.mp4. In case the filename exists it
    adds (n) at the end, where n is the n occurrence of files with the same filename.

    Args:
        date (datetime, optional): a date in datetime format to be used to create the filename.
        Defaults to datetime.now().

    Returns:
        str: a string with the filename
    """
    # Get current time
    current_time = date
    # Set variables with current time
    year = prepare_number(current_time.year)
    month = prepare_number(current_time.month)
    day = prepare_number(current_time.day)
    hour = prepare_number(current_time.hour)
    minute = prepare_number(current_time.minute)
    # Set the variable filename with the
    filename = year + month + day + "_" + hour + minute + "_video.mp4"
    # Checks if the filename exists. If it does, changes filename by adding (n), where n is the
    # number of files with the same name
    if os.path.isfile(filename):
        file_exists = True
        counter = 1
        while file_exists:
            new_filename = filename[:-4] + f" ({counter})"
            if not os.path.isfile(new_filename + ".mp4"):
                filename = new_filename + ".mp4"
                file_exists = False
    return filename

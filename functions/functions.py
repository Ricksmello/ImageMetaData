import exifread
import datetime
import os
import socket


folder = os.getcwd()
datetime_log: str = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")

# Get the hostname.
hostname = socket.gethostname()
# Get the datetime.
date_log = str(datetime.datetime.now().strftime("%d.%m.%Y"))
# Set the file name.
path = os.path.join(folder, hostname + " - " + date_log + ".log")


def newFileName(**kwargs):
    """
    Generate the new file name.

    :argument:
       filename (str): The actual file name.

    :returns:
        new_file_name (str): The new file name.
    """

    # Arguments.
    filename = kwargs.get("filename")

    full_path = os.path.join(folder, filename)

    with open(full_path, 'rb') as image:  # file path and name
        exif = exifread.process_file(image)

    # Take the Data Taken, otherwise take the timestamp.
    if exif:
        new_file_name = str(exif['EXIF DateTimeOriginal'])
        file_width = str(exif['EXIF ExifImageWidth'])
        file_lenght = str(exif['EXIF ExifImageLength'])
        new_file_name = new_file_name + '_w_' + file_width + '_l_' + file_lenght
        new_file_name = new_file_name.replace(".", "")

    else:

        new_file_name = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
        new_file_name = new_file_name.strftime("%Y/%m/%d, %H:%M:%S.%f")

    if ":" in new_file_name:
        new_file_name = new_file_name.replace(":", ".")
        new_file_name = new_file_name.replace("/", ".")
        new_file_name = new_file_name.replace(",", "")

    return new_file_name


@staticmethod
def renameFile(**kwargs):
    """
    Reanem the file.

    :argument:
       old_name (str): The actual file name.
       new_name (str): The new file name.

    :returns:
        No return.
    """

    # Arguments.
    old_name = kwargs.get("old_name")
    new_name = kwargs.get("new_name")

    # Rename file.
    try:
        os.rename(old_name, new_name)
        print(f"The file {old_name} was renamed to {new_name}.")
        addLogs(message="General", value=f"The file {old_name} was renamed to {new_name}.")
    except FileNotFoundError:
        print(f"The file {old_name} was not found.")
        addLogs(message="General", value=f"The file {old_name} was not found.")
    except FileExistsError:
        print(f"There is already a file with the name  {new_name}.")
        addLogs(message="General", value=f"There is already a file with the name  {new_name}.")
    except Exception as e:
        print(f"Something wrong happened: {e}")
        addLogs(message="General", value=f"Something wrong happened: {e}")


def addLogs(**kwargs):

    try:
        # kwargs variables.
        message = kwargs.get("message")
        value = kwargs.get("value")
        value1 = kwargs.get("value1")
        value2 = kwargs.get("value2")

        # Append the log file.
        with open(path, 'a+', encoding='utf-8') as log_file:
            if message == 'NewSession':
                log_file.write(str(value) + "\n")  # Test case name.
                log_file.write("")
            elif message == 'General':
                type_log = "LOG"

                # Alignment.
                type_log = "{:<9}".format(type_log)

                log_file.write(datetime_log + " - " + type_log + " - " + value + "\n")

            elif message == 'EndExecution':
                log_file.write("\n " + "*" * 138 + "\n")
            else:
                log_file.write(datetime_log + " - Log       - " + value + " " + " - " + str(value1) + "\n")

    except Exception as ex:
        print(f"Log error: ", ex)


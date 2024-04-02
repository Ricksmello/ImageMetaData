import exifread
import datetime
import os
import socket
import shutil


datetime_log: str = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")

# Get the hostname.
hostname = socket.gethostname()
# Get the datetime.
date_log = str(datetime.datetime.now().strftime("%d.%m.%Y"))


def newFileName(**kwargs):
    """
    Generate the new file name.

    :argument:
        filename (str): The actual file name.
        full_path (str): Path to treat the files.
        full_path_log (str): Path of the log file.

    :returns:
        new_file_name (str): The new file name.
    """

    # Arguments.
    filename = kwargs.get("filename")
    full_path = kwargs.get("full_path")
    full_path_log = kwargs.get("full_path_log")

    try:
        with open(os.path.join(full_path, filename), 'rb') as image:  # file path and name
            exif = exifread.process_file(image)

        # Take the Data Taken, otherwise take the timestamp.
        if exif: ### Tem o EXIF mas não tem os campos necessários.
            new_file_name = str(exif['EXIF DateTimeOriginal'])
            file_width = str(exif['EXIF ExifImageWidth'])
            file_lenght = str(exif['EXIF ExifImageLength'])
            new_file_name = new_file_name + '_w_' + file_width + '_l_' + file_lenght
            new_file_name = new_file_name.replace(".", "")
            addLogs(full_path_log=full_path_log, message="General", value=f"File {filename} using Width and Lenght.")

        else:

            new_file_name = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
            new_file_name = new_file_name.strftime("%Y/%m/%d, %H:%M:%S.%f")
            addLogs(full_path_log=full_path_log, message="General", value=f"File {filename} using DateTime.")

        if ":" in new_file_name:
            new_file_name = new_file_name.replace(":", ".")
            new_file_name = new_file_name.replace("/", ".")
            new_file_name = new_file_name.replace(",", "")

        return new_file_name

    except Exception as ex:
        print(f"Log error: ", ex)


@staticmethod
def renameFile(**kwargs):
    """
    Reanem the file.

    :argument:
        old_name (str): The actual file name.
        new_name (str): The new file name.
        full_path (str): Path to treat the files.
        full_path_log (str): Path of the log file.

    :returns:
        No return.
    """

    # Args.
    full_path = kwargs.get("full_path")
    full_path_log = kwargs.get("full_path_log")
    old_name = os.path.join(full_path, kwargs.get("old_name"))
    new_name = os.path.join(full_path, kwargs.get("new_name"))

    # Rename file.
    try:
        os.rename(old_name, new_name)
        print(f"The file {old_name} was renamed to {new_name}.")
        addLogs(full_path_log=full_path_log, message="General", value=f"The file {old_name} was renamed to {new_name}.")
    except FileNotFoundError:
        print(f"The file {old_name} was not found.")
        addLogs(full_path_log=full_path_log, message="General", value=f"The file {old_name} was not found.")
    except FileExistsError:
        print(f"There is already a file with the name  {new_name}.")
        addLogs(full_path_log=full_path_log, message="General",
                value=f"There is already a file with the name  {new_name}.")
    except Exception as e:
        print(f"Something wrong happened: {e}")
        addLogs(full_path_log=full_path_log, message="General", value=f"Something wrong happened: {e}")


@staticmethod
def move_files_to_root(**kwargs):
    """
    Move image files to the root folder.

    :argument:
        full_path (str): Path to treat the files.

    :returns:
        No return.
    """

    # Args.
    full_path = kwargs.get("full_path")

    if not os.path.isdir(full_path):
        print(f'The path "{full_path}" is not a valid directory.')
        return

    for root, dirs, files in os.walk(full_path):
        for file in files:
            full_file_path = os.path.join(root, file)
            end = full_file_path.find(file) - 1
            file_path = full_file_path[:end]
            if file_path != full_path:
                shutil.move(full_file_path, full_path)
                print(f"FILE: {file} copied\n"
                      f"FROM: {file_path}\n"
                      f"TO  : {full_path}\n")


def addLogs(**kwargs):
    """
    Add logs in a file.

    :argument:
        full_path (str): Path to treat the files.

    :returns:
        No return.
    """

    try:
        # kwargs variables.
        message = kwargs.get("message")
        value = kwargs.get("value")
        full_path_log = kwargs.get("full_path_log")

        # Append the log file.
        with open(full_path_log, 'a+', encoding='utf-8') as log_file:
            if message == 'NewSession':
                log_file.write(f"\nNew Log Session - {datetime_log}\n\n")
            elif message == 'General':
                type_log = "LOG"

                # Alignment.
                type_log = "{:<9}".format(type_log)

                log_file.write(datetime_log + " - " + type_log + " - " + value + "\n")

            elif message == 'EndSession':
                log_file.write("\n " + "*" * 138 + "\n")
            else:
                raise

    except Exception as ex:
        print(f"Log error: ", ex)


import os

import functions.functions
import functions.functions as aux

folder = os.getcwd()
total_list = {}

date_log = functions.functions.date_log
hostname = functions.functions.hostname


class Main:

    def __init__(self):
        # List the files from the current folder.

        # Ask for the path to scan.
        print(f"Inform the path to scan the image files:")
        full_path = input()
        full_path = os.path.abspath(full_path)

        # Set Log file.
        log_file = date_log + " - " + hostname + ".log"
        log_file = os.path.join(full_path, log_file)

        full_path_log = os.path.join(full_path, log_file)

        aux.addLogs(full_path_log=full_path_log, message="NewSession") ### Full_path_log está com problema.
        aux.move_files_to_root(full_path=full_path)
        Main.listFiles(full_path_log=full_path_log, full_path=full_path)
        aux.addLogs(full_path_log=full_path_log, message="EndSession")

    @staticmethod
    def listFiles(**kwargs):
        """
        Lista all the files in a specific folder.

        :argument:
            full_path (str): Path to treat the files.
            full_path_log (str): Path of the log file.

        :returns:
            No return.
        """

        # Args.
        full_path = kwargs.get("full_path")
        full_path_log = kwargs.get("full_path_log")

        if not full_path:
            print(f'The folder "{full_path}" does not exist.')
            return

        # List the files.
        files = os.listdir(full_path)
        files = sorted(files, reverse=True)

        # Only pictures files.
        extension_image = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        # Show the name and the date.
        print(f'Files in folder "{full_path}":')
        aux.addLogs(full_path_log=full_path_log, message="NewSession", value="Read the files inside the folder.")

        for count, file in enumerate(files):

            # Verify the file extension.
            extension = os.path.splitext(file)[1].lower()

            # Generate the new file name.
            if extension in extension_image:
                new_file_name = (aux.newFileName(full_path_log=full_path_log, full_path=full_path, filename=file)
                                 + extension)
                total_list.setdefault(new_file_name, [])

            # Generate the new file name.
            if extension in extension_image:
                new_file_name = (aux.newFileName(full_path_log=full_path_log, full_path=full_path, filename=file)
                                 + extension)
            else:
                continue

            if new_file_name in total_list.keys():
                total_list.setdefault(new_file_name, []).append(file)

        print(total_list)

        # Rename de files.
        for item in total_list:

            extension = os.path.splitext(item)[1].lower()
            item_no_extension = os.path.splitext(item)[0].lower()

            if len(total_list[item]) > 1:
                for count, subitems in enumerate(total_list[item]):

                    aux.renameFile(full_path_log=full_path_log, full_path=full_path, old_name=subitems,
                                   new_name=item_no_extension + " - Duplicated " + (count + 1).__str__() + extension)
            else:
                aux.renameFile(full_path_log=full_path_log, full_path=full_path, old_name=total_list[item][0],
                               new_name=item_no_extension + extension)


if __name__ == "__main__":
    Main()

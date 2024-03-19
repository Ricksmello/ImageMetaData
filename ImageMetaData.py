import os
import functions.functions as aux

folder = os.getcwd()
total_list = {}


class Main:

    def __init__(self):
        # List the files from the current folder.

        aux.addLogs(message="NewSession")
        Main.listFiles(self)
        aux.addLogs(message="EndSession")

    @staticmethod
    def listFiles(self):
        """
        Lista all the files in a specific folder.

        :argument:
            No args.

        :returns:
            No return.
        """
        if not os.path.isdir(folder):
            print(f'The folder "{folder}" does not exist.')

            return

        # List the files.
        files = os.listdir(folder)
        files = sorted(files, reverse=True)

        # Only pictures files.
        extension_image = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        # Show the name and the date.
        print(f'Files in folder "{folder}":')
        aux.addLogs(message="New Session", value="Read the files inside the folder.")

        for count, file in enumerate(files):

            # Verify the file extension.
            extension = os.path.splitext(file)[1].lower()

            # Generate the new file name.
            if extension in extension_image:
                new_file_name = aux.newFileName(filename=file) + extension
                total_list.setdefault(new_file_name, [])

            # Generate the new file name.
            if extension in extension_image:
                new_file_name = aux.newFileName(filename=file) + extension
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

                    aux.renameFile(old_name=subitems,
                                   new_name=item_no_extension + " - Duplicated " + (count + 1).__str__() + extension)
            else:
                aux.renameFile(old_name=total_list[item][0], new_name=item_no_extension + extension)


if __name__ == "__main__":
    Main()

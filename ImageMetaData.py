import datetime
import os
import exifread

folders = os.getcwd()
duplicity_list = []
total_list = {}


class Main:

    def __init__(self):
        # List the files from the current folder.
        Main.listFiles(self)

    '------------------------------------------------------------------------------------------------------------------'
    ''
    '------------------------------------------------------------------------------------------------------------------'
    def listFiles(self, **kwargs):

        if not os.path.isdir(folders):
            print(f'O diretório "{folders}" não existe.')
            return

        # List the files.
        files = os.listdir(folders)
        files = sorted(files, reverse=True)

        # Only pictures files.
        extension_image = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        # Show the name and the date.
        print(f'Arquivos de imagem em "{folders}":')

        for count, file in enumerate(files):

            # Verify the file extension.
            extension = os.path.splitext(file)[1].lower()

            # Generate the new file name.
            if extension in extension_image:
                new_file_name = Main.newFileName(self, filename=file) + extension
                total_list.setdefault(new_file_name, [])

            # Generate the new file name.
            if extension in extension_image:
                new_file_name = Main.newFileName(self, filename=file) + extension
            else:
                continue

            if new_file_name in total_list.keys():
                total_list.setdefault(new_file_name, []).append(file)

        print(total_list)

    '------------------------------------------------------------------------------------------------------------------'
    ''
    '------------------------------------------------------------------------------------------------------------------'
    def newFileName(self, **kwargs):

        # Arguments.
        filename = kwargs.get("filename")

        full_path = os.path.join(folders, filename)

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

    '------------------------------------------------------------------------------------------------------------------'
    ''
    '------------------------------------------------------------------------------------------------------------------'
    def renameFile(self, **kwargs):

        # Arguments.
        old_name = kwargs.get("old_name")
        new_name = kwargs.get("new_name")

        # Rename file.
        try:
            os.rename(old_name, new_name)
            print(f"O arquivo {old_name} foi renomeado para {new_name}.")
        except FileNotFoundError:
            print(f"O arquivo {old_name} não foi encontrado.")
        except FileExistsError:
            print(f"Já existe um arquivo com o nome {new_name}.")
            duplicity_list[old_name] = new_name
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

        return duplicity_list

    '------------------------------------------------------------------------------------------------------------------'
    ''
    '------------------------------------------------------------------------------------------------------------------'
    def checkDuplicity(self, **kwargs):

        # Arguments.
        new_file_name = kwargs.get("new_file_name")

        # List the files.
        files = os.listdir(folders)

        # Show the name and the date.
        print(f'Arquivos de imagem em "{folders}":')
        for new_sequence in range(1, 100):

            # Verify if it is necessary to change the first file adding "Duplicated 1".
            if new_file_name in files:
                change_actual = True
            else:
                change_actual = False

            return change_actual


if __name__ == "__main__":
    Main()

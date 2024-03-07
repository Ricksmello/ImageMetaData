import datetime
import os
import exifread

folders = os.getcwd()
file_list = {}


class Main:

    def __init__(self):
        # List the files from the current folder.
        Main.listFiles(self)

    '------------------------------------------------------------------------------------------------------------------'
    ''
    '------------------------------------------------------------------------------------------------------------------'
    def listFiles(self, **kwargs):

        change_actual = False
        actual_sequence = 1

        if not os.path.isdir(folders):
            print(f'O diretório "{folders}" não existe.')
            return

        # List the files.
        files = os.listdir(folders)

        # Only pictures files.
        extension_image = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        # Show the name and the date.
        print(f'Arquivos de imagem em "{folders}":')
        for file in files:
            # Verify the file extension.
            extension = os.path.splitext(file)[1].lower()

            # Generate the new file name.
            if extension in extension_image:
                new_file_name = Main.newFileName(self, filename=file) + extension
            else:
                continue

            file_list[file] = new_file_name

        for old_name, new_name in file_list.items():
            print(old_name + " ----> " + new_name)

            extension = os.path.splitext(new_name)[1].lower()
            old_name = os.path.splitext(old_name)[0]
            new_name = os.path.splitext(new_name)[0]

            change_actual = (
                Main.checkDuplicity(self,
                                    new_file_name=new_name + " - duplicated_" + actual_sequence.__str__() +
                                                  extension, extension=extension))

            while change_actual:
                actual_sequence = actual_sequence + 1
                change_actual = (
                    Main.checkDuplicity(self,
                                        new_file_name=new_name + " - duplicated_" + actual_sequence.__str__() +
                                                      extension, extension=extension))

            Main.renameFile(self, file=old_name + extension,
                            new_file_name=new_name + " - duplicated_" + actual_sequence.__str__() + extension)

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
        file = kwargs.get("file")
        new_file_name = kwargs.get("new_file_name")

        # Rename file.
        try:
            os.rename(file, new_file_name)
            print(f"O arquivo {file} foi renomeado para {new_file_name}.")
        except FileNotFoundError:
            print(f"O arquivo {file} não foi encontrado.")
        except FileExistsError:
            print(f"Já existe um arquivo com o nome {new_file_name}.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

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

import datetime
import os
import exifread

folders = os.getcwd()
file_list = []


class Main:

    def __init__(self):
        # List the files from the current folder.
        Main.listFiles(self)

    def listFiles(self, **kwargs):

        if not os.path.isdir(folders):
            print(f'O diretório "{folders}" não existe.')
            return

        # List the files.
        files = os.listdir(folders)

        # Only pictures files.
        extension_image = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        # Only files did not change.
        #change_sintaxes = ['_w_', '_l_']

        # Show the name and the date.
        print(f'Arquivos de imagem em "{folders}":')
        for file in files:
            # Verify the file extension.
            extension = os.path.splitext(file)[1].lower()

            # Only files did not change.
            if file.__contains__('_w_') or file.__contains__('_l_'):
                has_change_sintaxe = True
            else:
                has_change_sintaxe = False

            if (extension in extension_image) and (has_change_sintaxe is False):
                print("-" * 50)
                print(f"File name: {file}")
                file_date_time = Main.showDateTime(self, filename=file)
                print(f"Created / Changed in: {file_date_time}")
                print("-" * 50)

                # Check before rename.
                new_name = Main.checkDuplicity(self, file_date_time, extension)

                # Rename the files.
                Main.renameFile(self, file, new_name)

    def showDateTime(self, filename):

        full_path = os.path.join(folders, filename)

        with open(full_path, 'rb') as image:  # file path and name
            exif = exifread.process_file(image)

        # Take the Data Taken, otherwise take the timestamp.
        if exif:
            file_date_time = str(exif['EXIF DateTimeOriginal'])
            file_width = str(exif['EXIF ExifImageWidth'])
            file_lenght = str(exif['EXIF ExifImageLength'])
            file_date_time = file_date_time + '_w_' + file_width + '_l_' + file_lenght
            file_date_time = file_date_time.replace(".", "")

        else:

            file_date_time = datetime.datetime.fromtimestamp(os.path.getmtime(full_path))
            file_date_time = file_date_time.strftime("%Y/%m/%d, %H:%M:%S.%f")

        if ":" in file_date_time:
            file_date_time = file_date_time.replace(":", ".")
            file_date_time = file_date_time.replace("/", ".")
            file_date_time = file_date_time.replace(",", "")

        return file_date_time

    def renameFile(self, file, new_name):

        # Rename file.
        try:
            os.rename(file, new_name)
            print(f"O arquivo {file} foi renomeado para {new_name}.")
        except FileNotFoundError:
            print(f"O arquivo {file} não foi encontrado.")
        except FileExistsError:
            print(f"Já existe um arquivo com o nome {new_name}.")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

    def checkDuplicity(self, file_date_time, extension):

        # List the files.
        files = os.listdir(folders)

        # Show the name and the date.
        print(f'Arquivos de imagem em "{folders}":')
        for new_sequence in range(1, 100):

            file_name = file_date_time + " - Duplicated_" + str(new_sequence) + extension

            if not (file_name in files):
                return file_name


if __name__ == "__main__":
    Main()

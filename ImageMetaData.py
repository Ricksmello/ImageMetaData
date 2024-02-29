import datetime
import os
import exifread

diretorio = os.getcwd()
file_list = []


class Main:

    def __init__(self):
        # List the files from the current folder.
        Main.listFiles(self, create_list=False)

    def listFiles(self, **kwargs):

        create_list = kwargs.get("create_list")

        if not os.path.isdir(diretorio):
            print(f'O diretório "{diretorio}" não existe.')
            return

        # List the files.
        arquivos = os.listdir(diretorio)

        # Only pictures files.
        extensoes_imagem = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        # Show the name and the date.
        print(f'Arquivos de imagem em "{diretorio}":')
        for arquivo in arquivos:
            # Verify the file extension.
            extension = os.path.splitext(arquivo)[1].lower()

            if extension in extensoes_imagem and create_list is False:
                print("-" * 50)
                print(f"File name: {arquivo}")
                file_date_time = Main.showDateTime(self, filename=arquivo)
                print(f"Created / Changed in: {file_date_time}")
                print("-" * 50)

                # Check before rename.
                new_name = Main.checkDuplicity(self, file_date_time, extension)

                # Rename the files.
                Main.renameFile(self, arquivo, new_name)

    def showDateTime(self, filename):

        full_path = os.path.join(diretorio, filename)

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
        files = os.listdir(diretorio)

        # Show the name and the date.
        print(f'Arquivos de imagem em "{diretorio}":')
        for new_sequence in range(1, 100):

            file_name = file_date_time + " - Duplicated_" + str(new_sequence) + extension

            if not (file_name in files): ### Está mudando mesmo que já tenha o Duplicated.
                return file_name


if __name__ == "__main__":
    Main()

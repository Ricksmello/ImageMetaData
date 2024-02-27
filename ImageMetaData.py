import datetime
import os
import exifread

diretorio = os.getcwd()

def main():
    # List the files from the current folder.
    listFiles()


def listFiles():
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
        # Verifica se a extensão do arquivo corresponde a uma extensão de imagem
        extension = os.path.splitext(arquivo)[1].lower()

        if extension in extensoes_imagem:
            print("-" * 50)
            print(f"File name: {arquivo}")
            file_date_time = showDateTime(filename=arquivo)
            print(f"Created / Changed in: {file_date_time}")
            print("-" * 50)

            # Rename the files.
            renameFile(arquivo, file_date_time, extension)


def showDateTime(filename):
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


def renameFile(file, file_date_time, extension):

    # Rename file.
    try:
        os.rename(file, file_date_time + extension)
        print(f"O arquivo {file} foi renomeado para {file_date_time}.")
    except FileNotFoundError:
        print(f"O arquivo {file} não foi encontrado.")
    except FileExistsError:
        os.rename(file, file_date_time + " - Duplicated_1" + extension)
        checkDuplicity(file)
        print(f"Já existe um arquivo com o nome {file_date_time}.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


def checkDuplicity(file):

    if "Duplicated" in file:
        position_number = file.rfind("_") + 1
        position_dot = file.rfind('.')

        return file[position_number:position_dot]


if __name__ == "__main__":
    main()


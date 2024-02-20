from PIL import Image, ExifTags
import datetime
import os


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
    file_date_time = datetime.datetime.fromtimestamp(os.path.getmtime(full_path)) ### Está pegando a data de modificação.
    file_date_time = file_date_time.strftime("%Y/%m/%d %H:%M:%S")

    file_date_time = file_date_time.replace(":", ".")
    file_date_time = file_date_time.replace("/", ".")

    return file_date_time


def renameFile(arquivo, file_date_time, extension):

    # Rename file.
    try:
        os.rename(arquivo, file_date_time + extension)
        print(f"O arquivo {arquivo} foi renomeado para {file_date_time}.")
    except FileNotFoundError:
        print(f"O arquivo {arquivo} não foi encontrado.")
    except FileExistsError:
        print(f"Já existe um arquivo com o nome {file_date_time}.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    main()


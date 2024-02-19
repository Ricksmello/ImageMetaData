from PIL import Image, ExifTags
import datetime
import os


def apresentarDataHora(filename):
    image_exif = Image.open(filename).getexif()
    if image_exif:
        # Make a map with tag names
        exif = {ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes}

        # Grab the date
        date_obj = exif["DateTime"]
        print('Modificado em:', date_obj)
    else:
        modify_time = os.path.getmtime(filename)
        modify_date = datetime.datetime.fromtimestamp(modify_time)
        print('Modificado em: ', modify_date.strftime("%d/%m/%Y %H:%M:%S"))


def listar_arquivos(diretorio):
    # Verifica se o diretório existe
    if not os.path.isdir(diretorio):
        print(f'O diretório "{diretorio}" não existe.')
        return

    # Lista todos os arquivos no diretório
    arquivos = os.listdir(diretorio)

    # Extensões de arquivo de imagem comuns
    extensoes_imagem = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    # Apresenta apenas os arquivos de imagem
    print(f'Arquivos de imagem em "{diretorio}":')
    for arquivo in arquivos:
        # Verifica se a extensão do arquivo corresponde a uma extensão de imagem
        if os.path.splitext(arquivo)[1].lower() in extensoes_imagem:
            print("-" * 50)
            print(f"Nome do arquivo: {arquivo}")
            apresentarDataHora(filename=arquivo)
            print("-" * 50)


if __name__ == "__main__":
    listar_arquivos(os.getcwd())


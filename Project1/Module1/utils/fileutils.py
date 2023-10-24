import os


def get_files_in_folder(folder_path) -> list:
    try:
        files_in_folder = sorted(list(filter(lambda file: os.path.isfile(os.path.join(folder_path, file)), os.listdir(folder_path))))
        return list(zip(files_in_folder, files_in_folder))
    except FileNotFoundError:
        return []


def delete_files(root_directory, files_names: list) -> None:
    for file in files_names:
        file_path = os.path.join(root_directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

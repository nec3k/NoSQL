import os


def get_files_in_folder(folder_path) -> list:
    if not os.path.isdir(folder_path):
        return []
    files_in_folder = list(filter(lambda entry: entry.is_file(), os.scandir(folder_path)))
    filenames = map(lambda file: file.name, files_in_folder)
    files_info = map(lambda file: {"filename": file.name, "size": file.stat().st_size, "ctime": file.stat().st_ctime}, files_in_folder)
    return list(zip(filenames, files_info))


def delete_files(root_directory, files_names: list) -> None:
    for file in files_names:
        file_path = os.path.join(root_directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

import os
from setting import DATA_DIR


def add_to_local(files):
    if not files:
        return "[Warning]: File is not None"
    new_files = []
    exist_files = []
    try:
        for uploaded_file in files:
            bytes_data = uploaded_file.read()
            file_path = os.path.join(DATA_DIR, uploaded_file.name)
            if not os.path.exists(file_path):
                with open(file_path, "w", encoding="utf8") as f:
                    f.write(bytes_data.decode("utf8"))
                    new_files.append(uploaded_file.name)
            else:
                exist_files.append(uploaded_file.name)
        if new_files and not exist_files:
            return "[Success]: Add success"
        if not new_files and exist_files:
            return f"[Warning]: {', '.join(exist_files)} already exist"
        if new_files and exist_files:
            return {
                "Success": f"[Success]: {', '.join(new_files)} add success",
                "Warning": f"[Warning]: {', '.join(exist_files)} already exist"
            }
    except Exception as e:
        raise e


def get_data_info():
    files = os.listdir(DATA_DIR)
    total_size = sum([
        os.path.getsize(os.path.join(DATA_DIR, name))
        for name in files
    ])
    info_dict = {
        "files": files,
        "len": len(files),
        "total_size": total_size
    }
    return info_dict


def remove_file(file_name):
    return os.remove(os.path.join(DATA_DIR, file_name))


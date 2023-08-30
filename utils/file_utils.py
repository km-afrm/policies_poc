import os


def get_latest_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None

    return max(files)


def get_latest_version(directory):
    return get_latest_file(directory).split(".")[0]

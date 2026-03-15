import os

def get_directory_size(path):
    total = 0

    for root, dirs, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)

            try:
                total += os.path.getsize(fp)
            except:
                pass

    return total

def human_readable(size):
    for unit in ["B","KB","MB","GB","TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
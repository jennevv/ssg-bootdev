import os
import shutil


def cp_dir(src: str, dst: str) -> None:
    if not os.path.exists(src):
        raise ValueError(f"Source directory {src} does not exist.")
    if os.path.exists(dst):
        shutil.rmtree(dst)

    cp_recursively(src, dst)

    return


def cp_recursively(src: str, dst: str):
    if not os.path.exists(dst):
        os.mkdir(dst)

    contents_current_dir = os.listdir(src)
    paths_current_dir = [os.path.join(src, content) for content in contents_current_dir]
    src_subdirs = list(filter(os.path.isdir, paths_current_dir))
    src_files = list(filter(os.path.isfile, paths_current_dir))

    if len(src_subdirs) == 0:
        for src_file in src_files:
            dst_file = os.path.join(dst, os.path.basename(src_file))
            _ = shutil.copy(src_file, dst_file)
    else:
        for src_file in src_files:
            dst_file = os.path.join(dst, os.path.basename(src_file))
            _ = shutil.copy(src_file, dst_file)
        for src_subdir in src_subdirs:
            dst_subdir = os.path.join(dst, os.path.basename(src_subdir))
            cp_recursively(src_subdir, dst_subdir)

    return


def log_path(path: str) -> None:
    print(f"Current path: {path}")

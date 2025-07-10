import re
import os
from .markdown_to_html_node import markdown_to_html_node


def extract_title(md: str) -> str:
    match: list[str] = re.findall(r"(?m)^# (.*)", md, re.MULTILINE)
    if match != []:
        title = match[0].strip()
        return title
    else:
        raise ValueError("No header found.")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        md = f.read()

    with open(template_path) as f:
        template = f.read()

    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    with open(dest_path, "x") as f:
        _ = f.write(template)

    return


def generate_pages_recursively(from_path: str, template_path: str, dest_path: str):
    dir_contents = os.listdir(from_path)
    paths_dir_contents = [os.path.join(from_path, content) for content in dir_contents]

    src_files = list(filter(os.path.isfile, paths_dir_contents))
    dest_files = [os.path.join(dest_path, os.path.basename(file)) for file in src_files]
    dest_files = [os.path.splitext(file)[0] + ".html" for file in dest_files]
    print(dest_files)

    src_subdirs = list(filter(os.path.isdir, paths_dir_contents))
    dest_subdirs = [
        os.path.join(dest_path, os.path.basename(subdir)) for subdir in src_subdirs
    ]

    for src_file, dest_file in zip(src_files, dest_files):
        if os.path.splitext(src_file)[1] == ".md":
            generate_page(src_file, template_path, dest_file)

    if src_subdirs != []:
        for src_subdir, dest_subdir in zip(src_subdirs, dest_subdirs):
            os.mkdir(dest_subdir)
            generate_pages_recursively(src_subdir, template_path, dest_subdir)

    return

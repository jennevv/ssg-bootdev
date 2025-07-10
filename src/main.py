from .cp_dir import cp_dir
from .generate_page import generate_page, generate_pages_recursively

from sys import argv


def main():
    src = "static/"
    dst = "docs/"

    basepath = argv[1] if len(argv) > 1 else "/"

    cp_dir(src, dst)

    generate_pages_recursively("content/", "template.html", dst, basepath)


if __name__ == "__main__":
    main()

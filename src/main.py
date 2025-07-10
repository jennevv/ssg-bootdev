from .cp_dir import cp_dir
from .generate_page import generate_page, generate_pages_recursively


def main():
    src = "static/"
    dst = "public/"

    cp_dir(src, dst)

    generate_pages_recursively("content/", "template.html", "public/")


if __name__ == "__main__":
    main()

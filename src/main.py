import os
import shutil
import sys
from utils import *

def copy_files(src, dest):
    # copy files from src to dest recursively, it should clear the dest directory first and log each file copied
    if os.path.exists(dest):
        shutil.rmtree(dest)
    
    if not os.path.exists(dest):
        os.makedirs(dest)

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            copy_files(s, d)
        else:
            if not os.path.exists(d):
                print(f"Copying {s} to {d}")
                shutil.copy2(s, d)

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    # read the source file
    with open(from_path, 'r') as f:
        source = f.read()

    # read the template file
    with open(template_path, 'r') as f:
        template = f.read()
    
    title = extract_title(source)
    html = markdown_to_html_node(source).to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    # write the generated file to the destination path, creating the directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    with open(dest_path, 'w') as f:
        f.write(template)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    # Generate pages recursively from dir_path_content to dest_dir_path using template_path
    for item in os.listdir(dir_path_content):
        s = os.path.join(dir_path_content, item)
        d = os.path.join(dest_dir_path, item.replace(".md", ".html"))  # Ensure .md files are converted to .html
        if os.path.isdir(s):
            # Recursively process subdirectories
            generate_pages_recursive(basepath, s, template_path, d)
        elif s.endswith(".md"):  # Only process Markdown files
            print(f"Generating page from {s} to {d} using template {template_path}")
            generate_page(basepath, s, template_path, d)

def main():
    # set basepath to argv[1] if provided, else '/'
    print("Basepath:", sys.argv[1] if len(sys.argv) > 1 else "/")
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # copy_files("static", "public")
    generate_pages_recursive(basepath, "content", "template.html", "docs")
    



if __name__ == "__main__":
    main()
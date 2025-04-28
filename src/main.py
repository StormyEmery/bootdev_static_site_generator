from textnode import TextNode, TextType
import os
import shutil

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

def main():
    copy_files("static", "public")
    

if __name__ == "__main__":
    main()
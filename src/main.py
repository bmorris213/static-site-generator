import os
import shutil

def copy_to(source_dir, target_dir):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct full paths for source and target directories based on the script's directory
    source_directory = os.path.join(script_dir, source_dir)
    target_directory = os.path.join(script_dir, target_dir)

    if not os.path.exists(source_directory):
        raise Exception(f"Path of {source_directory} does not exist")
    
    # if target does not exist, make target
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    print(f"copying {source_directory} to {target_directory}")

    for item in os.listdir(source_directory):
        source = os.path.join(source_directory, item)
        target = os.path.join(target_directory, item)
        print(f"looking at {item}")
        if os.path.isdir(source):
            copy_to(source, target)
        else:
            shutil.copy2(source, target)

def delete_contents(target_directory):
    shutil.rmtree

destination_folder = "public"
source_folder = "static"

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(script_dir, destination_folder)
    source = os.path.join(script_dir, source_folder)

    print("deleting contents of public")
    shutil.rmtree(target)
    os.makedirs(target)
    print("copying files...")
    copy_to(source,target)

if __name__ == "__main__":
    main()
import os
import shutil
import re
from textnode import TextNode

def generate_pages_recursively(source_dir, template_dir, target_dir):
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir , item)
        new_target = os.path.join(target_dir , item)
        if os.path.isdir(item_path):
            if not os.path.exists(new_target):
                os.makedirs(new_target)
            generate_pages_recursively(item_path, template_dir, new_target)
        elif os.path.isfile(item_path):
            generate_page(source_dir, template_dir, target_dir)

def generate_page(source_dir, template_dir, target_dir):
    source_document = "index.md"
    template_document = "template.html"
    target_document = "index.html"
    # read markdown file at source_dir
    markdown_data = ""
    with open(f"{source_dir}/{source_document}", "r") as source_file:
        markdown_data = markdown_data + source_file.read()
    
    # read template file at template_dir
    html_data = ""
    with open(f"{template_dir}/{template_document}", "r") as template_file:
        html_data = html_data + template_file.read()
    # use process_doc to convert the text
    html_string = TextNode.process_doc(markdown_data).to_html()

    # extract the title
    title_string = extract_title(html_string)

    # replace {{ Title }} and {{ Content }} from template
    html_data = html_data.replace("{{ Title }}", title_string)
    html_data = html_data.replace("{{ Content }}", html_string)

    # write the new document to target_dir
    with open(f"{target_dir}/{target_document}", "w") as target_document:
        target_document.write(html_data)

def extract_title(html):
    search_results = re.search(r'<h1>(.*?)</h1>', html)
    if search_results == None:
        raise Exception("Page has no title...")
    return search_results.group(1)

def copy_to(source_dir, target_dir):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    components = script_dir.split(os.sep)
    if components:
        components.pop()
    script_dir = os.path.join(*components)
    script_dir = f"/{script_dir}"
    
    # Construct full paths for source and target directories based on the script's directory
    source_directory = os.path.join(script_dir, source_dir)
    target_directory = os.path.join(script_dir, target_dir)

    if not os.path.exists(source_directory):
        raise Exception(f"Path of {source_directory} does not exist")
    
    # if target does not exist, make target
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for item in os.listdir(source_directory):
        source = os.path.join(source_directory, item)
        target = os.path.join(target_directory, item)
        if os.path.isdir(source):
            copy_to(source, target)
        else:
            shutil.copy2(source, target)

def main():
    destination_folder = "public"
    source_folder="static"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    components = script_dir.split(os.sep)
    if components:
        components.pop()
    script_dir = os.path.join(*components)
    script_dir = f"/{script_dir}"

    target = os.path.join(script_dir, destination_folder)
    source = os.path.join(script_dir, source_folder)

    shutil.rmtree(target)
    os.makedirs(target)
    copy_to(source,target)
    
    target = os.path.join(script_dir, "public")
    source = os.path.join(script_dir, "content")

    generate_pages_recursively(source,script_dir,target)

if __name__ == "__main__":
    main()
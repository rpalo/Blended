import os
import sys
import shutil
import fileinput
import webbrowser
import fileinput
import datetime
import click
from random import randint
import pkg_resources

# Very important, get the directory that the user wants run commands in
cwd = os.getcwd()
app_version = pkg_resources.require("blended")[0].version

@click.group()
def cli():
    """Blended: Static Website Generator"""

@cli.command('version', short_help='Show which version of Blended you are running.')
def version():
    """Prints Blended's current version"""

    print("You are running Blended v"+app_version)

@cli.command('init', short_help='Initiate a new website')
def init():
    """Initiates a new website"""
    print("Blended: Static Website Generator -\n")
    wname = raw_input("Website Name: ")
    wdesc = raw_input("Website Description: ")
    wlan = raw_input("Website Language: ")
    wlic = raw_input("Website License: ")
    aname = raw_input("Author(s) Name(s): ")

    # Create the templates folder
    templ_dir = os.path.join(cwd, "templates")
    if not os.path.exists(templ_dir):
        os.makedirs(templ_dir)

    # Create the content folder
    cont_dir = os.path.join(cwd, "content")
    if not os.path.exists(cont_dir):
        os.makedirs(cont_dir)

    # Populate the configuration file
    config_file_dir = os.path.join(cwd, "config.py")
    config_file = open(config_file_dir, "w")
    config_file.write('# configuration is atuomatically generated by Blended, feel free to edit any values\n\n')
    config_file.write('website_name = "'+wname+'"\n')
    config_file.write('website_description = "'+wdesc+'"\n')
    config_file.write('website_license = "'+wlic+'"\n')
    config_file.write('author_name = "'+aname+'"\n')
    config_file.write('website_language = "'+wlan+'"\n')
    config_file.write('home_page_list = "no"\n')
    config_file.write('\n')
    config_file.close()

    print("\nThe required files for your website have been generated.")

@cli.command('clean', short_help='Remove the build folder')
def clean():
    """Removes all built files"""
    print("Removing the built files!")

    # Remove the  build folder
    build_dir = os.path.join(cwd, "build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

@cli.command('purge', short_help='Purge all the files created by Blended')
def purge():
    """Removes all files generated by Blended"""
    print("Purging the Blended files!")

    # Remove the templates folder
    templ_dir = os.path.join(cwd, "templates")
    if os.path.exists(templ_dir):
        shutil.rmtree(templ_dir)

    # Remove the content folder
    cont_dir = os.path.join(cwd, "content")
    if os.path.exists(cont_dir):
        shutil.rmtree(cont_dir)

    # Remove the  build folder
    build_dir = os.path.join(cwd, "build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    # Remove config.py
    config_file_dir = os.path.join(cwd, "config.py")
    if os.path.exists(config_file_dir):
        os.remove(config_file_dir)

    # Remove config.pyc
    config2_file_dir = os.path.join(cwd, "config.pyc")
    if os.path.exists(config2_file_dir):
        os.remove(config2_file_dir)

@cli.command('build', short_help='Build the Blended files into a website')
def build():
    """Blends the generated files and outputs a html website"""

    # Make sure there is actually a configuration file
    config_file_dir = os.path.join(cwd, "config.py")
    if not os.path.exists(config_file_dir):
        sys.exit("There dosen't seem to be a configuration file. Have you run the init command?")
    else:
        sys.path.insert(0, cwd)
        from config import website_name, website_description, website_license, author_name, website_language, home_page_list

    print("Building your Blended files into a website!")
    
    # Create the build folder
    build_dir = os.path.join(cwd, "build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
        os.makedirs(build_dir)
    else:
        os.makedirs(build_dir)

    # Make sure there is actually a header template file
    header_file_dir = os.path.join(cwd, "templates", "header.html")
    if not os.path.exists(header_file_dir):
        sys.exit("There dosen't seem to be a header template file. You need one to generate.")

    # Make sure there is actually a footer template file
    footer_file_dir = os.path.join(cwd, "templates", "footer.html")
    if not os.path.exists(footer_file_dir):
        sys.exit("There dosen't seem to be a footer template file. You need one to generate.")

    # Open the header and footer files for reading
    header_file = open(header_file_dir, "r")
    footer_file = open(footer_file_dir, "r")

    # Create the html page listing
    page_list = '<ul class="page-list">\n'
    for filename in os.listdir(os.path.join(cwd, "content")):
        page_list = page_list + '<li class="page-list-item"><a href="'+filename+'">'+filename.replace(".html", "")+'</a></li>\n'
    page_list = page_list + '</ul>'

    if home_page_list == "yes":
        # Open the home page file (index.html) for writing
        home_working_file = open(os.path.join(cwd, "build", "index.html"), "w")

        home_working_file.write(header_file.read())

        # Make sure there is actually a home page template file
        home_templ_dir = os.path.join(cwd, "templates", "home_page.html")
        if os.path.exists(home_templ_dir):
            home_templ_file = open(home_templ_dir, "r")
            home_working_file.write(home_templ_file.read())
        else:
            print("No home page template file found. Writing page list to index.html")
            home_working_file.write(page_list)

        home_working_file.write(footer_file.read())

        home_working_file.close()

    for filename in os.listdir(os.path.join(cwd, "content")):
        header_file = open(header_file_dir, "r")
        footer_file = open(footer_file_dir, "r")
        currents_working_file = open(os.path.join(cwd, "build", filename), "w")

        # Write the header
        currents_working_file.write(header_file.read())

        # Get the actual stuff we want to put on the page
        text_content = open(os.path.join(cwd, "content", filename), "r")
        text_cont1 = text_content.read()

        # Write the text content into the content template and onto the build file
        content_templ_dir = os.path.join(cwd, "templates", "content_page.html")
        if os.path.exists(content_templ_dir):
            content_templ_file = open(content_templ_dir, "r")
            content_templ_file1 = content_templ_file.read()
            content_templ_file2 = content_templ_file1.replace("{page_content}", text_cont1)
            currents_working_file.write(content_templ_file2)
        else:
            currents_working_file.write(text_cont1)

        # Write the footer to the build file
        currents_working_file.write(footer_file.read())

        # Close the build file
        currents_working_file.close()

    # Replace global variables such as site name and language
    for filename in os.listdir(os.path.join(cwd, "build")):
        for line in fileinput.input(os.path.join(cwd, "build", filename), inplace=1):
            line = line.replace("{website_name}", website_name)
            line = line.replace("{website_description}", website_description)
            line = line.replace("{website_license}", website_license)
            line = line.replace("{website_language}", website_language)
            line = line.replace("{author_name}", author_name)
            line = line.replace("{random_number}", str(randint(0,100000000)))
            line = line.replace("{build_date}", str(datetime.datetime.now().date()))
            line = line.replace("{build_time}", str(datetime.datetime.now().time()))
            line = line.replace("{build_datetime}", str(datetime.datetime.now()))
            line = line.replace("{page_list}", page_list)
            print line.rstrip('\n')
        fileinput.close()

    # Copy the asset folder to the build folder
    shutil.copytree(os.path.join(cwd, "templates", "assets"), os.path.join(cwd, "build", "assets"))

    print("The files are built! You can find them in the build/ directory. Run the view command to see what you have created in a web browser.")


@cli.command('view', short_help='View the finished Blended website')
def view():
    """Opens the built index.html file in a web browser"""

    index_path = os.path.realpath(os.path.join(cwd, "build", "index.html"))
    if os.path.exists(index_path):
        webbrowser.open('file://' + index_path)
    else:
        print("The index.html file could not be found! Have you deleted it or have you built with home_page_list set to 'no' in config.py?")

if __name__ == '__main__':
    cli()

import yaml

# Load the CLoader class if it is available,
# otherwise fall back to the default Loader class
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def load_envvars(base_dir):
    try:
        # Try to open the .envvars.yaml file in the current directory
        with open("./.envvars.yaml", "r") as yaml_file:
            envvars = yaml.load(yaml_file, Loader=Loader)
    except FileNotFoundError:
        # If the file is not found, try to open it in the parent directory of base_dir
        with open(str(base_dir.parent) + "/.envvars.yaml", "r") as yaml_file:
            envvars = yaml.load(yaml_file, Loader=Loader)
    return envvars

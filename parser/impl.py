import json
import os

from parser.errors import ValidationException
from utils.file_utils import get_latest_file, get_latest_version

'''
Explore some of the config management libraries like: 
1. https://hydra.cc/docs/intro/
2.  
'''


class PolicyParser:

    def __init__(self, directory_path, base_version=None, region='us', platform='affirm', region_version=None,
                 platform_version=None, custom_key=None, custom_key_version=None):
        self.dir = directory_path
        self.base_path = os.path.join(directory_path, "base")
        if base_version is None:
            self.base_version = get_latest_version(self.base_path)
        else:
            self.base_version = base_version

        print("Base version: " + self.base_version)

        self.region_version = region_version
        self.platform_version = platform_version

        self.base_path = os.path.join(self.base_path, self.base_version + ".json")

        self.region = region
        self.platform = platform

        self.custom_key = custom_key
        self.custom_key_version = custom_key_version

        rendered_config = self._load_default_config()
        if self._validate_config(rendered_config):
            self.rendered_config = rendered_config
        else:
            self.rendered_config = None
            raise ValidationException("Failed validations for rendered config")

    @staticmethod
    def _validate_config(config):
        if config is None:
            return False
        # Implement all the checks here
        return True

    def _read_base_config(self):
        try:
            print("Loading: ", self.base_path)
            with open(self.base_path, 'r') as base_config_file:
                return json.load(base_config_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Base config file '{self.base_path}' not found.")
        except Exception as e:
            raise Exception(f"An error occurred while reading the base config: {e}")

    @staticmethod
    def _apply_overrides(base_config, override_json_path):
        try:
            with open(override_json_path, 'r') as override_json_file:
                overrides = json.load(override_json_file)

            base_config.update(overrides)
            print(f"Overrides applied based on '{override_json_path}'.")
            return base_config
        except FileNotFoundError:
            print("File not found.")
            return base_config
        except Exception as e:
            print(f"An error occurred: {e}")

    def _load_default_config(self):
        # Precedence of loading configs base -> region -> platform
        base_config = self._read_base_config()
        region_overidden = self._load_region_config(base_config)
        platform_overriden = self._load_platform_config(region_overidden)
        return self._load_custom_key_config(platform_overriden)

    def _load_region_config(self, base_config):
        region_path = os.path.join(self.dir, "region", self.region)
        if self.region_version is None:
            # Throw an exception perhaps
            print("Looking up latest region version")
            self.region_version = get_latest_version(region_path)

        region_file = os.path.join(region_path, self.region_version + ".json")
        return self._apply_overrides(base_config, region_file)

    # Loads the latest platform config if it exists or else return the base config
    def _load_platform_config(self, base_config):
        if self.platform is None:
            return base_config

        platform_path = os.path.join(self.dir, "platform", self.platform, self.region)

        if self.platform_version is None:
            print("Looking up latest platform version")
            self.platform_version = get_latest_version(platform_path)

        print("Platform version: " + self.platform_version)
        platform_path_file = os.path.join(platform_path, self.platform_version + ".json")
        return self._apply_overrides(base_config, platform_path_file)

    def _load_custom_key_config(self, base_config):
        if self.custom_key is None:
            return base_config

        custom_key_dir_path = os.path.join(self.dir, "custom", self.custom_key)

        if self.custom_key_version is None:
            print("Looking up latest custom_key version for key: " + self.custom_key)
            self.custom_key_version = get_latest_version(custom_key_dir_path)

        print("Custom Key version: " + self.custom_key_version)
        custom_key_path_file = os.path.join(custom_key_dir_path, self.custom_key_version + ".json")
        return self._apply_overrides(base_config, custom_key_path_file)

    def render_latest_policy(self):
        return self.rendered_config

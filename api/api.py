import os
from abc import ABC, abstractmethod

from models.models import DomainMapping
from parser.impl import PolicyParser
from store.local_storage import InMemLocalStorage


class PolicyManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def lookup_policy(self, domain, domain_id):
        """Retrieve a policy with the given domain and snapshots for a domain ID."""
        pass

    @abstractmethod
    def generate_store_policies(self, domain, domain_id, platform, base_version=None, region_version=None,
                                platform_version=None):
        """Generates the policy for a given platform"""
        pass


class LocalPolicyManager(PolicyManager):

    def __init__(self, policies_path, domain_mapping_store: InMemLocalStorage):
        self.domain_mapping_store = domain_mapping_store
        self.region = os.getenv('region', 'us')  # default to US region if it doesnt exist or consider throwing an error
        self.parser_store = {}
        self.policies_path = policies_path
        self.platform_latest_parsers = {}

    def lookup_policy(self, domain, domain_id):
        return self.domain_mapping_store.lookup(domain_id, domain)

    def generate_store_policies(self, domain, domain_id, platform, base_version=None, region_version=None,
                                platform_version=None, custom_key=None, custom_key_version=None):

        key = self.__lookup_policy_store_key__(base_version, region_version, platform,
                                               platform_version, custom_key, custom_key_version)

        if key not in self.parser_store:
            # Load the latest version of policy and store it.
            self.parser_store[key] = PolicyParser(self.policies_path, base_version=base_version, region=self.region,
                                                  platform=platform, region_version=region_version,
                                                  platform_version=platform_version,
                                                  custom_key=custom_key, custom_key_version=custom_key_version)

        # Further optimization can be made to cache the latest version of configs across all nodes.
        parser = self.parser_store[key]
        # Store in domain mapping store
        self.domain_mapping_store.store(DomainMapping(reference_id=domain_id, reference_id_type=domain,
                                                      base_version=parser.base_version,
                                                      region=self.region, region_version=parser.region_version,
                                                      platform=platform, platform_version=parser.platform_version,
                                                      custom_key=custom_key, custome_key_version=custom_key_version))
        return parser.render_latest_policy()

    @staticmethod
    def __lookup_policy_store_key__(base_version=None, region_version=None,
                                    platform="affirm", platform_version=None, custom_key=None,
                                    custom_key_version=None):
        if base_version is None:
            base_version = ""

        if region_version is None:
            region_version = ""

        if platform_version is None:
            platform_version = ""

        if custom_key is None:
            custom_key = ""

        if custom_key_version is None:
            custom_key_version = ""

        return base_version + "," + region_version + "," + platform + "," \
               + platform_version + "," + custom_key + "," + custom_key_version

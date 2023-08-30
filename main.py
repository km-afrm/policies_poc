# This is a sample Python script.
from api.api import LocalPolicyManager
from parser.impl import PolicyParser
from store.local_storage import InMemLocalStorage
from utils.file_utils import get_latest_file

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


if __name__ == '__main__':
    # Example usage
    # Load latest files with a policy parse
    base_path = 'policies'
    # config_manager = PolicyParser(base_path)
    # print(config_manager.render_latest_policy())

    # Load policy manager with a in memory implementation for storing domain specific configs and base path
    policy_manager = LocalPolicyManager(policies_path=base_path, domain_mapping_store=InMemLocalStorage())

    # Generates and stores the latest policy for order id "order_id_123456" and domain "order" for platform "affirm".
    # Default region is "us" but it can also be inferred from env variobles or kube config
    print(policy_manager.generate_store_policies(domain_id="order_id_123456", domain="order", platform="affirm"))

    # Lookup cached or snapshoted policy for "order_id_123456", "order"
    print("Looked up domain: ", policy_manager.lookup_policy(domain_id="order_id_123456", domain="order").__dict__)

    # Generates and stores latest config for a given custom key

    # Generates and stores the latest policy for order id "order_id_123456" and domain "order" for platform "affirm".
    # Default region is "us" but it can also be inferred from env variobles or kube config
    print(policy_manager.generate_store_policies(domain_id="order_id_1234567", domain="order", platform="affirm",
                                                 custom_key="segment_ramp_v1"))

    # Lookup cached or snapshoted policy for "order_id_123456", "order"
    print("Looked up domain: ", policy_manager.lookup_policy(domain_id="order_id_1234567", domain="order").__dict__)

    # More to explore explore:
    # Json schema validator: http://json-schema.org/ and/or say an open spec for our policies
    #

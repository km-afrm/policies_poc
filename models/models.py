from datetime import datetime


class DomainMapping:

    def __init__(self, reference_id, reference_id_type, base_version, region, platform, region_version, platform_version, custom_key= None, custome_key_version = None):
        self.referenceID = reference_id
        self.referenceIDType = reference_id_type
        self.baseVersion = base_version
        self.region = region
        self.platform = platform
        self.region_version = region_version
        self.platform_version = platform_version
        self.custom_key = custom_key
        self.custom_key_version = custome_key_version
        self.createdAt = datetime.now()
        self.startTime = datetime.now()

    def get_key(self):
        return self.construct_key(self.referenceID, self.referenceIDType)

    @staticmethod
    def construct_key(key_id, id_type):
        return key_id + "_" + id_type


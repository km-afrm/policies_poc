from models.models import DomainMapping


class InMemLocalStorage:

    def __init__(self):
        self.domainMap = {}

    def store(self, mapping: DomainMapping):
        self.domainMap[mapping.get_key()] = mapping

    def lookup(self, reference_id, reference_id_type):
        return self.domainMap[DomainMapping.construct_key(reference_id, reference_id_type)]
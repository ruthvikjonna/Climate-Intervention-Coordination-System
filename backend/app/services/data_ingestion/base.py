from abc import ABC, abstractmethod

class BaseIngestion(ABC):
    """
    Abstract base class for all data ingestion plugins.
    """
    @abstractmethod
    def authenticate(self):
        """Authenticate with the data source if needed."""
        pass

    @abstractmethod
    def download(self, *args, **kwargs):
        """Download raw data from the data source."""
        pass

    @abstractmethod
    def parse(self, raw_data):
        """Parse the raw data into a usable format (e.g., dict, DataFrame)."""
        pass

    @abstractmethod
    def store(self, parsed_data):
        """Store the parsed data in the database."""
        pass 
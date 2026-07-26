import boto3
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

def get_parameters(parameter_name: str) -> str:
    """
    Fetches a parameter value from AWS Systems Manager Parameter Store.

    Args:
        parameter_name (str): The name of the parameter to retrieve.

    Returns:
        str: The value of the parameter.
    """
    try:
        ssm = boto3.client('ssm', region_name=os.environ['AWS_REGION'])
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
        par = response['Parameter']['Value']
        if not par:
            raise ValueError(f"Parameter {parameter_name} is empty.")
        return par
    except Exception as e:
        raise RuntimeError(f"Error fetching parameter {parameter_name}: {e}") from e
        
class ConfigSettings:
    def __init__(self):
        if ENVIRONMENT == 'production':
            self._load_production()
        else:
            self._load_development()

    def _load_development(self):
        self.db_host = os.environ['DB_HOST']
        self.db_password = os.environ['DB_PASSWORD']
        self.db_name = os.environ['DB_NAME']
        self.user = os.environ['DB_USER']
        self.api_games = os.environ['API_GAMES']
        self.api_image = os.environ['API_IMAGE']
        self.api = os.environ['API']
        self.llm_key = os.environ['LLM_KEY']
        self.system_prompt = os.environ['SYSTEM_PROMPT']
        self.sync_key = os.environ['SYNC_KEY']
        self.aws_region = os.environ['AWS_REGION']
        self.sqs_queue = os.environ['SQS_QUEUE']
        self.sqs_endpoint = os.environ['SQS_ENDPOINT']
        self.s3_bucket = os.environ['S3_BUCKET']
        self.games_page_1 = os.environ['GAMES_PAGE_1']
        self.games_page_2 = os.environ['GAMES_PAGE_2']
        self.queries = os.environ['QUERIES']
        self.images = os.environ['IMAGES']
        
    def _load_production(self):
        self.db_host = get_parameters('/games/host')
        self.db_password = get_parameters('/games/db-password')
        self.db_name = get_parameters('/games/db-name')
        self.user = get_parameters('/games/db-user')
        self.api_games = get_parameters('/games/api-games')
        self.api_image = get_parameters('/games/api-image')
        self.api = get_parameters('/games/api')
        self.llm_key = get_parameters('/games/llm-key')
        self.system_prompt = get_parameters('/games/system-prompt')
        self.sync_key = get_parameters('/games/sync-key')
        self.aws_region = get_parameters('/games/aws-region')
        self.sqs_queue = get_parameters('/games/sqs-queue')
        self.sqs_endpoint = None
        self.s3_bucket = get_parameters('/games/s3-bucket')

    @property
    def database_url(self) -> str:
        """
        Creates the postgres database URL from the config settings.

        Returns:
            str: The database URL.
        """
        return f"postgresql://{self.user}:{self.db_password}@{self.db_host}/{self.db_name}"

    @property
    def async_database_url(self) -> str:
        """
        Creates the async postgres database URL from the config settings.

        Returns:
            str: The async database URL.
        """
        return f"postgresql+asyncpg://{self.user}:{self.db_password}@{self.db_host}/{self.db_name}"

@lru_cache()
def get_config_settings() -> ConfigSettings:
    """
    Retrieves the config settings.

    Returns:
        ConfigSettings: ConfigSettings object containing all config values.
    """
    return ConfigSettings()

config_settings = get_config_settings()

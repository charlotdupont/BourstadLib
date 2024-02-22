"""
Config module for BourstadLib
"""

from decouple import config  #type: ignore


class DatabaseConfigError(Exception):
    def __init__(self, error_message):
        message = f"""
        \033[1m
        To config your database, you can either pass in a dict or add the values to the env:
        -- "\033[1;35mDB_NAME\033[0m": \033[1;35mSQLite, PostgreSQL or MySQL\033[0m
        -- "\033[1;35mCONNECTION_STRING\033[0m": \033[1;35mConnection string for your database.\033[0m
        \n \033[1m\033[1;36m{error_message}\033[0m
        \033[0m
        """
        super().__init__(message)

def raiseConfigError(*args, **kwargs):
    raise DatabaseConfigError(*args, **kwargs)

def _get_keys_from_env() -> dict:
    data:dict =  {
        "FMP_API_KEY": config("FMP_API_KEY", None),
        "NASDAQ_API_KEY": config("NASDAQ_API_KEY", None),
        "ALPHA_VANTAGE_API_KEY": config("ALPHA_VANTAGE_API_KEY", None),
        }
    return {key: value for key, value in data.items() if value is not None}

def _get_database_config_from_env() -> dict:
    try:
        data:dict = {
        "DB_NAME": config("DB_NAME"),
        "CONNECTION_STRING": config("CONNECTION_STRING")
    }
    except Exception as e:
        raise DatabaseConfigError(str(e))
    return {key: value for key, value in data.items() if value is not None}

class Config:
    def __init__(self,
                 database_config: dict|None = None,
                 api_keys: dict|None = None,
                 
                 ):
        # Database
        if database_config:
            pass
        else:
            self._db_name = config("DB_NAME", raiseConfigError("To configure"))
        
        
        
        if database_config:
            if not database_config.get("DB_NAME", None) or not database_config.get("CONNECTION_STRING", None):
                raise DatabaseConfigError("'DB_NAME' and 'CONNECTION_STRING' dict keys are required!")
        
        # API
        if api_keys:
            self._keys: dict = api_keys
        else:
            self._keys:dict = _get_keys_from_env() #type: ignore[no-redef]
            
        self._apis = list(self._keys)
        
        # DB
        # self._db_name = database_config.get("name", None)            
        # match self._db_name: #Option for the creation steps to be different for each database type in the feature
        #     case "SQLite":
        #         self._engine = create_engine(database_config.get("connection_string", None))
        #     case "PostgreSQL":
        #         self._engine = create_engine(database_config.get("connection_string", None))
        #     case "MySQL":
        #         self._engine = create_engine(database_config.get("connection_string", None))
                


# config_item = {"x": "test", "y": "7"}

# c = Config(config_item)
# print(c._apis)

_get_database_config_from_env()
import dataclasses


@dataclasses.dataclass
class Config:
    debug: bool
    database_url: str

    @staticmethod
    def from_dotenv(verbose: bool = False) -> "Config":
        import dotenv

        env = dotenv.dotenv_values(".env", verbose=verbose)
        database_url = env["DATABASE_URL"]
        debug = _dotenv_bool(env, "DEBUG")
        config = Config(debug=debug, database_url=database_url)
        return config


def _dotenv_bool(source: dict[str, str], key: str, default: bool = False) -> bool:
    value = source.get(key, str(default)).lower()
    return value == "true"

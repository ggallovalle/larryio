import dataclasses


@dataclasses.dataclass
class Config:
    debug: bool
    postgres_url: str

    @staticmethod
    def from_dotenv(source: str|dict = ".env", verbose: bool = False) -> "Config":
        import dotenv
        if isinstance(source, str):
            env = dotenv.dotenv_values(source, verbose=verbose)
        else:
            env = source

        database_url = env["POSTGRES_URL"]
        debug = _dotenv_bool(env, "DEBUG")
        config = Config(debug=debug, postgres_url=database_url)
        return config


def _dotenv_bool(source: dict[str, str], key: str, default: bool = False) -> bool:
    value = source.get(key, str(default)).lower()
    return value == "true"

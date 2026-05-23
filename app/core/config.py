from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	"""Application settings."""

	app_name: str = "Mundo Invest API"
	debug: bool = False
	database_url: str = "sqlite:///./test.db"

	pipefy_token: str = ""
	pipefy_api_url: str = "https://api.pipefy.com/graphql"
	pipefy_pipe_id: str = ""

	model_config = SettingsConfigDict(
		env_file=".env",
		env_file_encoding="utf-8",
	)


settings = Settings()

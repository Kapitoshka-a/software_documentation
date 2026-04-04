class EntityNotFoundError(ValueError):
    def __init__(self, entity: str, entity_id: str) -> None:
        super().__init__(f"{entity} with id {entity_id} was not found")


class EntityAlreadyExistsError(ValueError):
    def __init__(self, entity: str, details: str) -> None:
        super().__init__(f"{entity} already exists: {details}")


class UserEmailAlreadyExistsError(EntityAlreadyExistsError):
    def __init__(self, email: str) -> None:
        super().__init__("User", f"email={email}")

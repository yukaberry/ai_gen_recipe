from pydantic import BaseModel, model_validator, ValidationError

class UserContact(BaseModel):
    email: str | None = None
    phone: str | None = None

    @model_validator(mode='after')
    def at_least_one_contact(cls, model):
        # `model` is an instance of UserContact
        if not model.email and not model.phone:
            raise ValueError('At least one contact detail (email or phone) must be provided')
        return model

# Example usages

# This works
user1 = UserContact(email='test@example.com')
print(user1)

# This also works
user2 = UserContact(phone='123-456-7890')
print(user2)

# This will raise a validation error
try:
    user3 = UserContact()
except ValidationError as e:
    print(e)

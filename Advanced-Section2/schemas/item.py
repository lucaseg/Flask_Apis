from ma import ma
from models.item import ItemModel

class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
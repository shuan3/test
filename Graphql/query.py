from graphene import Field, Int, List, Schema, ObjectType, String, Mutation


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


### Change or modify data opbject
class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    def mutate(self, info, name, age):
        user = {"id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user=user)


class Query(ObjectType):
    user = Field(UserType, user_Id=Int())
    users = [
        {"id": 1, "name": "User1", "age": 21},
        {"id": 3, "name": "User1", "age": 22666},
        {"id": 2, "name": "User1", "age": 25},
    ]

    users_min_age = List(UserType, min_age=Int())

    @staticmethod
    def resolve_user(self, info, user_Id):
        matched_user = [user for user in Query.users if user["id"] == user_Id]
        return matched_user[0] if matched_user else None

    @staticmethod
    def resolve_users_min_age(self, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]


class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    def mutate(self, info, user_id, name, age):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break
        # user=[user for user in Query.users if user['id']==user_id]
        if not user:
            return None
        if name is not None:
            user["name"] = name
        if age is not None:
            user["age"] = age

        return UpdateUser(user=user)


class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)

    user = Field(UserType)

    def mutate(self, info, user_id):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break
        if not user:
            return None
        Query.users = [u for u in Query.users if u["id"] != user_id]
        return DeleteUser(user=user)


class Mutation(ObjectType):
    # any change and update class need to be add in mutation
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


gql_search = """
query {
   user(userId:4){
        id
        name
        age
        }
}"""

gql_search_1 = """
query {
   user(userId:4){
        id
        name
        age
        }
}"""

## Function receiver in class query need to be remove _ and the second word is upper case
# gql='''
# query {
#    usersMinAge(minAge:1){
#         id
#         name
#         age
#         }
# }'''
gql_update = """
query {
   updateUser(userId:1,name:"New User",age:33){
        id
        name
        age
        }
}"""


gql = """
mutation {
   createUser(name: "New User",age:25){
        user { id
                name
                age }
        }
}"""
gql_delete = """
query {
   updateUser(userId:1){
        id
        name
        age
        }
}"""


gql_search_delete = """query {
   user(userId:1){
        id
        name
        age
        }
}"""

schema = Schema(query=Query, mutation=Mutation)


if __name__ == "__main__":
    result = schema.execute(gql)
    print(result)
    result = schema.execute(gql_search)
    print(result)
    result = schema.execute(gql_update)
    print(result)
    result = schema.execute(gql_search_1)
    print(result)
    result = schema.execute(gql_delete)
    print(result)
    result = schema.execute(gql_search_delete)
    print(result)
# print(result.data['hello'])


### Example 1
# class Query(ObjectType):
#     hello=String(name=String(default_value='stranger'))
#     def resolve_hello(self,info,name):
#         return 'Hello '+ {name}


# schema=Schema(query=Query)
# gql='''{
# hello(name: "graphql")
# }'''
# if __name__ == "__main__":
#         result=schema.execute(gql)
#         print(result)

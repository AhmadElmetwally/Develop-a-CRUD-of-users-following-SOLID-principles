from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

   

class User:
    def __init__(self, email, password, name):
        self.id = str(uuid.uuid4())
        self.email = email
        self.password = password
        self.name = name


class UserRepository:
    def __init__(self):
        self.users = {}

    def create_user(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def get_user(self, user_id: str) -> User:
        return self.users.get(user_id)

    def update_user(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def delete_user(self, user_id: str) -> None:
        if user_id in self.users:
            del self.users[user_id]


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data):
        user = User(user_data['email'], user_data['password'], user_data['name'])
        created_user = self.repository.create_user(user)
        return created_user

    def get_user(self, user_id):
        user = self.repository.get_user(user_id)
        return user

    def update_user(self, user_id, user_data):
        user = self.repository.get_user(user_id)
        if user:
            user.email = user_data.get('email', user.email)
            user.password = user_data.get('password', user.password)
            user.name = user_data.get('name', user.name)
            updated_user = self.repository.update_user(user)
            return updated_user
        return None

    def delete_user(self, user_id):
        self.repository.delete_user(user_id)


repository = UserRepository()
service = UserService(repository)


@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.get_json()
    created_user = service.create_user(user_data)
    return jsonify(created_user.__dict__)


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = service.get_user(user_id)
    if user:
        return jsonify(user.__dict__)
    else:
        return 'User not found', 404


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    updated_user = service.update_user(user_id, user_data)
    if updated_user:
        return jsonify(updated_user.__dict__)
    else:
        return 'User not found', 404


@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    service.delete_user(user_id)
    return '', 204


if __name__ == '__main__':
    app.run()
    
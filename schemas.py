from marshmallow import Schema, fields 


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    credentials = fields.Nested('UserCredentialsSchema', exclude=('user',), dump_only=True)
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('user',), dump_only=True)
    user_games = fields.Nested('UserGameSchema', many=True, exclude=('user',), dump_only=True)

class DeveloperSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    games = fields.Nested('GameSchema', many=True, exclude=('developer',), dump_only=True)

class EditorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    games = fields.Nested('GameSchema', many=True, exclude=('editor',), dump_only=True)

class GameSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    release_date = fields.Date(required=True)
    thumbnail = fields.Str(required=True)
    description = fields.Str(required=True)
    is_free = fields.Bool(load_default=True)
    created_at = fields.DateTime(dump_only=True)
    uploaded_at = fields.DateTime(dump_only=True)
    developer_id = fields.Int(required=True)
    editor_id = fields.Int(required=True)
    is_published = fields.Bool(load_default=True)
    reviews = fields.Nested('ReviewSchema', many=True, exclude=('game',), dump_only=True)
    user_games = fields.Nested('UserGameSchema', many=True, exclude=('game',), dump_only=True)
    genres = fields.Nested('GameGenreSchema', many=True, exclude=('game',), dump_only=True)

class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    games = fields.Nested('GameGenreSchema', many=True, exclude=('genre',), dump_only=True)

class GameGenreSchema(Schema):
    game_id = fields.Int(required=True)
    genre_id = fields.Int(required=True)
    game = fields.Nested('GameSchema', exclude=('genres',), dump_only=True)
    genre = fields.Nested('GenreSchema', exclude=('games',), dump_only=True)

class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    game_id = fields.Int(required=True)
    rating = fields.Int(required=True)
    text_review = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user = fields.Nested('UserSchema', exclude=('reviews', 'credentials', 'user_games'), dump_only=True)
    game = fields.Nested('GameSchema', exclude=('reviews', 'user_games', 'genres'), dump_only=True)

class UserCredentialsSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    password_hash = fields.Str(required=True, load_only=True)
    role_id = fields.Int(required=True)
    user = fields.Nested('UserSchema', exclude=('credentials', 'reviews', 'user_games'), dump_only=True)
    role = fields.Nested('RoleSchema', exclude=('credentials',), dump_only=True)

class UserGameSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    game_id = fields.Int(required=True)
    claimed_at = fields.DateTime(dump_only=True)
    user = fields.Nested('UserSchema', exclude=('credentials', 'reviews', 'user_games'), dump_only=True)
    game = fields.Nested('GameSchema', exclude=('reviews', 'user_games', 'genres'), dump_only=True)

class RoleSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    credentials = fields.Nested('UserCredentialsSchema', many=True, exclude=('role',), dump_only=True)

class RegisterSchema(Schema):
    username = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    role_id = fields.Int(required=True)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
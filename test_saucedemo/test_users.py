
users = [
    {"username": "standard_user", "password": "secret_sauce"},
   #{"username": "locked_out_user", "password": "secret_sauce"},
    {"username": "problem_user", "password": "secret_sauce"},
    {"username": "performance_glitch_user", "password": "secret_sauce"},
    {"username": "error_user", "password": "secret_sauce"},
    {"username": "visual_user", "password": "secret_sauce"}
]
for user in users:
    assert len(user["username"]) > 0, "Username can't be empty!"
    assert len(user["password"]) >= 6, "Password too short!"
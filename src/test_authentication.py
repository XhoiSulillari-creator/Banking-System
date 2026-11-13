from authentication import AuthenticationService


auth = AuthenticationService()

auth.register("C005", "password123")

print(auth.authenticate("C005", "password123"))
print(auth.authenticate("C005", "wrongpassword"))
print(auth.authenticate("C999", "password123"))
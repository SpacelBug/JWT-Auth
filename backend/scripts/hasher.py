from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes="argon2",
    argon2__rounds=3,
    argon2__memory_cost=65536,
    argon2__parallelism=4,
    argon2__type="id",
    deprecated="auto",
)

hash = pwd_context.hash(input("password: "))

print(hash)

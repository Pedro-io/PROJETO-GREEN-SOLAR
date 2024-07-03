import bcrypt
import yaml

# Defina as senhas reais aqui
passwords = {
    "user1": "password123",
    "user2": "mypassword456"
}

# Gere os hashes das senhas
hashed_passwords = {username: bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    for username, password in passwords.items()}

# Crie o formato de credenciais para o YAML
credentials = {"usernames": {}}
for username, hashed in hashed_passwords.items():
    credentials["usernames"][username] = {
        "name": username.capitalize(),
        "password": hashed
    }

# Adicione informações de cookie e preauthorization
config = {
    "credentials": credentials,
    "cookie": {
        "name": "your_cookie_name",
        "key": "your_cookie_key",
        "expiry_days": 30
    },
    "preauthorized": {
        "emails": []
    }
}

# Salve as credenciais no arquivo YAML
with open("config.yaml", "w") as file:
    yaml.dump(config, file)

print("Configurações salvas em config.yaml")

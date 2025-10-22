import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from adapters.repositories.file_user_repository import FileUserRepository
from use_cases.create_user_use_case import CreateUserUseCase
from use_cases.list_users_use_case import ListUsersUseCase

def main():
    # Creamos un repositorio real
    repository = FileUserRepository('users.json')

    # Creamos el caso de uso con el repositorio real
    create_user = CreateUserUseCase(repository)

    # Crear un nuevo usuario
    try:
        user = create_user.execute('Agustín', 'Estévez Domínguez', '76826889N')
        print(f"Usuario creado: {user}")
    except Exception as e:
        print(f"Error al crear usuario: {e}")

    # Listar usuarios
    list_users = ListUsersUseCase(repository)
    try:
        users = list_users.execute()
        print("Usuarios registrados:")
        for user in users:
            print(f" - {user._username} {user._lastname} ({user._dni})")
    except Exception as e:
        print(f"Error al listar usuarios: {e}")

if __name__ == '__main__':
    main()
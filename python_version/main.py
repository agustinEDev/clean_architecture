import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from adapters.repositories.file_user_repository import FileUserRepository
from use_cases.create_user_use_case import CreateUserUseCase
from use_cases.list_users_use_case import ListUsersUseCase
from use_cases.update_user_use_case import UpdateUserUseCase
from use_cases.delete_user_use_case import DeleteUserUseCase
from use_cases.find_user_use_case import FindUserUseCase

def main():
    # Creamos un repositorio real
    repository = FileUserRepository('users.json')
    # Creamos el caso de uso con el repositorio real
    create_user = CreateUserUseCase(repository)

    # Creamos una lista de usuarios para crear con dnis válidos
    users_to_create = [
        ('Agustín', 'Estévez Domínguez', '76826889N'),
        ('María', 'López Fernández', '12345678Z'),
        ('Juan', 'Pérez Gómez', '87654321X')
    ]

    # Crear un nuevo usuario
    try:
        for user_data in users_to_create:
            user = create_user.execute(*user_data)
            print(f"Usuario creado: {user}")
    except Exception as e:
        print(f"Error al crear usuario: {e}")

    # Buscar usuario
    find_user = FindUserUseCase(repository)
    try:
        user = find_user.execute('76826889N')
        print(f"Usuario encontrado: {user}")
    except Exception as e:
        print(f"Error al encontrar usuario: {e}")

    # Listar usuarios
    list_users = ListUsersUseCase(repository)
    try:
        users = list_users.execute()
        print("Usuarios registrados:")
        for user in users:
            print(f" - {user._username} {user._lastname} ({user._dni})")
    except Exception as e:
        print(f"Error al listar usuarios: {e}")

    # Actualizar usuario
    update_user = UpdateUserUseCase(repository)
    try:
        user = update_user.execute('76826889N', 'Agustin', 'Estevez D.')
        print(f"Usuario actualizado: {user}")
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")

    # Eliminar usuario
    delete_user = DeleteUserUseCase(repository)
    try:
        delete_user.execute('76826889N')
        print("Usuario eliminado.")
    except Exception as e:
        print(f"Error al eliminar usuario: {e}")

if __name__ == '__main__':
    main()
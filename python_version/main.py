import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from adapters.repositories.file_user_repository import FileUserRepository
from use_cases.create_user_use_case import CreateUserUseCase

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

if __name__ == '__main__':
    main()
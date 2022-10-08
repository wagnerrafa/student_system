import json

from apps.abstract.tests import AbstractTest


class StudentTest(AbstractTest):
    """Student related tests"""
    __student_id = None
    __student = {
        'name': 'temporary',
        'email': 'temporary@temporary.com',
        'birthday': '2022-10-07'
    }

    def setUp(self):
        """Assert get users detail"""
        super(StudentTest, self).setUp()
        response = self.client.post('/api/v1/alunos/', self.get_student())
        self.assertEqual(response.status_code, 201)
        self.__student_id = json.loads(response.content)['aluno']['id']

    def test_api_get_students(self):
        """Assert get users detail"""
        self.printl('Lista de estudantes')
        response = self.client.get('/api/v1/alunos/')
        self.assertEqual(response.status_code, 200)

    def test_api_create_student(self):
        """Assert get users detail"""
        self.printl('Criar estudante')
        student = {
            'name': 'temporary1',
            'email': 'temporary1@temporary.com',
            'birthday': '2022-10-07'
        }
        response = self.client.post('/api/v1/alunos/', student)
        self.assertEqual(response.status_code, 201)

    def test_api_filter_student(self):
        """Assert get student detail"""
        email = 'temporary@temporary.com'
        self.printl('Filtrar estudante')
        response = self.client.get(f'/api/v1/alunos/?email={email}')
        self.assertEqual(response.status_code, 200)
        students = json.loads(response.content)['alunos']
        self.assertEqual(1, len(students))

    def test_api_put_student_error(self):
        """Assert put student detail error in field validation"""
        self.printl('Inválido update estudante')
        response = self.client.put(self.get_url_detail(), self.get_student(), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_api_put_student_success(self):
        """Assert put student detail success, altering email and birthday"""
        self.printl('Válido update estudante')
        self.set_student('birthday', '2022-10-07')
        user = self.set_student('email', 'temporary2@temporary.com')
        response = self.client.put(self.get_url_detail(), user, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_api_delete_user(self):
        """Assert Delete User"""
        self.printl('Remover estudante')
        response = self.client.delete(self.get_url_detail())
        self.assertEqual(response.status_code, 200)

    def get_url_detail(self):
        return f'/api/v1/alunos/{self.__student_id}/'

    def get_student(self):
        """Get Student"""
        return self.__student

    def set_student(self, field, value):
        """Update field in Student, return Student"""
        self.__student[field] = value
        return self.__student

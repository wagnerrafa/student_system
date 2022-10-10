import json
from apps.abstract.tests import AbstractTest


class StudentTest(AbstractTest):
    """Student related tests"""

    def test_api_get_students(self):
        """Assert get students detail"""
        self.printl('Lista de estudantes')
        response = self.client.get('/api/v1/aluno/')
        self.assertEqual(response.status_code, 200)

    def test_api_create_student(self):
        """Assert create student"""
        self.printl('Criar estudante')
        student = {
            'name': 'temporary1',
            'email': 'temporary1@temporary.com',
            'birthday': '2022-10-07'
        }
        response = self.client.post('/api/v1/aluno/', student)
        self.assertEqual(response.status_code, 201)

    def test_api_filter_student(self):
        """Assert get students detail"""
        email = 'temporary@temporary.com'
        self.printl('Filtrar estudante')
        response = self.client.get(f'/api/v1/aluno/?email={email}')
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

    def test_api_delete_student(self):
        """Assert Delete Student"""
        self.printl('Remover estudante')
        response = self.client.delete(self.get_url_detail())
        self.assertEqual(response.status_code, 200)

    def get_url_detail(self):
        return f'/api/v1/aluno/{self.get_student_id()}/'

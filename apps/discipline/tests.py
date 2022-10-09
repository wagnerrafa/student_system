import json
from apps.abstract.tests import AbstractTest


class DisciplineTest(AbstractTest):
    """Discipline related tests"""
    __discipline_id = None
    __discipline = {
        'name': 'temporary discipline',
        'workload': '20',
    }

    def setUp(self):
        """Assert get users detail"""
        super(DisciplineTest, self).setUp()
        response = self.client.post('/api/v1/disciplina/', self.get_discipline())
        self.assertEqual(response.status_code, 201)
        self.__discipline_id = json.loads(response.content)['disciplina']['id']

    def test_api_get_disciplines(self):
        """Assert get users detail"""
        self.printl('Lista de disciplinas')
        response = self.client.get('/api/v1/disciplina/')
        self.assertEqual(response.status_code, 200)

    def test_api_create_discipline(self):
        """Assert get users detail"""
        self.printl('Criar disciplina')
        discipline = {
            'name': 'temporary discipline 1',
            'workload': '20',
        }
        response = self.client.post('/api/v1/disciplina/', discipline)
        self.assertEqual(response.status_code, 201)

    def test_api_filter_discipline(self):
        """Assert get discipline detail"""
        name = 'temporary discipline'
        self.printl('Filtrar disciplina')
        response = self.client.get(f'/api/v1/disciplina/?name={name}')
        self.assertEqual(response.status_code, 200)
        disciplines = json.loads(response.content)['disciplinas']
        self.assertEqual(1, len(disciplines))

    def test_api_put_discipline_error(self):
        """Assert put discipline detail error in field validation"""
        self.printl('Inválido update disciplina')
        response = self.client.put(self.get_url_detail(), self.get_discipline(), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_api_put_discipline_success(self):
        """Assert put discipline detail success, altering email and birthday"""
        self.printl('Válido update disciplina')
        user = self.set_discipline('name', 'temporary discipline 2')
        response = self.client.put(self.get_url_detail(), user, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_api_delete_user(self):
        """Assert Delete User"""
        self.printl('Remover disciplina')
        response = self.client.delete(self.get_url_detail())
        self.assertEqual(response.status_code, 200)

    def get_url_detail(self):
        return f'/api/v1/disciplina/{self.__discipline_id}/'

    def get_discipline(self):
        """Get Discipline"""
        return self.__discipline

    def set_discipline(self, field, value):
        """Update field in Discipline, return Discipline"""
        self.__discipline[field] = value
        return self.__discipline

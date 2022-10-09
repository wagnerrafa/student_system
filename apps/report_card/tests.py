import json
from apps.abstract.tests import AbstractTest


class ReportCardTest(AbstractTest):
    """ReportCard related tests"""
    __report_card_id = None
    __report_card = {
        'grade': '5',
        'delivery_date': '2001-12-31',
    }

    def setUp(self):
        """Assert get report_cards detail"""
        super(ReportCardTest, self).setUp()
        self.set_report_card('discipline_id', self.get_discipline_id())
        self.set_report_card('student_id', self.get_student_id())
        response = self.client.post('/api/v1/boletim/', self.get_report_card())
        self.assertEqual(response.status_code, 201)
        self.__report_card_id = json.loads(response.content)['boletim']['id']

    def test_api_get_report_cards(self):
        """Assert get report_cards detail"""
        self.printl('Lista de boletins')
        response = self.client.get('/api/v1/boletim/')
        self.assertEqual(response.status_code, 200)

    def test_api_create_report_card(self):
        """Assert create report_card"""
        self.printl('Criar boletim')
        report_card = {
            'grade': '6',
            'delivery_date': '2001-12-31',
            'discipline_id': self.get_discipline_id(),
            'student_id': self.get_student_id(),
        }
        response = self.client.post('/api/v1/boletim/', report_card)
        self.assertEqual(response.status_code, 201)

    def test_api_filter_report_card(self):
        """Assert get report_card detail"""
        gradle = '5'
        self.printl('Filtrar boletim')
        response = self.client.get(f'/api/v1/boletim/?grade={gradle}')
        self.assertEqual(response.status_code, 200)
        report_cards = json.loads(response.content)['boletins']
        self.assertEqual(1, len(report_cards))

    def test_api_put_report_card_error(self):
        """Assert put report_card detail error in field validation delivery_date"""
        self.printl('Inválido update boletim')
        report_card = self.get_report_card().copy()
        report_card['delivery_date'] = '01-01-2020'
        response = self.client.put(self.get_url_detail(), report_card, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_api_put_report_card_success(self):
        """Assert put report_card detail success, altering gradle"""
        self.printl('Válido update boletim')
        report_card = self.set_report_card('gradle', '7')
        response = self.client.put(self.get_url_detail(), report_card, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_api_delete_user(self):
        """Assert Delete ReportCard"""
        self.printl('Remover boletim')
        response = self.client.delete(self.get_url_detail())
        self.assertEqual(response.status_code, 200)

    def get_url_detail(self):
        return f'/api/v1/boletim/{self.__report_card_id}/'

    def get_report_card(self):
        """Get ReportCard"""
        return self.__report_card

    def set_report_card(self, field, value):
        """Update field in ReportCard, return ReportCard"""
        self.__report_card[field] = value
        return self.__report_card

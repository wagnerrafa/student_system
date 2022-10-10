import datetime
import os
import platform
import random
import sqlite3
import time
import uuid
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker
from faker.providers import DynamicProvider

fake = Faker()
disciplines_provider = DynamicProvider(
    provider_name="discipline",
    elements=["português", 'inglês', 'geografia', 'matematica', 'historia', 'filosofia', 'educação física'],
)

fake.add_provider(disciplines_provider)


class DBOperations:
    __cursor = None
    __conn = None
    __db_name_student = 'student_student'
    __db_name_discipline = 'discipline_discipline'
    __db_name_report_card = 'report_card_reportcard'
    __default_uuid = '00000000-0000-0000-0000-000000000000'
    __user_id = None
    __base_insert = """INSERT INTO {} {} VALUES {}"""
    __base_select_all = """SELECT {} FROM {}"""
    __base_select_where = """SELECT {} FROM {} WHERE {}"""
    __discipline_id = None
    __student_id = None
    __report_card_id = None

    def __init__(self):
        self.__join_report_card = f""" INNER JOIN {self.__db_name_student} on {self.__db_name_report_card}.student_id 
                  = {self.__db_name_student}.id INNER JOIN {self.__db_name_discipline} on {self.__db_name_discipline}.id 
                  = {self.__db_name_report_card}.discipline_id"""

    @staticmethod
    def __get_uuid():
        """Get uuid"""
        return str(uuid.uuid4()).replace('-', '')

    def __create_user(self):
        """Create User"""
        username = fake.user_name()
        user = User.objects.create_user(**{
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'username': username,
            'email': fake.email(),
        })

        password = fake.password()
        user.set_password(password)
        user.save()
        self.__user_id = str(user.id)
        print(f'Username: {username}')
        print(f'Password: {password}')

    def __create_connection(self):
        """Connect in db"""
        self.__conn = sqlite3.connect('db.sqlite3')
        self.__cursor = self.__conn.cursor()

    @staticmethod
    def __now():
        """Get current datetime"""
        return str(datetime.datetime.today())

    def __create_student(self):
        """Insert student detail"""
        name = fake.name()
        print(f'Student name: {name}')
        email = fake.email()
        birthday = fake.date()
        sql = self.__base_insert.format(self.__db_name_student, ('id', 'created_at', 'updated_at', 'create_user',
                                                                 'update_user', 'name', 'birthday', 'email'),
                                        (self.__student_id, self.__now(), self.__now(), self.__default_uuid,
                                         self.__default_uuid, name, birthday, email))

        self.__cursor.execute(sql)
        self.__conn.commit()

    def __create_discipline(self):
        """Insert discipline detail"""
        name = fake.discipline()
        workload = random.randint(1, 200)
        print(f'Discipline name: {name}')
        print(f'Discipline workload: {workload}')
        sql = self.__base_insert.format(self.__db_name_discipline, ('id', 'created_at', 'updated_at', 'create_user',
                                                                    'update_user', 'name', 'workload'),
                                        (self.__discipline_id, self.__now(), self.__now(), self.__default_uuid,
                                         self.__default_uuid, name, workload))

        self.__cursor.execute(sql)
        self.__conn.commit()

    def __create_report_card(self):
        """Insert report_card detail"""
        grade = random.randint(1, 10)
        delivery_date = fake.date()
        print(f'Reportcard grade: {grade}')
        print(f'Reportcard delivery_date: {delivery_date}')
        sql = self.__base_insert.format(self.__db_name_report_card, ('id', 'created_at', 'updated_at', 'create_user',
                                                                     'update_user', 'grade', 'delivery_date',
                                                                     'discipline_id', 'student_id'),
                                        (self.__report_card_id, self.__now(), self.__now(), self.__default_uuid,
                                         self.__default_uuid, grade, delivery_date, self.__discipline_id,
                                         self.__student_id))

        self.__cursor.execute(sql)
        self.__conn.commit()

    def __get_all_by_db(self, db):
        """Abstract select all"""
        self.__create_connection()
        sql = self.__base_select_all.format('*', f'"{db}"')
        data = self.__cursor.execute(sql)
        rows = data.fetchall()
        self.close_connection()
        return rows

    def __get_by_sql(self, sql):
        """Abstract select sql, managing the connection"""
        self.__create_connection()
        data = self.__cursor.execute(sql)
        rows = data.fetchall()
        self.close_connection()
        return rows

    def __get_media_by_operation(self, operation):
        """Calculate media and select by operation"""
        sql = f"SELECT * FROM {self.__db_name_report_card}" + self.__join_report_card + \
              f' WHERE {self.__db_name_report_card}.grade {operation} (SELECT AVG(grade) ' \
              f'FROM {self.__db_name_report_card})'
        self.__create_connection()
        data = self.__cursor.execute(sql)
        rows = data.fetchall()
        self.close_connection()
        return rows

    def create_values(self):
        """Insert values in tables"""
        self.__discipline_id = self.__get_uuid()
        self.__student_id = self.__get_uuid()
        self.__report_card_id = self.__get_uuid()
        self.__create_connection()
        self.__create_user()
        self.__create_student()
        self.__create_discipline()
        self.__create_report_card()
        self.close_connection()

    def get_students(self):
        """Select all students"""
        rows = self.__get_all_by_db(self.__db_name_student)
        for row in rows:
            print(row, 'student')
        return rows

    def get_disciplines(self):
        """Select all disciplines"""
        rows = self.__get_all_by_db(self.__db_name_discipline)
        for row in rows:
            print(row, 'discipline')
        return rows

    def get_report_cards(self):
        """Select all report card"""
        sql = self.__base_select_all.format('*', f'"{self.__db_name_report_card}"') + self.__join_report_card
        rows = self.__get_by_sql(sql)
        for row in rows:
            print(row, 'report card')
        return rows

    def get_report_cards_above_average(self):
        """Select student where above average"""
        rows = self.__get_media_by_operation('>=')
        for row in rows:
            print(row, 'approved student')
        return rows

    def get_report_cards_below_average(self):
        """Select student where below average"""
        rows = self.__get_media_by_operation('<')
        for row in rows:
            print(row, 'reproved student')
        return rows

    def get_report_cards_approved(self):
        """Select student approved"""
        sql = self.__base_select_where.format('*', self.__db_name_report_card, f'grade >= 5')
        rows = self.__get_by_sql(sql)
        for row in rows:
            print(row, 'approved student')
        return rows

    def get_report_cards_reproved(self):
        """Select student reproved"""
        sql = self.__base_select_where.format('*', self.__db_name_report_card, f'grade < 5')
        rows = self.__get_by_sql(sql)
        for row in rows:
            print(row, 'approved student')
        return rows

    def close_connection(self):
        if self.__cursor is not None:
            self.__cursor.close()


class Command(BaseCommand):
    help = 'run crontab events'

    def printl(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    @staticmethod
    def __prepare_django():
        try:
            if os.path.exists('db.sqlite3') is False:
                if os.path.exists('venv') is False:
                    os.system('python -m venv venv')
                if platform.system().lower() == 'linux':
                    os.system('source venv/bin/activate')
                else:
                    os.system('.\\venv\\Scripts\\activate')
                os.system('pip install -r requirements.txt')
                os.system('python manage.py makemigrations')
                os.system('python manage.py migrate')
        except Exception as e:
            print(e, 'Erro ao validar o servidor\n')
            print('Siga o Readme para criar o ambiente e seu banco de dados antes de criar o fake_database novamente')

    def handle(self, *args, **options):
        self.__prepare_django()

        db_operations = DBOperations()
        operations = {
            '1': [db_operations.create_values, 'Criar todos os registros no banco'],
            '2': [db_operations.get_students, 'Exibir todos os alunos'],
            '3': [db_operations.get_disciplines, 'Exibir todas as disciplinas'],
            '4': [db_operations.get_report_cards, 'Exibir todos os boletins'],
            '5': [db_operations.get_report_cards_above_average, 'Exibir todos os boletins acima da media'],
            '6': [db_operations.get_report_cards_below_average, 'Exibir todos os boletins abaixo da media'],
            '7': [db_operations.get_report_cards_approved, 'Exibir todos os boletins aprovados'],
            '8': [db_operations.get_report_cards_reproved, 'Exibir todos os boletins reprovados'],
            '9': [db_operations.close_connection, 'Sair'],
        }

        while True:
            for key, values in operations.items():
                print(f'{key}: {values[1]}')
            option_selected = input(f'\nInsira uma opção de 1 a {len(operations)}\n')
            if option_selected == '9':
                print('Até logo')
                break

            selected_option = operations.get(option_selected)
            if not selected_option:
                print('Insira uma opção válida')
                time.sleep(4)
            selected_option[0]()
            time.sleep(5)

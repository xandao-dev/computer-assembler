# region Imports
from pathlib import Path

from whaaaaat import Separator, prompt
from whaaaaat import style_from_dict, Token
from transitions import Machine, State
# endregion

menu_style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#FF9D00 bold',
    Token.Selected: '#5F819D',
    Token.Pointer: '#FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})

states = [
    State(name='start'),
    State(name='create_user_data_folder', on_enter='create_user_data_folder'),
    State(name='get_user_data_filenames', on_enter='get_user_data_filenames'),
    State(name='prepare_questions', on_enter='prepare_questions'),
    State(name='get_answer_menu', on_enter='get_answer_menu'),
    State(name='verify_answers', on_enter='verify_answers')
]

transitions = [
    {"trigger": 'start', 'source': '*', 'dest': 'start'},
    { 'trigger': 'create_user_data_folder', 'source': 'start', 'dest': 'create_user_data_folder'},
    { 'trigger': 'get_user_data_filenames', 'source': 'create_user_data_folder', 'dest': 'get_user_data_filenames'},
    { 'trigger': 'prepare_questions', 'source': 'get_user_data_filenames', 'dest': 'prepare_questions'},
    { 'trigger': 'get_answer_menu', 'source': 'prepare_questions', 'dest': 'get_answer_menu'},
    { 'trigger': 'verify_answers', 'source': 'get_answer_menu', 'dest': 'verify_answers'},
]


class Menu(object):

    def __init__(self):
        self.data_filenames = None  # type : list
        self.questions_menu = None  # type : list
        self.question_overwrite = None  # type : list
        self.answers_menu = None  # type : dict
        self.username = None  # type : str
        self.save_session = False  # type : bool
        self.user_options = {
            'restore': 'Restore a session',
            'save': 'Create a new session',
            'continue': 'Continue without saving',
            'delete': 'Delete a session',
            'exit': 'Exit'
        }    # type : dict

    def reset_fields(self):
        self.data_filenames = None  # type : list
        self.questions_menu = None  # type : list
        self.question_overwrite = None  # type : list
        self.answers_menu = None  # type : dict
        self.username = None  # type : str
        self.save_session = False  # type : bool

    def prepare_questions(self):
        self.questions_menu = [
            {
                'type': 'rawlist',
                'name': 'user_options',
                'message': '***Session Manager***:',
                'choices': [
                    Separator(),
                    self.user_options['restore'],
                    self.user_options['save'],
                    self.user_options['continue'],
                    Separator(),
                    self.user_options['delete'],
                    self.user_options['exit'],
                    Separator()
                ]
            },
            {
                'type': 'rawlist',
                'name': 'restore',
                'message': 'Select a session to try to restore:',
                'choices': [*[session for session in self.data_filenames], '<---Go-back---'],
                'when': lambda answers: answers['user_options'] == self.user_options['restore']
            },
            {
                'type': 'input',
                'name': 'save',
                'message': 'Write your first name or username to save:',
                'when': lambda answers: answers['user_options'] == self.user_options['save']
            },
            {
                'type': 'checkbox',
                'name': 'delete',
                'message': 'Mark the sessions you want to delete:',
                'choices': list(map(lambda e: {'name': e}, self.data_filenames)),
                'when': lambda answers: answers['user_options'] == self.user_options['delete']
            }
        ]

        self.question_overwrite = [
            {
                'type': 'confirm',
                'name': 'overwrite_data',
                'message': 'There is already a session with that name, overwrite it?',
                'default': True
            }
        ]
    
    def get_answer_menu(self):
        self.answers_menu = prompt(self.questions_menu, style=menu_style)  

    def verify_answers(self):

        # Handle when person choose 'Restore a session'
        if self.answers_menu['user_options'] == self.user_options['restore']:
            if self.answers_menu['restore'] == '<---Go-back---':
                return False
            else:
                self.username = self.answers_menu['restore']
                self.save_session = True
                return True

        # Handle when person choose 'Create a new session'
        elif self.answers_menu['user_options'] == self.user_options['save']:
            self.username = self.answers_menu['save']
            self.save_session = True
            return self.__verify_if_session_file_exists()
            

        # Handle when person choose 'Continue without saving'
        elif self.answers_menu['user_options'] == self.user_options['continue']:
            self.username, self.save_session = None, False
            return True

        # Handle when person choose 'Delete a session'
        elif self.answers_menu['user_options'] == self.user_options['delete']:
            if len(self.answers_menu['delete']) > 0:
                [self.__delete_session_data(user_data_folder_path / username) for username in self.answers_menu['delete']]
            return False

        # Handle when person choose 'Exit'
        elif self.answers_menu['user_options'] == self.user_options['exit']:
            exit()

    def run(self):
        done = False
        while(not done):
            if(self.questions_menu != None): self.reset_fields()
            machine = Machine(self, states, transitions=transitions, initial='start')
            self.create_user_data_folder()
            self.get_user_data_filenames()
            self.prepare_questions()
            self.get_answer_menu()
            done = self.verify_answers()

import pytest
import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://localhost:5001'


@pytest.fixture(scope="class")
def setup_session():
    session = requests.Session()
    yield session
    session.close()


def extract_cell_state(html_content, cell_position):
    """Parse the HTML to extract the state of a specific cell."""
    soup = BeautifulSoup(html_content, 'html.parser')
    cells = soup.find_all('td')
    if cells and len(cells) > cell_position:
        return cells[cell_position].text.strip()
    return None


class TestTicTacToe:

    @pytest.fixture(autouse=True)
    def set_session(self, setup_session):
        self.session = setup_session

    def test_cell_change(self):
        # Get the state of the first cell before any move
        response_before = self.session.get(f'{BASE_URL}/')
        cell_before = extract_cell_state(response_before.content, 0)
        self.session.post(f'{BASE_URL}/play/0')
        response_after = self.session.get(f'{BASE_URL}/')
        cell_after = extract_cell_state(response_after.content, 0)
        assert cell_before == '' and cell_after == 'X'

    def test_new_game(self):
        # Start a new game
        self.session.post(f'{BASE_URL}/new_game')
        response = self.session.get(f'{BASE_URL}/')
        board_state = [extract_cell_state(response.content, i) for i in range(9)]
        assert all(cell == '' for cell in board_state)

    def test_computer_play(self):
        # Make a move on the first cell
        self.session.post(f'{BASE_URL}/play/0')
        response = self.session.get(f'{BASE_URL}/')
        board_state = [extract_cell_state(response.content, i) for i in range(9)]
        assert board_state.count('X') == 1 and board_state.count('O') == 1

    def test_restart_game(self):
        response = self.session.post(f'{BASE_URL}/restart')
        assert 'Game restarted.' in response.text

    def test_win_condition(self):
        # Simulate a win condition for Player X in the last row
        self.session.post(f'{BASE_URL}/play/4')
        self.session.post(f'{BASE_URL}/play/1')
        self.session.post(f'{BASE_URL}/play/7')
        response = self.session.get(f'{BASE_URL}/')
        assert 'wins!' in response.text

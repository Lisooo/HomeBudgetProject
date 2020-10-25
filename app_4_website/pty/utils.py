from app_4_website.models import Party


class Pty:
    def __init__(self, p_pty_id):
        self.pty_id = p_pty_id

    def get_pty_data(self):
        v_data = Party.query
        v_data = v_data.filter(Party.pty_id == self.pty_id)
        v_data = v_data.order_by(Party.pty_id)
        v_data = v_data.first()

        return v_data

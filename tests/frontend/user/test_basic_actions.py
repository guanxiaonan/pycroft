from flask import url_for

from pycroft import config
from pycroft.model import session
from pycroft.model.user import User
from pycroft.model.facilities import Room
from tests.fixtures import permissions
from tests.fixtures.dummy import user as dummy_user_fixtures, facilities
from . import UserFrontendTestBase


class UserBlockingTestCase(UserFrontendTestBase):
    def setUp(self):
        super().setUp()
        username = permissions.UserData.user3_user.login
        self.test_user_id = User.q.filter_by(login=username).one().id

    def test_blocking_and_unblocking_works(self):
        user_show_endpoint = url_for("user.user_show", user_id=self.test_user_id)
        response = self.client.get(user_show_endpoint)
        self.assert200(response)

        response = self.client.post(url_for("user.suspend", user_id=self.test_user_id),
                                    data={'ends_at-unlimited': 'y',
                                          'reason': 'Ist doof'})
        self.assertRedirects(response, user_show_endpoint)
        self.assert_message_flashed("Nutzer gesperrt", 'success')

        response = self.client.post(url_for("user.unblock", user_id=self.test_user_id))
        self.assertRedirects(response, user_show_endpoint)
        self.assert_message_flashed("Nutzer entsperrt", 'success')

    def test_unblocked_user_cannot_be_unblocked(self):
        response = self.client.post(url_for("user.unblock", user_id=self.test_user_id))
        self.assert404(response)
        self.assert_message_substr_flashed("ist nicht gesperrt!", category='error')


class UserMovingOutTestCase(UserFrontendTestBase):
    def setUp(self):
        super().setUp()
        username = permissions.UserData.user3_user.login
        self.user = User.q.filter_by(login=username).one()

    def test_user_cannot_be_moved_back_in(self):
        # attempt to move the user back in
        endpoint = url_for('user.move_back_in', user_id=self.user.id)
        response = self.client.post(endpoint, data={
            # Will be serialized to str implicitly
            'building': self.user.room.building.id,
            'level': self.user.room.level,
            'room_number': self.user.room.number,
            'mac': "00:de:ad:be:ef:00",
        })
        self.assert_404(response)
        self.assert_message_flashed("Nutzer {} ist nicht ausgezogen!"
                                    .format(self.user.id), category='error')

    def test_user_moved_out_correctly(self):
        endpoint = url_for('user.move_out', user_id=self.user.id)
        response = self.client.post(endpoint)
        self.assert_redirects(response, url_for('user.user_show', user_id=self.user.id))
        self.assertMessageFlashed("Nutzer wurde ausgezogen", 'success')
        # TODO: Test whether everything has been done on the library side!


class UserMovedOutTestCase(UserFrontendTestBase):
    def setUp(self):
        super().setUp()
        # Taking the dummy user because the one from the `permission`
        # fixtures is member in `config.member_group`
        username = dummy_user_fixtures.UserData.dummy.login
        self.user = User.q.filter_by(login=username).one()

    def test_user_cannot_be_moved_out(self):
        endpoint = url_for('user.move_out', user_id=self.user.id)
        response = self.client.post(endpoint, data={'comment': "Ist doof"})
        self.assert_404(response)
        self.assert_message_flashed("Nutzer {} ist aktuell nirgends eingezogen!"
                                    .format(self.user.id), category='error')

    def test_user_can_be_moved_back_in(self):
        user_id = self.user.id
        endpoint = url_for('user.move_back_in', user_id=user_id)
        # Pick a room, any room
        room = Room.q.filter_by(inhabitable=True).limit(1).one()
        response = self.client.post(endpoint, data={
            # Will be serialized to str implicitly
            'building': room.building.id,
            'level': room.level,
            'room_number': room.number,
            'mac': "00:de:ad:be:ef:00",
        })
        self.assert_redirects(response, url_for('user.user_show', user_id=user_id))
        self.assert_message_flashed("Nutzer wurde wieder eingezogen", category='success')

# Copyright (c) 2014 The Pycroft Authors. See the AUTHORS file.
# This file is part of the Pycroft project and licensed under the terms of
# the Apache License, Version 2.0. See the LICENSE file for details.
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from pycroft.model.user import User
from tests import FixtureDataTestBase
from tests.lib.fixtures.finance_fixtures import FinanceAccountData, \
    JournalData, SemesterData, UserData
from pycroft.lib.finance import import_journal_csv, get_current_semester, \
    simple_transaction
from pycroft.model.finance import FinanceAccount, Journal, JournalEntry, \
    Transaction
from datetime import date, timedelta


class Test_010_Journal(FixtureDataTestBase):

    datasets = [FinanceAccountData, JournalData, SemesterData, UserData]

    def setUp(self):
        super(Test_010_Journal, self).setUp()
        self.asset_account = FinanceAccount.q.filter_by(
            name=FinanceAccountData.Asset.name
        ).one()
        self.liability_account = FinanceAccount.q.filter_by(
            name=FinanceAccountData.Liability.name
        ).one()
        self.expense_account = FinanceAccount.q.filter_by(
            name=FinanceAccountData.Expense.name
        ).one()
        self.revenue_account = FinanceAccount.q.filter_by(
            name=FinanceAccountData.Revenue.name
        ).one()
        self.journal = Journal.q.filter_by(
            account_number=JournalData.Journal1.account_number
        ).one()
        self.author = User.q.filter_by(
            login=UserData.Dummy.login
        ).one()

    def test_0010_import_journal_csv(self):
        """
        This test should verify that the csv import works as expected.
        """
        f = open("example/example.csv")
        import_journal_csv(f, date(2013, 1, 5))

        journal = (Journal.q
                   .filter(Journal.iban == JournalData.Journal1.iban)
                   .one())

        # test for correct dataimport
        entry = JournalEntry.q.filter(
            JournalEntry.journal == journal,
            JournalEntry.original_description == u"0000-3, SCH, AAA, ZW41D/01 99 1, SS 13").first()
        self.assertEquals(entry.other_account_number, "12345678")
        self.assertEquals(entry.other_routing_number, "80040400")
        self.assertEquals(entry.other_name, u"SCH, AAA")
        self.assertEquals(entry.amount, 900000)
        self.assertEquals(entry.transaction_date, date(2013, 1, 2))
        self.assertEquals(entry.valid_date, date(2013, 1, 2))

        # verify that the right year gets chosen for the transaction
        entry = JournalEntry.q.filter(
            JournalEntry.journal == journal,
            JournalEntry.original_description == u"Pauschalen").first()
        self.assertEquals(entry.transaction_date, date(2012, 12, 24))
        self.assertEquals(entry.valid_date, date(2012, 12, 24))

        # verify that a negative amount is imported correctly
        self.assertEquals(entry.amount, -600)

        # verify that the correct transaction year gets chosen for a valuta date
        # which is in the next year
        entry = JournalEntry.q.filter(
            JournalEntry.journal == journal,
            JournalEntry.original_description == u"BESTELLUNG SUPERMEGATOLLER SERVER").first()
        self.assertEquals(entry.transaction_date, date(2012, 12, 29))
        self.assertEquals(entry.valid_date, date(2013, 1, 10))

        JournalEntry.q.delete()

    def test_0020_get_current_semester(self):
        from pprint import pprint
        from pycroft.model.finance import Semester
        pprint(date.today())
        pprint(Semester.q.one().__dict__)
        try:
            get_current_semester()
        except NoResultFound:
            self.fail("No semester found")
        except MultipleResultsFound:
            self.fail("Multiple semesters found")

    def test_0030_simple_transaction(self):
        try:
            simple_transaction(
                u"transaction", self.asset_account, self.liability_account,
                9000, self.author
            )
        except Exception:
            self.fail()
        Transaction.q.delete()


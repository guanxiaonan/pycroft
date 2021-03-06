# coding=utf-8
# Copyright (c) 2016 The Pycroft Authors. See the AUTHORS file.
# This file is part of the Pycroft project and licensed under the terms of
# the Apache License, Version 2.0. See the LICENSE file for details.
from datetime import datetime, timedelta
from fixture import DataSet

today = datetime.utcnow().date()


class SemesterData(DataSet):
    class dummy_semester1:
        name = "first semester"
        registration_fee = 25.00
        regular_semester_fee = 15.00
        reduced_semester_fee = 4.50
        late_fee = 2.50
        grace_period = timedelta(62)
        reduced_semester_fee_threshold = timedelta(62)
        payment_deadline = timedelta(31)
        allowed_overdraft = 5.00
        begins_on = today
        ends_on = today + timedelta(days=180)


class AccountData(DataSet):
    class bank_account:
        name = u"Bankkonto 1020304050"
        type = "BANK_ASSET"

    class dummy_asset:
        name = u"An asset account"
        type = "ASSET"

    class dummy_liability:
        name = u"An liability account"
        type = "LIABILITY"

    class dummy_expense:
        name = u"An expense account"
        type = "EXPENSE"

    class dummy_revenue:
        name = u"A revenue account"
        type = "REVENUE"

    class dummy_user1:
        name = u'User account'
        type = 'USER_ASSET'

    class dummy_user2(dummy_user1):
        pass

    class dummy_user3(dummy_user1):
        pass

    class dummy_user4(dummy_user1):
        pass

    class dummy_user5(dummy_user1):
        pass


class BankAccountData(DataSet):
    class dummy:
        name = u"Beispielkonto"
        bank = u"Beispielbank"
        account_number = "1020304050"
        routing_number = "12345678"
        iban = "DE61123456781020304050"
        bic = "ABCDEFGH123"
        account = AccountData.bank_account

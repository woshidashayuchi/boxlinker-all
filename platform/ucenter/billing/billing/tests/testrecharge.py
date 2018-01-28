#!/usr/bin/env python

import sys
from time import sleep

sys.path.insert(1, '../..')

from billing.manager import recharges_manager


def testrecharge(team_uuid, recharge_amount,
                 recharge_type, recharge_user):

    recharge_manager = recharges_manager.RechargesManager()

    return recharge_manager.recharge_create(
                            team_uuid, recharge_amount,
                            recharge_type, recharge_user)

if __name__ == '__main__':

    team_uuid = 'fd53c54a-899a-43cf-9858-a31253a107ed'
    recharge_amount = 10
    recharge_type = 'zhifubao'
    recharge_user = 'yanhua'

    print testrecharge(team_uuid, recharge_amount, 
                       recharge_type, recharge_user)

# -*- coding: utf-8 -*-
# Author: YanHua <it-yanh@all-reach.com>

from common.logs import logging as log
from common.code import request_result
from common.acl import acl_check
from common.parameters import parameter_check
from common.token_localauth import token_auth

from billing.manager import levels_manager
from billing.manager import recharges_manager
from billing.manager import costs_manager
from billing.manager import limits_manager
from billing.manager import resources_manager
from billing.manager import vouchers_manager
from billing.manager import bills_manager
from billing.manager import balances_manager
from billing.manager import orders_manager


class BillingRpcManager(object):

    def __init__(self):

        self.levels_manager = levels_manager.LevelsManager()
        self.recharges_manager = recharges_manager.RechargesManager()
        self.costs_manager = costs_manager.CostsManager()
        self.limits_manager = limits_manager.LimitsManager()
        self.resources_manager = resources_manager.ResourcesManager()
        self.vouchers_manager = vouchers_manager.VouchersManager()
        self.bills_manager = bills_manager.BillsManager()
        self.balances_manager = balances_manager.BalancesManager()
        self.orders_manager = orders_manager.OrdersManager()

    @acl_check
    def cost_accounting(self, context, parameters):

        try:
            resource_type = parameters.get('resource_type')
            resource_conf = parameters.get('resource_conf')
            resource_status = parameters.get('resource_status')
            hours = parameters.get('hours')

            resource_type = parameter_check(resource_type, ptype='pstr')
            resource_conf = parameter_check(resource_conf, ptype='pstr')
            resource_status = parameter_check(resource_status, ptype='pstr')
            hours = parameter_check(hours, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.costs_manager.cost_accounting(
                    resource_type, resource_conf,
                    resource_status, hours)

    @acl_check
    def limit_check(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            resource_type = parameters.get('resource_type')
            cost = parameters.get('cost')

            resource_type = parameter_check(resource_type, ptype='pstr')
            cost = parameter_check(cost, ptype='pflt', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.limits_manager.limit_check(
                    team_uuid, project_uuid, user_uuid,
                    resource_type, cost)

    @acl_check
    def limit_list(self, context, parameters):

        try:
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.limits_manager.limit_list(
                    page_size, page_num)

    @acl_check
    def limit_update(self, context, parameters):

        try:
            team_level = parameters.get('team_level')
            resource_type = parameters.get('resource_type')
            limit = parameters.get('limit')

            team_level = parameter_check(team_level, ptype='pstr')
            resource_type = parameter_check(resource_type, ptype='pstr')
            limit = parameter_check(limit, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.limits_manager.limit_update(
                    team_level, resource_type, limit)

    @acl_check
    def resource_create(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            resource_uuid = parameters.get('resource_uuid')
            resource_name = parameters.get('resource_name')
            resource_type = parameters.get('resource_type')
            resource_conf = parameters.get('resource_conf')
            resource_status = parameters.get('resource_status')

            resource_uuid = parameter_check(resource_uuid, ptype='pstr')
            resource_name = parameter_check(resource_name, ptype='pnam')
            resource_type = parameter_check(resource_type, ptype='pstr')
            resource_conf = parameter_check(resource_conf, ptype='pstr')
            resource_status = parameter_check(resource_status, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.resources_manager.resource_create(
                    resource_uuid, resource_name, resource_type,
                    resource_conf, resource_status, user_uuid,
                    team_uuid, project_uuid)

    @acl_check
    def resource_delete(self, context, parameters):

        try:
            resource_uuid = context.get('resource_uuid')

            resource_uuid = parameter_check(resource_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.resources_manager.resource_delete(resource_uuid)

    @acl_check
    def resource_update(self, context, parameters):

        try:
            resource_uuid = context.get('resource_uuid')

            resource_conf = parameters.get('resource_conf')
            resource_status = parameters.get('resource_status')
            user_uuid = parameters.get('user_uuid')
            team_uuid = parameters.get('team_uuid')
            project_uuid = parameters.get('project_uuid')

            resource_uuid = parameter_check(resource_uuid, ptype='pstr')
            resource_conf = parameter_check(resource_conf, ptype='pstr',
                                            exist='no')
            resource_status = parameter_check(resource_status, ptype='pstr',
                                              exist='no')
            user_uuid = parameter_check(user_uuid, ptype='pstr',
                                        exist='no')
            team_uuid = parameter_check(team_uuid, ptype='pstr',
                                        exist='no')
            project_uuid = parameter_check(project_uuid, ptype='pstr',
                                           exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.resources_manager.resource_update(
                    resource_uuid, resource_conf, resource_status,
                    user_uuid, team_uuid, project_uuid)

    @acl_check
    def resource_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.resources_manager.resource_list(
                    team_uuid, page_size, page_num)

    @acl_check
    def resource_check(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_name = user_info.get('user_name')

            add_list = parameters['add_list']
            delete_list = parameters['delete_list']
            update_list = parameters['update_list']

            if user_name != 'service':
                return request_result(202)
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.resources_manager.resource_check(
                    add_list, delete_list, update_list)

    @acl_check
    def voucher_create(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')

            denomination = parameters.get('denomination')
            invalid_time = parameters.get('invalid_time')

            denomination = parameter_check(denomination, ptype='pint')
            invalid_time = parameter_check(invalid_time, ptype='pflt')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.vouchers_manager.voucher_create(
                    user_uuid, denomination, invalid_time)

    @acl_check
    def voucher_active(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')
            user_name = user_info.get('user_name')

            voucher_uuid = parameters.get('voucher_uuid')

            voucher_uuid = parameter_check(voucher_uuid, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.vouchers_manager.voucher_active(
                    voucher_uuid, user_uuid, team_uuid,
                    project_uuid, user_name)

    @acl_check
    def voucher_distribute(self, context, parameters):

        try:
            voucher_uuid = parameters.get('voucher_uuid')
            accepter = parameters.get('accepter')

            voucher_uuid = parameter_check(voucher_uuid, ptype='pstr')
            accepter = parameter_check(accepter, ptype='pnam')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.vouchers_manager.voucher_distribute(
                    voucher_uuid, accepter)

    @acl_check
    def voucher_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')

            start_time = parameters.get('start_time')
            end_time = parameters.get('end_time')
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            start_time = parameter_check(start_time, ptype='pflt')
            end_time = parameter_check(end_time, ptype='pflt')
            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.vouchers_manager.voucher_list(
                    user_uuid, team_uuid, start_time,
                    end_time, page_size, page_num)

    @acl_check
    def voucher_accept(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_name = user_info.get('user_name')

            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.vouchers_manager.voucher_list_accept(
                    user_name, page_size, page_num)

    @acl_check
    def bill_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            start_time = parameters.get('start_time')
            end_time = parameters.get('end_time')
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            start_time = parameter_check(start_time, ptype='pflt')
            end_time = parameter_check(end_time, ptype='pflt')
            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.bills_manager.bill_list(
                    team_uuid, start_time, end_time,
                    page_size, page_num)

    @acl_check
    def level_init(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.levels_manager.level_init(team_uuid)

    @acl_check
    def level_info(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.levels_manager.level_info(team_uuid)

    @acl_check
    def balance_init(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            balance = parameters.get('balance')
            balance = parameter_check(balance, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.balances_manager.balance_init(team_uuid, balance)

    @acl_check
    def balance_info(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.balances_manager.balance_info(team_uuid)

    @acl_check
    def balance_check(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']

            user_name = user_info.get('user_name')
            if user_name != 'service':
                return request_result(202)
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.balances_manager.balance_check()

    @acl_check
    def recharge_precreate(self, context, parameters):

        try:
            token = context.get('token')
            user_info = token_auth(context['token'])['result']
            user_name = user_info.get('user_name')

            recharge_type = parameters.get('recharge_type')
            recharge_amount = parameters.get('recharge_amount')

            recharge_amount = parameter_check(recharge_amount, ptype='pint')
            if int(recharge_amount) < 1:
                raise(Exception('Parameter error'))
            if (recharge_type != 'zhifubao') and (recharge_type != 'weixin'):
                raise(Exception('Parameter error'))
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.recharges_manager.recharge_precreate(
                    token, user_name, recharge_type, recharge_amount)

    @acl_check
    def recharge_create(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')
            user_name = user_info.get('user_name')

            recharge_uuid = parameters.get('recharge_uuid')
            recharge_type = parameters.get('recharge_type')
            recharge_amount = parameters.get('recharge_amount')

            recharge_uuid = parameter_check(recharge_uuid, ptype='pint')
            recharge_type = parameter_check(recharge_type, ptype='pstr')
            recharge_amount = parameter_check(recharge_amount, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.recharges_manager.recharge_create(
                    recharge_uuid, recharge_type, recharge_amount,
                    team_uuid, user_name)

    @acl_check
    def recharge_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            start_time = parameters.get('start_time')
            end_time = parameters.get('end_time')
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            start_time = parameter_check(start_time, ptype='pflt')
            end_time = parameter_check(end_time, ptype='pflt')
            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.recharges_manager.recharge_list(
                    team_uuid, start_time, end_time,
                    page_size, page_num)

    @acl_check
    def recharge_info(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            recharge_uuid = parameters.get('recharge_uuid')

            recharge_uuid = parameter_check(recharge_uuid, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.recharges_manager.recharge_info(
                    recharge_uuid, team_uuid)

    @acl_check
    def recharge_check(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')

            recharge_type = parameters.get('recharge_type')
            start_time = parameters.get('start_time')
            end_time = parameters.get('end_time')
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            start_time = parameter_check(start_time, ptype='pflt')
            end_time = parameter_check(end_time, ptype='pflt')
            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
            if recharge_type not in ('all', 'zhifubao', 'weixin'):
                raise(Exception('Parameter error'))
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.recharges_manager.recharge_check(
                    user_uuid, recharge_type,
                    start_time, end_time,
                    page_size, page_num)

    @acl_check
    def order_create(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            user_uuid = user_info.get('user_uuid')
            team_uuid = user_info.get('team_uuid')
            project_uuid = user_info.get('project_uuid')

            resource_uuid = parameters.get('resource_uuid')
            cost = parameters.get('cost')
            status = parameters.get('status')

            resource_uuid = parameter_check(resource_uuid, ptype='pstr')
            cost = parameter_check(cost, ptype='pflt')
            status = parameter_check(status, ptype='pstr')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.orders_manager.order_create(
                    user_uuid, team_uuid, project_uuid,
                    resource_uuid, cost, status)

    @acl_check
    def order_update(self, context, parameters):

        try:
            order_uuid = context.get('resource_uuid')

            cost = parameters.get('cost')
            status = parameters.get('status')

            cost = parameter_check(cost, ptype='pflt', exist='no')
            status = parameter_check(status, ptype='pstr', exist='no')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.orders_manager.order_update(
                    order_uuid, cost, status)

    @acl_check
    def order_list(self, context, parameters):

        try:
            user_info = token_auth(context['token'])['result']
            team_uuid = user_info.get('team_uuid')

            start_time = parameters.get('start_time')
            end_time = parameters.get('end_time')
            page_size = parameters.get('page_size')
            page_num = parameters.get('page_num')

            start_time = parameter_check(start_time, ptype='pflt')
            end_time = parameter_check(end_time, ptype='pflt')
            page_size = parameter_check(page_size, ptype='pint')
            page_num = parameter_check(page_num, ptype='pint')
        except Exception, e:
            log.warning('parameters error, context=%s, parameters=%s, reason=%s'
                      % (context, parameters, e))
            return request_result(101)

        return self.orders_manager.order_list(
                    team_uuid, start_time, end_time,
                    page_size, page_num)

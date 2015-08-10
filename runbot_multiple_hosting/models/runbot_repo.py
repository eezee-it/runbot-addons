# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    This module copyright (C) 2010 - 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import requests
import re
import os
import urlparse

from openerp import models, api, fields

import logging

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class Hosting(object):
    def __init__(self, token):
        self.session = requests.Session()
        self.session.auth = token

    @classmethod
    def get_api_url(cls, endpoint):
        return '%s%s' % (cls.API_URL, endpoint)

    @classmethod
    def get_url(cls, endpoint, *args):
        tmp_endpoint = endpoint % tuple(args)
        return '%s%s' % (cls.URL, tmp_endpoint)

    def update_status_on_commit(self, owner, repository, commit_hash, status):
        raise NotImplementedError("Should have implemented this")


class RunbotRepoDep(models.Model):
    _name = 'runbot.repo.dep'

    repo_src_id = fields.Many2one('runbot.repo', string='Repository', required=True, ondelete='cascade')
    repo_dst_id = fields.Many2one('runbot.repo', string='Repository', required=True, ondelete='cascade')
    reference = fields.Char('Reference', required=True, default="refs/heads/master")


class RunbotRepo(models.Model):
    _inherit = "runbot.repo"

    @api.model
    def _get_hosting(self):
        """
        Return a list of hosting available for Runbot

        Inherit this method to add a new hosting
        :return: A list of hosting
        """

        hosting = []
        return hosting

    hosting = fields.Selection(_get_hosting, string='Hosting', required=True)
    username = fields.Char('Username')
    password = fields.Char('Password')
    visible = fields.Boolean('Visible on the web interface of Runbot')
    dependency_nested_ids = fields.One2many('runbot.repo.dep', 'repo_src_id', string='Nested Dependency')

    @api.multi
    def get_pull_request_branch(self, pull_number):
        raise NotImplementedError("Should have implemented this")

    @api.one
    def get_hosting_instance(self):
        raise NotImplementedError("Should have implemented this")
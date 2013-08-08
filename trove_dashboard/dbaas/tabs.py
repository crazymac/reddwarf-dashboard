# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 Rackspace Hosting
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = ("dbaas/_detail_overview.html")

    def get_context_data(self, request):
        return {"instance": self.tab_group.kwargs['instance']}


class LogTab(tabs.Tab):
    name = _("Log")
    slug = "log"
    template_name = "dbaas/_detail_log.html"
    preload = False

    def get_context_data(self, request):
        instance = self.tab_group.kwargs['instance']
        tail = request.GET.get('length', None)
        try:
            data = api.nova.server_console_output(request,
                                                  instance.id,
                                                  tail)
        except:
            data = _('Unable to get log for instance "%s".') % instance.id
            exceptions.handle(request, ignore=True)
        return {"instance": instance,
                "console_log": data}


class InstanceDetailTabs(tabs.TabGroup):
    slug = "instance_details"
    tabs = (OverviewTab, LogTab)
    sticky = True
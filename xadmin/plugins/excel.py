import xadmin

from django.template import loader

from xadmin.views import BaseAdminPlugin, ListAdminView

class ListImportExcelPlugin(BaseAdminPlugin):
	import_excel =False

	def init_request(self, *args, **kwargs):
		return bool(self.import_excel)

	def block_top_toolbar(self, context, nodes):
		nodes.append(loader.render_to_string('xadmin/excel/model_list.top_toobar.import.html', context_instance=context))

xadmin.site.register_plugin(ListImportExcelPlugin, ListAdminView)
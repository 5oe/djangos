from myAdmin.acquirer.modelAdmin import ModelAdmin


class ClsIndexViewModel(object):
    def __init__(self, model_admin: ModelAdmin):
        self.model_admin = model_admin
        self.query_set = model_admin.query_set
        self.list_display = model_admin.real_list_display
        self.search_fields = model_admin.search_fields
        self.format_data = []

    def _default_handle(self):
        self.format_data = [{'id': single.id, 'obj': single} \
                            for single in self.query_set]

    def _required_handle(self):
        query_set = self.query_set.values_list(*self.list_display)

    def replace_choice_display(self, query_set):
        for obj in query_set:

        pass

    @staticmethod
    def cls_index_context(admin, args_dict):
        context = {
            'show_fields': admin.show_fields,
            'data_list': admin.handle(**args_dict),
            'list_filter': admin.analyze_list_filter(),
            'search_fields': admin.search_fields(),
            'data_total_num': admin.obj_total_num,
        }
        return context

    def required_handle_data(self, query_set):
        return query_set.values_list(*self.list_display)

    def replace_choice_display(self, data_list):
        pass

class ClsIndexViewModel(object):
    @staticmethod
    def cls_index_context(admin, args_dict):
        context = {
            'show_fields': admin.show_fields,
            'data_list': admin.get_data_list(**args_dict),
            'list_filter': admin.analyze_list_filter(),
            'search_fields': admin.get_search_fields(),
            'data_total_num': admin.data_total_num,
        }
        return context

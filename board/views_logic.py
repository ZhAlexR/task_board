from board.forms import SearchForm, FilterForm


class SearchFormMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_criteria = self.request.GET.get("search_criteria", "")
        context["search_form"] = SearchForm(
            initial={"search_criteria": search_criteria}
        )
        return context


class FilterFormMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filters = self.request.GET.getlist("status")
        sorting = self.request.GET.get("deadline", "deadline")
        context["filter_form"] = FilterForm(
            initial={
                "status": filters,
                "deadline": sorting
            }
        )
        return context

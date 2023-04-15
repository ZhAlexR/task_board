from board.forms import SearchForm, FilterForm


class SearchFormContextMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_criteria = self.request.GET.get("search_criteria", "")
        context["search_form"] = SearchForm(
            initial={"search_criteria": search_criteria}
        )
        return context


class SearchFormQuerySetMixin:

    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET)

        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["search_criteria"]
            )

        return queryset


class FilterFormMixin:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filters = self.request.GET.getlist("status")
        sorting = self.request.GET.get("deadline", "deadline")
        context["filter_form"] = FilterForm(
            initial={"status": filters, "deadline": sorting}
        )
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_form = FilterForm(self.request.GET)
        if filter_form.is_valid():
            statuses = [
                int(numb) for numb in filter_form.cleaned_data.get("status")
            ]
            deadline = filter_form.cleaned_data.get("deadline")
            if statuses:
                queryset = queryset.filter(status__in=statuses)
            queryset = queryset.order_by(deadline)

        return queryset

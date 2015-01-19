from django.core.urlresolvers import reverse
from django.views.generic import FormView, DetailView, UpdateView
from pygal.style import LightStyle
from metal.forms import SteelForm
from metal.models import Steel
from utils.helpers import get_di, get_lenghts, get_kl_data, get_hrc_from_carbon_a255_1, get_hrc_by_position


class SteelFormView(FormView):
    template_name = 'metal/steel_form.html'
    form_class = SteelForm
    steel_pk = 0

    def get_success_url(self):
        return reverse('steel_details', kwargs=dict(pk=self.steel_pk))

    def form_valid(self, form):
        instance = form.instance
        instance.save()
        self.steel_pk = instance.pk
        return super(SteelFormView, self).form_valid(form)

steel_form_view = SteelFormView.as_view()


class SteelDetail(DetailView):
    template_name_suffix = '_detail_view'
    model = Steel

    def get_context_data(self, **kwargs):
        import pygal
        context = super(SteelDetail, self).get_context_data(**kwargs)

        # context['di'] = get_di(steel=self.object)
        line_chart = pygal.Line(range=(0, 100), legend_at_bottom=True, style=LightStyle)
        line_chart.title = 'Browser usage evolution (in %)'
        # line_chart.x_labels = map(str, range(0, 82, 2))
        line_chart.x_labels = get_lenghts(steel=self.object)

        hrc = get_hrc_from_carbon_a255_1(self.object.carbon)
        kl_list = get_kl_data(steel=self.object).values()
        kl_list.sort()
        hrc_values = [get_hrc_by_position(hrc, kl) for kl in kl_list]
        line_chart.add(self.object.__unicode__(), hrc_values)

        # line_chart.add('Firefox', [None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
        # line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
        # line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
        # line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
        context['chart'] = line_chart.render()

        return context

steel_detail_view = SteelDetail.as_view()


class SteelUpdate(UpdateView):
    template_name_suffix = '_update_view'
    model = Steel

    def get_context_data(self, **kwargs):
        context = super(SteelUpdate, self).get_context_data(**kwargs)
        return context

steel_update_view = SteelUpdate.as_view()

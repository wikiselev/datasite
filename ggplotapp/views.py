from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from matplotlib import pyplot as plt
import io
import base64
from django.conf import settings
from .forms import NameForm

from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap, ggsave
from plotnine.data import mtcars

plt.switch_backend('Agg') 

def index(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            p = (
                ggplot(mtcars, aes('wt', 'mpg', color='factor(gear)')) 
                + geom_point()
                + stat_smooth(method='lm')
                + facet_wrap('~gear')
            )

            sio = io.BytesIO()
            # plt.savefig(sio, format="png")
            p.save(sio, format="png")
            encoded_img = base64.b64encode(sio.getvalue()).decode(settings.DEFAULT_CHARSET)
            return render(request, 'ggplotapp/index.html', {'form': form, 'image' : encoded_img, 'post' : 1})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'ggplotapp/index.html', {'form': form, 'post' : 0})

from rest_framework.decorators import api_view
from django.http import JsonResponse
from matplotlib import pyplot as plt
import io
import base64
from django.conf import settings
from .forms import NameForm
from .serializers import ImageSerializer
from rest_framework.renderers import JSONRenderer

from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap, ggtitle
from plotnine.data import mtcars

plt.switch_backend('Agg') 

class Plot:
    def __init__(self, image):
        self.image = image

@api_view()
def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'GET':
        p = (
            ggplot(mtcars, aes('wt', 'mpg', color='factor(gear)')) 
            + geom_point()
            + stat_smooth(method='lm')
            + facet_wrap('~gear')
            + ggtitle("test")
        )
        sio = io.BytesIO()
        p.save(sio, format="jpg")
        encoded_img = base64.b64encode(sio.getvalue()).decode(settings.DEFAULT_CHARSET)
        plot = Plot(image=encoded_img)
        serializer = ImageSerializer(plot)
        # serializer.image = encoded_img
        return JsonResponse(serializer.data)


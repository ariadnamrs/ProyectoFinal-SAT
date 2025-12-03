import base64
import ssl
import urllib.request
import json
import pyqrcode

from random import choice
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Camara, Comentario, Comentador, Like
from .camchannel2 import CamChanel2
from .camchannel import CamChanel

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'
}


def logout_view(request):
    request.session.delete()
    return HttpResponseRedirect('/')


def read_channels(url_data):
    url = url_data
    if url == "https://gitlab.eif.urjc.es/cursosweb/2023-2024/final-teveo/-/raw/main/listado1.xml":
        xmlStream = urllib.request.urlopen(url, context=ssl._create_unverified_context())
        channel = CamChanel(xmlStream)
    elif url == "https://gitlab.eif.urjc.es/cursosweb/2023-2024/final-teveo/-/raw/main/listado2.xml":
        xmlStream = urllib.request.urlopen(url, context=ssl._create_unverified_context())
        channel = CamChanel2(xmlStream)
    for cam in channel.cams():
        cam = Camara(id=cam['id'], lugar=cam['lugar'], src=cam['src'], coordenadas=cam['coordenadas'])
        list_id = Camara.objects.values_list('id', flat=True)
        if cam.id in list_id:
            print("Ya se han descargado estos datos")
        else:
            cam.save()


def camara(request, id):
    camara = Camara.objects.get(id=id)
    list_camaras = Camara.objects.all()
    list_comentarios = Comentario.objects.filter(content=camara)

    ordering = list_comentarios.order_by('-date')
    num_list_camaras = Camara.objects.all().count()
    num_list_comentarios = Comentario.objects.all().count

    id = request.session.session_key
    comentador = Comentador(id=id)
    id_session = comentador.id
    list_comentadores = Comentador.objects.values_list('id', flat=True)
    if id_session in list_comentadores:
        comentador = Comentador.objects.get(id=id_session)
        nombre_comentador = comentador.name
        if nombre_comentador == '':
            nombre_comentador = 'Anónimo'
    else:
        nombre_comentador = 'Anonimo'

    context = {
        'list_camaras': list_camaras,
        'id': camara.id,
        'imagen': camara.src,
        'lugar': camara.lugar,
        'localizacion': camara.coordenadas,
        'comentarios': ordering,
        'num_list_camaras': num_list_camaras,
        'num_list_comentarios': num_list_comentarios,
        'comentador': nombre_comentador
    }
    data = {
        'id': camara.id,
        'imagen': camara.src,
        'lugar': camara.lugar,
        'localizacion': camara.coordenadas
    }
    data_json = json.dumps(data)
    data_sin_json = json.loads(data_json)
    response = render(request, 'camara/camara.html', context)
    return HttpResponse(response)


def camara_json(request, id):
    print(request)
    camara = Camara.objects.get(id=id)
    list_comentarios = Comentario.objects.filter(content=camara)
    num_comentarios = len(list_comentarios)
    data = {
        'id': camara.id,
        'imagen': camara.src,
        'lugar': camara.lugar,
        'localizacion': camara.coordenadas,
        'comentarios': num_comentarios,

    }
    return JsonResponse(data)


def camaras(request):
    if request.method == 'POST':
        if 'valor' in request.POST:
            url = request.POST['valor']
            read_channels(url)
        elif 'id' in request.POST:
            id = request.POST['id']
            camara = Camara.objects.get(id=id)
            like = Like(me_gusta=camara)
            like.save()

    list_camaras = Camara.objects.all()
    num_list_camaras = Camara.objects.all().count()
    num_list_comentarios = Comentario.objects.all().count

    id = request.session.session_key
    comentador = Comentador(id=id)
    id_session = comentador.id
    list_comentadores = Comentador.objects.values_list('id', flat=True)
    if id_session in list_comentadores:
        comentador = Comentador.objects.get(id=id_session)
        nombre_comentador = comentador.name
        if nombre_comentador == '':
            nombre_comentador = 'Anónimo'
    else:
        nombre_comentador = 'Anónimo'
    list_fuente_datos = ['https://gitlab.eif.urjc.es/cursosweb/2023-2024/final-teveo/-/raw/main/listado1.xml',
                         'https://gitlab.eif.urjc.es/cursosweb/2023-2024/final-teveo/-/raw/main/listado2.xml', ]

    if len(list_camaras) == 0:
        context = {
            'datos': list_fuente_datos,
            'num_list_camaras': num_list_camaras,
            'num_list_comentarios': num_list_comentarios,
            'comentador': nombre_comentador
        }
        response = render(request, 'list_camaras/camaras.html', context=context)
        return HttpResponse(response)
    else:
        imagen_cam = choice(Camara.objects.values_list('src', flat=True))

        for camara in list_camaras:
            camara.num_comentarios = Comentario.objects.filter(content=camara).count()
            camara.likes = Like.objects.filter(me_gusta=camara).count()

        qr = pyqrcode.create(imagen_cam)
        qr.png('qr.png', scale=2)

        context = {
            'list_camaras': list_camaras,
            'imagen_cam': imagen_cam,
            'datos': list_fuente_datos,
            'num_list_camaras': num_list_camaras,
            'num_list_comentarios': num_list_comentarios,
            'comentador': nombre_comentador
        }
        response = render(request, 'list_camaras/camaras.html', context=context)
        return HttpResponse(response)


def index(request):
    id = request.session.session_key
    comentador = Comentador(id=id)
    id_session = comentador.id
    list_comentadores = Comentador.objects.values_list('id', flat=True)
    if id_session in list_comentadores:
        comentador = Comentador.objects.get(id=id_session)
        nombre_comentador = comentador.name
        if nombre_comentador == '':
            nombre_comentador = 'Anónimo'
    else:
        nombre_comentador = 'Anónimo'

    list_comentarios = Comentario.objects.all()
    ordering = list_comentarios.order_by('-date')
    num_list_camaras = Camara.objects.all().count()
    num_list_comentarios = Comentario.objects.all().count
    context = {

        'list_comentarios': ordering,
        'num_list_camaras': num_list_camaras,
        'comentador': nombre_comentador,
        'num_list_comentarios': num_list_comentarios,
    }

    response = render(request, 'main/main.html', context)
    return HttpResponse(response)


def configuracion(request):
    print("Session Key:", request.session.session_key)

    id = None
    if 'id' in request.GET:
        id = request.GET['id']
        print("GET id:", id)
        request.session['id'] = id

    elif 'id' in request.session:
        id = request.session.get('id')
        print("Session id:", id)
    else:
        if not request.session.session_key:
            request.session.save()
        print(request.session.session_key)
        id = request.session.session_key
        request.session['id'] = id
        print("New session id:", id)

    if not id:
        print("Error: 'id' es None")
        return HttpResponse("Error: 'id' es None", status=400)

    comentador = Comentador(id=id)
    id_session = comentador.id
    print("Session ID after Comentador creation:", id_session)

    list_comentadores = Comentador.objects.values_list('id', flat=True)
    if id_session in list_comentadores:
        comentador = Comentador.objects.get(id=id_session)
        nombre_comentador = comentador.name
        if nombre_comentador == '':
            nombre_comentador = 'Anónimo'
    else:
        nombre_comentador = 'Anónimo'

    num_list_camaras = Camara.objects.all().count()
    num_list_comentarios = Comentario.objects.all().count()

    id = request.session['id']
    if request.method == 'POST':
        nombre = request.POST.get('nombre', 'Anónimo')
        size = request.POST.get('size', '')
        letra = request.POST.get('letra', '')
        comentador.name = nombre
        comentador.letra_size = size
        comentador.letra_tipo = letra
        comentador.save()
        context = {
            'id': id,
            'size': size,
            'letra': letra,
            'comentador': nombre_comentador,
            'num_list_camaras': num_list_camaras,
            'num_list_comentarios': num_list_comentarios,
        }
    else:
        context = {
            'id': id,
            'comentador': nombre_comentador,
            'num_list_camaras': num_list_camaras,
            'num_list_comentarios': num_list_comentarios,
        }

    response = render(request, 'configuracion/configuracion.html', context=context)
    return HttpResponse(response)


def download_image(image_camara):
    request = urllib.request.Request(url=image_camara, headers=headers)
    try:
        with urllib.request.urlopen(request) as response:
            image = response.read()
    except urllib.error.URLError as e:
        return None
    return image


def dynamic(request, id_camara):
    camara = Camara.objects.get(id=id_camara)

    image = download_image(camara.src)
    list_comentarios = Comentario.objects.filter(content=camara)
    num_list_camaras = Camara.objects.all().count()
    num_list_comentarios = Comentario.objects.all().count()

    id_session = request.session.session_key
    list_comentadores = Comentador.objects.values_list('id', flat=True)
    if id_session in list_comentadores:
        comentador = Comentador.objects.get(id=id_session)
        nombre_comentador = comentador.name
        if nombre_comentador == '':
            nombre_comentador = 'Anónimo'
    else:
        nombre_comentador = 'Anónimo'

    image_base64 = base64.b64encode(image).decode('utf-8')

    context = {
        'comentarios': list_comentarios,
        'image_base64': image_base64,
        'image': image,
        'id': id_camara,
        'num_camaras': num_list_camaras,
        'num_comentarios': num_list_comentarios,
        'comentador': nombre_comentador
    }

    response = render(request, 'dinamica/dinamica.html', context=context)
    return HttpResponse(response)


def help(request):
    id = request.session.session_key
    comentador = Comentador(id=id)
    id_session = comentador.id
    list_comentadores = Comentador.objects.values_list('id', flat=True)
    if id_session in list_comentadores:
        comentador = Comentador.objects.get(id=id_session)
        nombre_comentador = comentador.name
        if nombre_comentador == '':
            nombre_comentador = 'Anónimo'
    else:
        nombre_comentador = 'Anónimo'

    num_list_camaras = Camara.objects.all().count()
    num_list_comentarios = Comentario.objects.all().count

    context = {
        'comentador': nombre_comentador,
        'num_list_camaras': num_list_camaras,
        'num_list_comentarios': num_list_comentarios,
    }
    response = render(request, 'ayuda/help.html', context=context)
    return HttpResponse(response)


def create_comentario(request):
    id = request.GET.get('id')
    camara = Camara.objects.get(id=id)
    id = request.session.session_key
    comentador = Comentador(id=id)
    id_session = comentador.id

    list_comentadores = Comentador.objects.values_list('id', flat=True)
    if id_session in list_comentadores:
        comentador = Comentador.objects.get(id=id_session)
        nombre_comentador = comentador.name
        if nombre_comentador == '':
            nombre_comentador = 'Anonimo'
    else:
        nombre_comentador = 'Anonimo'

    num_list_camaras = Camara.objects.all().count()
    num_list_comentarios = Comentario.objects.all().count

    if request.method == "POST":
        valor = request.POST['valor']
        if comentador.name == '':
            comentador.name = 'Anonimo'

        comentario = camara.comentario_set.create(title="Comentario", body=valor, date=timezone.now(),
                                                  comentador=comentador.name)
        comentario.save()

    context = {
        'num_list_camaras': num_list_camaras,
        'num_list_comentarios': num_list_comentarios,
        'imagen': camara.src,
        'lugar': camara.lugar,
        'localizacion': camara.coordenadas,
        'comentador': nombre_comentador,
    }
    response = render(request, 'comentario/coment.html', context)
    return HttpResponse(response)


def get_css(request):
    if not request.session.session_key:
        request.session.save()

    id = request.session.get('id')
    list_comentadores = Comentador.objects.all()

    comentador_now = Comentador(id=id)
    if comentador_now in list_comentadores:
        comentador = Comentador.objects.get(id=id)
        letra = comentador.letra_tipo
        size = comentador.letra_size

    else:
        letra = 'Arial'
        size = '16px'
    context = {
        'letra': letra,
        'size': size
    }
    css = render(request, 'dynamic.css', context=context)
    return HttpResponse(css, content_type='text/css')

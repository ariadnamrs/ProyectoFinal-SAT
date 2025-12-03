from django.test import TestCase, Client
from django.urls import reverse
from .models import Camara, Comentador, Comentario


class EndToEndTests(TestCase):

    def test_create_camara(self):
        camara = Camara(num_comentarios=0, src='http://test.com', lugar='Malaga', coordenadas='0.0.0', id=1)
        self.assertEqual(camara.num_comentarios, 0)

    def test_create_comentario(self):
        camara = Camara(num_comentarios=0, src='http://test.com', lugar='Malaga', coordenadas='0.0.0', id=1)
        comentario = Comentario(content=camara, comentador='Pepito', title='Titulo', body='Cuerpo_comentario',
                                date='14:20_56')
        self.assertEqual(comentario.comentador, 'Pepito')

    def test_create_comentador(self):
        comentador = Comentador(id=3939399393, name='Joaquin', letra_size='12px', letra_tipo='Arial')
        self.assertEqual(comentador.name, 'Joaquin')


class GetTests(TestCase):

    def test_root(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn(' <h1><a href="/">TeVeO </a></h1>', content)

    def test_get_css_view(self):
        # Crea un cliente para simular solicitudes HTTP
        client = Client()

        # Realiza una solicitud GET a la vista get_css
        response = client.get(reverse('dynamic_css'))

        # Verifica que la solicitud haya sido exitosa (código de estado 200)
        self.assertEqual(response.status_code, 200)

        # Verifica que el contenido de la respuesta sea de tipo CSS
        self.assertIn('text/css', response['Content-Type'])

        # Verifica que la respuesta contenga la información esperada
        # Puedes ajustar esta parte según lo que esperes que devuelva tu vista
        self.assertIn('Arial', response.content.decode('utf-8'))
        self.assertIn('16px', response.content.decode('utf-8'))
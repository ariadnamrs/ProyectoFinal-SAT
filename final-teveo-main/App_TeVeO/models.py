from django.db import models
from django.db.models.functions import Now


class Comentador(models.Model):
    id = models.CharField(max_length=256, primary_key=True)
    name = models.CharField(max_length=100)
    letra_size = models.CharField(max_length=100, default=None)
    letra_tipo = models.CharField(max_length=100, default=None)


class Camara(models.Model):
    num_comentarios = models.IntegerField(default=0)
    src = models.TextField()
    lugar = models.CharField(max_length=256)
    coordenadas = models.CharField(max_length=100)
    id = models.CharField(max_length=100, primary_key=True)


class Comentario(models.Model):
    content = models.ForeignKey(Camara, on_delete=models.CASCADE)
    comentador = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    body = models.TextField()
    date = models.DateTimeField(db_default=Now())


class Like(models.Model):
    me_gusta = models.ForeignKey(Camara, on_delete=models.CASCADE)

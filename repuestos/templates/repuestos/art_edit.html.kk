
{% load widget_tweaks %}

<html>

    <head>
        <title>Fresenius - Edicion Articulo</title>

        <style>
            .special div {
            border: 2px solid #f00;
            margin: -2px;
            }
        </style>








  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
  <title>Simple is Better Than Complex</title>







    </head>

    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.4.0/css/font-awesome.min.css">

<body>

<ul class="sidebar-nav">
        {% if user.is_authenticated %}
        <li>User: {{ user.get_username }}</li>
        <li><a href="{% url 'logout'%}?next={{request.path}}">Salir</a></li>
        {% else %}
        <li><a href="{% url 'login'%}?next={{request.path}}">Ingresar</a></li>
        {% endif %}
        </ul>



<table class="w3-table-all">
    <thead>
<tr class="w3-pale-red">
  <th>&nbsp;User: {{ user.get_username }}</th>
  <th class="w3-center"><h4 class="w3-opacity">Pag. de Edición</h4></th>
  <th><strong>Estado:</strong>&nbsp;{{ articulo_instance.SYS_ESTADO }}</th>
</tr>
</thead>
</table>


</div>

    <div><br><br>
     </div>


    <form action="" method="POST"  class="post-form">{% csrf_token %}





{% for field in form.visible_fields %}
    <div class="form-group">
      {{ field.titulo }}

{% render_field field class="form-control" %}

{% if field.Descripcion %}
        <small class="form-text text-muted">{{ field.Descripcion }}</small>
        {% render_field field class="form-control" %}
      {% endif %}
    </div>




{% endfor %}







    <table style="height: 50px; margin-left: auto; margin-right: auto;" border="0" width="1200" cellspacing="0" cellpadding="5">
    <tbody>
    <tr>
    <td width=200px><img src="http://reflexpnt.pythonanywhere.com/media/GUI_pictures/logoFresenius.jpg" width="200" height="42" /></td>
    <td  align="center"   width=700px></td>
    <td valign="bottom"><strong>Especificaciones T&eacute;cnicas</strong></td>
    </tr>
    </tbody>
    </table>


     <div>

     </div>
        <br>

<input type="text"
       name="titulo"
       id="id_name"
       {% if form.titulo.value != None %}value="{{ form.titulo.value|stringformat:'s' }}"{% endif %}
       maxlength="{{ form.titulo.field.max_length }}"
       >


    <table style="height: 5px; width: 1200px; margin-left: auto; margin-right: auto;" border="0" width="1200" cellspacing="0" cellpadding="3">
    <tbody>
    <tr >
    <td   width=320px bgcolor ="#0000e6"><font color="white"><font size="6"><strong>{{ articulo_instance.numeroParte }}</strong></td>
    <td   width=810px bgcolor ="#0000e6"><font color="white"><font size="6">&nbsp;{{ articulo_instance.titulo }}</td>
    <td bgcolor = "#0000e6"><button type="submit" class="save btn btn-default">Guardar</button></td>
    </tr>

    </tbody>
    </table>





    <div><br>
     </div>


    <table style="height: 5px; margin-left: auto; margin-right: auto;" border="0" width="1200" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td style="width: 597px;" bgcolor="#d9d9d9"><strong>INFORMACI&Oacute;N PARA COMPRAS</strong></td>
    </tr>
    </tbody>
    </table>


    <div><br>
     </div>


    <table style="height: 96px; width: 1200px; margin-left: auto; margin-right: auto;" border="1" cellspacing="0" cellpadding="6">
    <tbody>
    <tr>
    <td style="width: 10px;"><strong>Marca</strong></td>
    <td style="width: 687px;">&nbsp;{{ form.marca }}</td>
    <td style="width: 10px;"><strong>Reemplazable</strong></td>
    <td align="center"  style="width: 20px;">{{ form.Reemplazable }}&nbsp;</td>
    </tr>
    <tr>
    <td style="width: 10px;"><strong>Mod./# Parte</strong></td>
    <td style="width: 687px;">&nbsp;{{ form.modelo_NumParte }}</td>
    <td style="width: 10px;"><strong>Fab.a Pedido</strong></td>
    <td  align="center"  style="width: 20px;">{{ form.Fab_a_Pedido }}&nbsp;</td>
    </tr>
    <tr>
    <td style="width: 10px;"><strong>Linea</strong></td>
    <td style="width: 687px;" >{{ form.linea }}</td>
    <td style="width: 10px;"><strong>Plano</strong></td>
    <td align="center"  style="width: 20px;">{{ form.Plano }}&nbsp;</td>
    </tr>
    <tr>
    <td style="width: 10px;"><strong>Comentarios</strong></td>
    <td style="width: 687px;">&nbsp;{{ form.comentario }}</td>
    <td style="width: 10px;"><strong>Unidad</strong></td>
    <td align="center" style="width: 20px;">&nbsp;[&nbsp;{{ articulo_instance.unidad }}&nbsp;]</td>
    </tr>
    </tbody>
    </table>


   <div><br>
     </div>


    <table align="center" style="height: 5px; margin-left: auto; margin-right: auto;" border="0" width="1200" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td style="width: 597px;" bgcolor="#d9d9d9"><strong>DESCRIPCI&Oacute;N</strong></td>
    </tr>
    </tbody>
    </table>


    <table style="height: 300px; width: 1200px; margin-left: auto; margin-right: auto;" border="0" cellspacing="0" cellpadding="15">
    <tbody>
    <tr >
    <td width=5px >&nbsp;</td>
    <td class="special" width=300px valign="center"><img  width="300" src="http://freseniusmedicalcare.pythonanywhere.com/media/{{ articulo_instance.imagen_pri }}"</td>
    <td width=5px >&nbsp;</td>
    <td valign="top" align="left">
      </td>



    </tr>
    <tr >
    <td >&nbsp;</td>
    <td align="center" >{{ form.imagen_pri }}</td>
    <td >&nbsp;</td>
    <td >&nbsp;</td>
    </tr>
    </tbody>
    </table>



   <div><br>
     </div>


    <table style="height: 26px; width: 1200px; margin-left: auto; margin-right: auto;" border="0" cellspacing="0" cellpadding="4">
    <tbody>
    <tr>
    <td style="width: 12px;" bgcolor="#d9d9d9">&nbsp;</td>
    <td style="width: 1182px;" bgcolor="#d9d9d9"><strong>CONTROLES / ENSAYOS</strong></td>
    </tr>
    <tr>
    <td style="width: 12px;" bgcolor="#ffffff">&nbsp;</td>
    <td style="width: 1182px;" bgcolor="#ffffff">{{ form.Ensayos }}</td>
    </tr>
    </tbody>
    </table>

    <div><br>
     </div>


    <table style="height: 26px; width: 1200px; margin-left: auto; margin-right: auto;" border="0" cellspacing="0" cellpadding="4">
    <tbody>
    <tr>
    <td style="width: 12px;" bgcolor="#d9d9d9">&nbsp;</td>
    <td style="width: 1182px;" bgcolor="#d9d9d9"><strong>REFERENCIAS</strong></td>
    </tr>
    <tr>
    <td style="width: 12px;" bgcolor="#ffffff">&nbsp;</td>
    <td style="width: 1182px;" bgcolor="#ffffff">{{ form.Referencia1 }}</td>
    </tr>
    <tr>
    <td style="width: 12px;" bgcolor="#ffffff">&nbsp;</td>
    <td style="width: 1182px;" bgcolor="#ffffff">{{ form.Referencia2}}</td>
    </tr>
    <tr>
    <td style="width: 12px;" bgcolor="#ffffff">&nbsp;</td>
    <td style="width: 1182px;" bgcolor="#ffffff">{{ form.Referencia3}}</td>
    </tr>
    <tr>
    <td style="width: 12px;" bgcolor="#ffffff">&nbsp;</td>
    <td style="width: 1182px;" bgcolor="#ffffff">{{ form.Referencia4}}</td>
    </tr>
    <tr>
    <td style="width: 12px;" bgcolor="#ffffff">&nbsp;</td>
    <td style="width: 1182px;" bgcolor="#ffffff">{{ form.Referencia5 }}</td>
    </tr>
    </tbody>
    </table>

    <div><br>
     </div>


    <table style="height: 26px; width: 1200px; margin-left: auto; margin-right: auto;" border="0" cellspacing="0" cellpadding="4">
    <tbody>
    <tr>
    <td style="width: 12px;" bgcolor="#d9d9d9">&nbsp;</td>
    <td style="width: 1182px;" bgcolor="#d9d9d9"><strong>CONTROL DE CAMBIOS</strong></td>
    </tr>
    <tr>
    <td style="width: 12px;" bgcolor="#ffffff">&nbsp;</td>
    <td style="width: 1182px;" bgcolor="#ffffff"></td>
    </tr>
    </tbody>
    </table>
    <table style="width: 1200px; height: 50px; margin-left: auto; margin-right: auto;" border="1" cellspacing="0" cellpadding="3">
    <tbody>
    <tr>
    <td style="width: 10px;"><strong>Rev.</strong></td>
    <td style="width: 452px;"><strong>Modificaci&oacute;n</strong></td>
    <td style="width: 35px; text-align: center;"><strong>Fecha</strong></td>
    </tr>
    <tr>
    <td style="width: 10px; text-align: center;">00</td>
    <td style="width: 452px;">Emisi&oacute;n</td>
    <td style="width: 35px;">&nbsp;</td>
    </tr>
    <tr>
    <td style="width: 10px;">&nbsp;</td>
    <td style="width: 452px;">&nbsp;</td>
    <td style="width: 35px;">&nbsp;</td>
    </tr>
    </tbody>
    </table>


<div><br>
     </div>

    <table style="height: 4px; margin-left: auto; margin-right: auto;" border="0" width="1200" cellspacing="0" cellpadding="0">
    <tbody>
    <tr>
    <td style="width: 603px;" bgcolor="#0000e6">&nbsp;</td>
    </tr>
    </tbody>
    </table>

    <table style="height: 12px; width: 1200px; margin-left: auto; margin-right: auto;" border="0" cellspacing="0" cellpadding="5">
    <tbody>
    <tr>
    <td style="width: 10px;">&nbsp;</td>
    <td style="width: 447px;"><strong>AR-PE-06-050 - Rev.00 - 15/06/2018</strong></td>
    </tr>
    </tbody>
    </table>


    <div><br><br>
     </div>
    <div><br><br>
     </div>
    <div><br><br>
     </div>
    <div><br><br>
     </div>
    <div><br><br>
     </div>


{{ form.SYS_Prioridad }}

{{ form.SYS_ESTADO }}

        </form>


</body>



</html>

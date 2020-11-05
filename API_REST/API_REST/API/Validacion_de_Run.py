from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from itertools import cycle
#https://www.registrocivil.cl/PortalOI/Manuales/Validacion_de_Run.pdf

def verificador_run(Run):
    try:
        num_Run,verificador = Run.split('-')
    except:
        raise ValidationError(_('%(Run)s no es valido, falta \'-\'.'),params={'Run': Run},)

    if verificador.lower() == 'k':
        verificador = 10

    Run_inverso = map(int,reversed(str(num_Run)))
    factores = cycle(range(2,8))

    S = sum(i*n for i, n in zip(Run_inverso,factores))
    Ri = S % 11
    Rf = 11 - Ri

    if Rf == 11:
        Rf = 0

    if Rf != int(verificador):
        raise ValidationError(
            _('%(Run)s no es valido.'),
            params={'Run': Run},
        )
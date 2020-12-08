import random
secret="".join([random.SystemRandom().choice(')(o--2n^&xp^0_fg6(76@o6n0)o6s%+&lte6utip8kkb$4=xdn') for i in range(50)])
print("export SECRET_KEY='{0}'".format(secret))
print("export DJANGO_SUPERUSER_PASSWORD='{0}'".format("Secret.123"))
print("export DJANGO_SUPERUSER_EMAIL='{0}'".format("Fernando.Alonso@sigvip.com"))
print("export DJANGO_SUPERUSER_USERNAME='{0}'".format("Fernando"))
print("export DJANGO_SUPERUSER_APELLIDOP='{0}'".format("Alonso"))
print("export DJANGO_SUPERUSER_APELLIDOM='{0}'".format("Díaz"))
print("export DJANGO_SUPERUSER_RUT='{0}'".format("8332472-4"))
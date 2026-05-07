[app]
title = Expert Yafaa Shield
package.name = yafshield
package.domain = org.salah
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المتطلبات الأساسية التي يطلبها السيرفر الآن
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,chardet,idna,flask,pyTelegramBotAPI

# الأيقونة والخلفية (تأكد أن الاسم هو background.png)
icon.filename = background.png
presplash.filename = background.png

orientation = portrait
fullscreen = 0
android.archs = armeabi-v7a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.allow_backup = True

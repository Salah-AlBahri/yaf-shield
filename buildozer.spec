[app]
title = Expert Yafaa Shield
package.name = yafshield
package.domain = org.salah
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# المتطلبات الأساسية لعمل الكود الخاص بك
requirements = python3,kivy==2.3.0,flask,pyTelegramBotAPI,requests,urllib3,certifi,chardet,idna

# أيقونة التطبيق وصورة البداية
icon.filename = background.png
presplash.filename = background.png

orientation = portrait
fullscreen = 0
android.archs = armeabi-v7a
android.api = 33
android.minapi = 21
android.ndk = 25b
android.allow_backup = True

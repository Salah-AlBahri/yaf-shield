[app]
title = Expert Yafaa Shield
package.name = yafshield
package.domain = org.salah
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# هذه هي المكتبات التي يحتاجها كودك بالضبط ليعمل
requirements = python3,kivy,requests,urllib3,certifi,chardet,idna,flask,pyTelegramBotAPI

# ربط الأيقونة بالخلفية التي سميناها background.png
icon.filename = background.png
presplash.filename = background.png

orientation = portrait
fullscreen = 0
android.archs = armeabi-v7a
android.allow_backup = True

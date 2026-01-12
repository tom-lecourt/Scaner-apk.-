[app] title = XeleryScan package.name = xeleryscan package.domain =
org.xelery source.dir = . source.include_exts = py,png,jpg,kv,atlas
version = 0.1 requirements = python3,kivy,pillow,pyzbar,requests
orientation = portrait android.permissions = CAMERA, INTERNET
android.api = 31 android.archs = arm64-v8a

[buildozer] log_level = 2 warn_on_root = 1

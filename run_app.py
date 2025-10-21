#!/usr/bin/env python3


import sys
import os


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


try:
    from distutils.version import StrictVersion
except ImportError:
    print("🔧 Применяем исправление для Python 3.12+...")

    import types



    class StrictVersion:
        def __init__(self, vstring):
            self.version = vstring

        def __str__(self):
            return self.version

        def __repr__(self):
            return f"StrictVersion('{self.version}')"



    distutils_version = types.ModuleType('distutils.version')
    distutils_version.StrictVersion = StrictVersion


    sys.modules['distutils.version'] = distutils_version


    distutils = types.ModuleType('distutils')
    distutils.version = distutils_version
    sys.modules['distutils'] = distutils

    print("✅ Исправление применено успешно")


try:
    from main import CryptoDetector

    print("🚀 Запуск Crypto Price Detector...")
    app = CryptoDetector()
    app.run()

except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("Убедитесь, что установлены все зависимости:")
    print("pip install -r requirements.txt")

except Exception as e:
    print(f"❌ Ошибка запуска: {e}")
    input("Нажмите Enter для выхода...")

from setuptools import setup

APP = ['billing.py']

DATA_FILES = ['logo.jpg']

OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'reportlab', 'PIL'],
    'includes': ['invoice_pdf'],
    'plist': {
        'CFBundleName': 'Shivay Billing',
        'CFBundleDisplayName': 'Shivay Billing',
        'CFBundleIdentifier': 'com.shivaytextiles.billing',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

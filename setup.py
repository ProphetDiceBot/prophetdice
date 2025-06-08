from setuptools import setup, find_packages

setup(
    name='pdice',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scikit-learn',
        'undetected-chromedriver',
        'asyncio',
        'tqdm',
        'pytesseract',
        'spacy',
        'pymupdf',
        'google-generativeai',
        'mistralai',
        'imblearn',
        'requests',
        'fastapi',
        'uvicorn',
        'pyautogui',
        'crewai',
        'pywebio',
        'pywebio-battery',

    ],
    author='Prophet Dice Bot',
    author_email='support@prophetdice.com',
    description='ProphetDice Functions',
    url='https://prophetdice.com',
)

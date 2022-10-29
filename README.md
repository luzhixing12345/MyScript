# MyScript

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)
![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)

MyScript is a Python script for auto environment setup

Type what you want, `MyScript` will save your time for searching:

- how to install
- where to find offical document

## Introduction

## Usage (Linux Only)

### Requirement

```bash
pip install rich
```

### Run

```bash
python main.py
```

### Other options

- get the lastest file to upgrade

  ```bash
  python MyScript.py --upgrade
  ```

- Set global environment variables for `MyScript.py` to use shorter

  ```bash
  python MyScript.py -> myscript
  python MyScript.py --upgrade -> myscript -upgrade
  ```

## Support

![Conda](https://img.shields.io/badge/conda-342B029.svg?&style=for-the-badge&logo=anaconda&logoColor=white)
![PYPI](https://img.shields.io/badge/pypi-3775A9?style=for-the-badge&logo=pypi&logoColor=white)
![NPM](https://img.shields.io/badge/npm-CB3837?style=for-the-badge&logo=npm&logoColor=white)

## Contribution

Hope for your contribution and expecially thanks for your contribution!

### Contribute for information

- fork this repo
- create a json file under `configuration` in the corresponding position
- read the corresponding README file first to find what the json file should include
- finsh your json and DO **NOT** run build.py
- create a new pull request

## Develop Reference

- [non-block keyboardmap](https://github.com/luzhixing12345/keyboardmap)
- [rich](https://github.com/Textualize/rich)
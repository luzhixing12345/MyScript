# MyScript

MyScript is a Python script for auto environment setup

Type what you want, `MyScript` will save your time for searching:

- how to install
- where to find offical document

## Introduction

[gif](gif)

## Usage

### Requirement

```bash
pip install rich
```

### Get source script

- Linux

  ```bash
  wget https://raw.githubusercontent.com/luzhixing12345/MyScript/main/MyScript.py
  ```

- Windows

  ```bash
  curl https://raw.githubusercontent.com/luzhixing12345/MyScript/main/MyScript.py
  ```

### Run

```bash
python MyScript.py
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

![python](https://img.shields.io/badge/python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
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

- [rich](https://github.com/Textualize/rich)
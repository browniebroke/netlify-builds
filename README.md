# Netlify Builds

<p align="center">
  <a href="https://github.com/browniebroke/netlify-builds/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/browniebroke/netlify-builds/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://codecov.io/gh/browniebroke/netlify-builds">
    <img src="https://img.shields.io/codecov/c/github/browniebroke/netlify-builds.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
  <a href="https://results.pre-commit.ci/latest/github/browniebroke/netlify-builds/main">
    <img src="https://results.pre-commit.ci/badge/github/browniebroke/netlify-builds/main.svg" alt="pre-commit.ci status">
  </a>
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/badge/packaging-poetry-299bd7?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAASCAYAAABrXO8xAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAJJSURBVHgBfZLPa1NBEMe/s7tNXoxW1KJQKaUHkXhQvHgW6UHQQ09CBS/6V3hKc/AP8CqCrUcpmop3Cx48eDB4yEECjVQrlZb80CRN8t6OM/teagVxYZi38+Yz853dJbzoMV3MM8cJUcLMSUKIE8AzQ2PieZzFxEJOHMOgMQQ+dUgSAckNXhapU/NMhDSWLs1B24A8sO1xrN4NECkcAC9ASkiIJc6k5TRiUDPhnyMMdhKc+Zx19l6SgyeW76BEONY9exVQMzKExGKwwPsCzza7KGSSWRWEQhyEaDXp6ZHEr416ygbiKYOd7TEWvvcQIeusHYMJGhTwF9y7sGnSwaWyFAiyoxzqW0PM/RjghPxF2pWReAowTEXnDh0xgcLs8l2YQmOrj3N7ByiqEoH0cARs4u78WgAVkoEDIDoOi3AkcLOHU60RIg5wC4ZuTC7FaHKQm8Hq1fQuSOBvX/sodmNJSB5geaF5CPIkUeecdMxieoRO5jz9bheL6/tXjrwCyX/UYBUcjCaWHljx1xiX6z9xEjkYAzbGVnB8pvLmyXm9ep+W8CmsSHQQY77Zx1zboxAV0w7ybMhQmfqdmmw3nEp1I0Z+FGO6M8LZdoyZnuzzBdjISicKRnpxzI9fPb+0oYXsNdyi+d3h9bm9MWYHFtPeIZfLwzmFDKy1ai3p+PDls1Llz4yyFpferxjnyjJDSEy9CaCx5m2cJPerq6Xm34eTrZt3PqxYO1XOwDYZrFlH1fWnpU38Y9HRze3lj0vOujZcXKuuXm3jP+s3KbZVra7y2EAAAAAASUVORK5CYII=" alt="Poetry">
  </a>
  <a href="https://github.com/ambv/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" alt="black">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/netlify-builds/">
    <img src="https://img.shields.io/pypi/v/netlify-builds.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/netlify-builds.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/netlify-builds.svg?style=flat-square" alt="License">
</p>

A command line utility to check build usage across multiple Netlify accounts

## Installation

Recommended to install this via [pipx]:

`pipx install netlify-builds`

## Setup

Create a `.netlify-builds.json` in your home directory with the following shape:

```json
{
  "team-name-1": "access-token-1",
  "team-name-2": "access-token-2",
  ...
}
```

To obtain the token for each team, open a private browsing session and login to your team dashboard and copy it from the local storage, it should be located under the key `nf-session`.

DO NOT LOG OUT. Instead, simply close the private browsing session. If you log out, the token will be invalidated.

## Profit

You're good to go, check all your accounts from the comfort of your terminal:

```
➜ netlify-builds
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━┓
┃ Team              ┃     Mins ┃ Start Date ┃ End Date   ┃ Elapsed ┃  Used ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━┩
│ team-blue         │   5 mins │ 2020-11-16 │ 2020-12-16 │   11.6% │  1.7% │
│ team-red          │ 182 mins │ 2020-10-27 │ 2020-11-27 │   75.9% │ 60.7% │
│ team-green        │  46 mins │ 2020-11-02 │ 2020-12-02 │   58.3% │ 15.3% │
└───────────────────┴──────────┴────────────┴────────────┴─────────┴───────┘
```

If you're likely to exceed the free quota (300 mins) the rows will appear in red, otherwise in green.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key]):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://browniebroke.com/"><img src="https://avatars1.githubusercontent.com/u/861044?v=4?s=80" width="80px;" alt=""/><br /><sub><b>Bruno Alla</b></sub></a><br /><a href="https://github.com/browniebroke/netlify-builds/commits?author=browniebroke" title="Code">💻</a> <a href="https://github.com/browniebroke/netlify-builds/commits?author=browniebroke" title="Documentation">📖</a> <a href="#ideas-browniebroke" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors] specification. Contributions of any kind welcome!

## Credits

This package was created with [Cookiecutter] and the [browniebroke/cookiecutter-pypackage][bb-cc-pypkg] project template.

[pipx]: https://pipxproject.github.io/pipx/
[emoji key]: https://allcontributors.org/docs/en/emoji-key
[all-contributors]: https://github.com/all-contributors/all-contributors
[cookiecutter]: https://github.com/audreyr/cookiecutter
[bb-cc-pypkg]: https://github.com/browniebroke/cookiecutter-pypackage

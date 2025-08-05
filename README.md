# 🐍 py-logic

Implementation of a logic formula parser and truth table generator in Python.

## 📚 Table of Contents

- [📜 Overview](#-overview)
- [🛠 Usage](#-usage)
- [📋 Requirements](#-requirements)
- [📄 License](#-license)
- [💝 Sponsor](#-sponsor)

## 📜 Overview

This project is meant as educational material in order to learn about basic
interpreters and the process of lexing and parsing a language as well as the
concept of AST (Abstract Syntax Tree), therefore why it supports only basic
logic symbols.

The choice of interpreting logic formulas was made due to its relative
simplicity and the fact that it is related to computer science.

That is also the same reason the tutorial is written in Python, as it is a
popular language for beginners and it is easy to understand, you can find the
whole blog post
[here](https://aster.deno.dev/posts/introduction-to-interpreters-part-1/). This
also has a second part
[here](https://aster.deno.dev/posts/introduction-to-interpreters-part-2/) (which
project you can also find [here](https://github.com/4ster-light/f-logic)) that
goes even further explaining functional programming concepts in F# and
showcasing its features for this use case.

## 🛠 Usage

- Run `python main.py` to generate a truth table for a given formula:

```bash
$ python main.py
Enter a logical formula (e.g., P & Q -> R, !A | B):

P & Q -> R

P | Q | R | P & Q -> R
----------------------
T | T | T | T
T | T | F | F
T | F | T | T
T | F | F | T
F | T | T | T
F | T | F | T
F | F | T | T
F | F | F | T
```

- Run `python main.py --debug` to see the tokens and expression tree generated
  by the parser:

```bash
$ python main.py --debug
Enter a logical formula (e.g., P & Q -> R, !A | B):

P & Q -> R

- Formula:
  - P & Q -> R
- Tokens:
  - Token(type='Variable', lexeme='P')
  - Token(type='AndOp', lexeme='&')
  - Token(type='Variable', lexeme='Q')
  - Token(type='ImpliesOp', lexeme='->')
  - Token(type='Variable', lexeme='R')
  - Token(type='Eof', lexeme=None)
- Expression:
  - Implies(left=And(left=Var(name='P'), right=Var(name='Q')), right=Var(name='R'))
```

## 📋 Requirements

Only Python 3 or higher is required.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.

## 💝 Sponsor

If you like this project, consider supporting me by buying me a coffee.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B41HVJUR)

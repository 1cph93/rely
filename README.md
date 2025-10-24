# Rely

[![Test](https://github.com/1cph93/rely/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/1cph93/rely/actions/workflows/test.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)

Rely is a tool for vetting GitHub dependencies.

> [!NOTE]
>
> Rely is in active development and certain features may be incomplete.

## Installation

1. Create a GitHub personal access token ([guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens))
2. Clone the repo
   ```sh
   git clone https://github.com/1cph93/rely.git
   ```
3. Ensure `uv` is installed ([guide](https://docs.astral.sh/uv/getting-started/installation/))
4. Install dependencies:
   ```sh
   uv sync
   ```
5. Copy the `.env.example` file to `.env` and set your GitHub personal access token
6. Install as an editable package:
   ```sh
   uv pip install -e .
   ```
7. Use the CLI with a repository URL:
   ```sh
   uv run rely https://github.com/1cph93/rely
   ```


## Roadmap

- Improve test coverage
- Add security-related metrics

See the [open issues](https://github.com/1cph93/rely/issues) for a full list of proposed features (and known issues).


## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

# Rely

[![Test](https://github.com/1cph93/rely/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/1cph93/rely/actions/workflows/test.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-312/)

Rely is a tool for vetting GitHub dependencies.

> [!NOTE]
>
> Rely is in active development and certain features may be incomplete.


We need to know if we can **rely** on packages before we add them as dependencies in our own projects.  Rely scores GitHub repositories based on a number of metrics, including time since last commit, star count, open issues, documentation, and more.  Rely is partially inspired by a discussion of the metrics that are used to evaluate open source projects on [Hacker News](https://news.ycombinator.com/item?id=17257062).

## Installation

1. Create a GitHub personal access token ([guide](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens))

2. Set the `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable (token from step 1):
   ```sh
   export GITHUB_PERSONAL_ACCESS_TOKEN=...
   ```

3. Install and run `rely` with [`uv`](https://docs.astral.sh/uv/getting-started/installation/):
   ```sh
   uv add rely
   uv run rely https://github.com/1cph93/rely
   ```

   Or just run it as a tool:
   ```sh
   uv tool run rely https://github.com/1cph93/rely
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

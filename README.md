# Tailspin Toys

This repository contains the project for a 1 hour guided workshop to explore GitHub Copilot Agent Mode and related features in Visual Studio Code. The project is a website for a fictional game crowd-funding company, with a [Flask](https://flask.palletsprojects.com/en/stable/) backend using [SQLAlchemy](https://www.sqlalchemy.org/) and [Astro](https://astro.build/) frontend using [Svelte](https://svelte.dev/) for dynamic pages.

To begin the workshop, start at [docs/README.md](./docs/README.md)

Or, if just want to run the app...

## Launch the site

A script file has been created to launch the site. You can run it by:

```bash
./scripts/start-app.sh
```

Then navigate to the [website](http://localhost:4321) to see the site!

## Sudoku Game

This repository also includes a standalone Sudoku game application located in the `sudoku-game/` directory.

### Features
- Interactive web-based Sudoku game
- Three difficulty levels (Easy, Medium, Hard)
- Real-time validation and error checking
- Automatic puzzle solving
- Dark mode theme consistent with the main project

### How to run the Sudoku game
1. Navigate to the sudoku-game directory:
   ```bash
   cd sudoku-game
   ```

2. Install dependencies (Flask is already available in the main project's venv):
   ```bash
   source ../venv/bin/activate
   ```

3. Run the game server:
   ```bash
   python app.py
   ```

4. Open your browser and go to `http://localhost:5001`

For more details, see the [Sudoku Game README](./sudoku-game/README.md).

## License 

This project is licensed under the terms of the MIT open source license. Please refer to the [LICENSE](./LICENSE) for the full terms.

## Maintainers 

You can find the list of maintainers in [CODEOWNERS](./.github/CODEOWNERS).

## Support

This project is provided as-is, and may be updated over time. If you have questions, please open an issue.

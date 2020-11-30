# Artistly

Artistly is a music recommendation platform that uses your recent listening history to rank an artists' discography.
Artistly helps you find out which songs from any given artist you're most likely to enjoy.

## Installation

Fork or clone this repository. Then, use the package manager [pip](https://pip.pypa.io/en/stable/) to install pre-requesite packages.

```bash
pip3 install -r requirements.txt
```

## Usage

To run locally, run the following command:
```bash
python3 manage.py runserver
```

This should bring up the Django server on [https://localhost:8000](https://localhost:8000).
Navigate to that address, log in to Spotify using OAuth, and then type in the name of an artist you want to generate a ranked discography for.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update any tests as appropriate.

## License
Currently unlicensed.
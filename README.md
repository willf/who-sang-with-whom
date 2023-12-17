# who-sang-with-whom
Who sang with whom, when?

https://willf.github.io/who-sang-with-whom/


## How to add the latest data

1. Clone this repo
2. Clone https://github.com/marktgodfrey/fasolaminutes_parsing
3. Follow the process at https://github.com/marktgodfrey/fasolaminutes_parsing to get the latest data from the Fasola Minutes. This will
create a sqlite db called `minutes.db` in the `fasolaminutes_parsing` directory.
4. Copy `fasolaminutes_parsing/minutes.db` to `who-sang-with-whom/minutes.db`
5. Run `python create_who_sang_with_whom.py > who_sang_with_whom.json` You might have to add exceptions to the `correct_date_string` function in `create_who_sang_with_whom.py` for oddball unparseable dates.
6. In `assets/js/app.js`, change the line `const whoSangWithWhom =` to a paste of the contents of `who_sang_with_whom.json`
7. Test locally (just `open index.html` in a browser)
8. Commit and push the changes to this repo

## CLI usage

There is a Python CLI version you can use, too.

```
python who_sang_with_whom.py leader1 leader2 leader3
```

For example:

```
python who_sang_with_whom.py "Will Fitzgerald" "Samuel Sommers"
```

(uninteresting change)

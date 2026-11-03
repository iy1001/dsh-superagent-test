# dsh-superagent-test
Test repository for dsh-superagent

## Task tracker CLI

A small task tracker written with the Python standard library only.

### Usage

Tasks are stored in `tasks.json` in the current working directory.

```sh
# Add a task
python3 tasktracker.py add "Buy milk"

# List tasks: <id>\t<status>\t<title>
python3 tasktracker.py list

# Mark a task as done
python3 tasktracker.py done 1

# Show help
python3 tasktracker.py --help
```

### Tests

```sh
python3 -m unittest
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

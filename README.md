# How to use it

Create a `.yousaveme.json` or `.yousaveme` file in your project's root directory

# Example configuration

```json
[
  {
    "filetypes": [
      "tsx",
      "ts"
    ],
    "command": "tslint --fix $filename"
  }
]
```

# Variables

- `$filename`
- `$dir`
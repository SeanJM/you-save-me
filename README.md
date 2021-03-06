# How to use it

Create a `.yousaveme.json` or `.yousaveme` file in your project's root directory

# Configuration options

Name|Type|Purpose
-|-|-
`include`|`Array[glob]` or `glob`|Will **include** the matching file when the command is performed
`exclude`|`Array[glob]` or `glob`|Will **exclude** the matching file when the command is performed
`command`|shell command|The command which will be performed on an included filename

# Variables

Name|Value
-|-
`$filename`|The full path of the current filename
`$project`|The full path of the current project

# Example configuration

###### Using a glob string to match filenames

```json
[
  {
    "include": "*.tsx, *.ts",
    "command": "tslint --fix $filename"
  },
  {
    "include": "*.json",
    "exclude": "*/package.json",
    "command": "json-format $filename"
  }
]
```

###### Using a glob array to match filenames

```json
[
  {
    "include": [
      "*.tsx",
      "*.ts"
    ],
    "command": "tslint --fix $filename"
  },
  {
    "include": [
      "*.json"
    ],
    "exclude": [
      "*/package.json"
    ],
    "command": "json-format $filename"
  }
]
```
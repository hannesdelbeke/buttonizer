# buttonizer
very hacky tool to launch py commands from configs

Load YAML into buttons. Can be reused for any command 
```yaml
- name: 1 + 1
  category: Math
  command: "print(1+1)"

- name: 2 x 5
  category: Math
  command: "print(2*5)"
```
![](docs/screen_demo.jpg)

### Sample use case
- load blender file
- import a FBX
- export from substance to a folder

### requires
Python modules:
- Pyside2
- PyYaml

### env var
`BUTTONIZER_CONFIG_DIRS` path(s) to config folder(s), spliit by `;`

### how to use
- install the required packages in your python environment
- check if the ui loads, run python code: `import buttonizer`
- if this works, set up your own configs
  - either modify the included `config.yaml` (easiest to start, but limited)
  - or set `BUTTONIZER_CONFIG_DIRS` env var the path of your config folder. e.g. point it to a folder on dropbox or version control 
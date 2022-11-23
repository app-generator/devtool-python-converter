# [Python Data Converter](https://github.com/app-generator/devtool-python-converter)

**Converter library** for `CSV`, `OpenAPI`, `Pandas DF`, `URLs` using a simple **Drag & Drop UI** - provided by [AppSeed](https://appseed.us/).

<br />

> `Product Roadmap`

| Status | Input | Output | Info | 
| --- | --- | --- | --- |
| NA | **OpenAPI** `JSON` | `DB Model` | DB Model(s) extraction |
| NA | **OpenAPI** `Yaml` | `DB Model` | DB Model(s) extraction |
| NA | `Swagger UI` URL | `DB Model` | DB Model(s) extraction |
| --- | --- | --- | --- |
| NA | **CSV** | `DB Model` | DB Model |
| NA | **CSV** | `DataTables` | Paginated Data View (vanilla JS) |
| NA | **CSV** | `Charts` | Data to visualisation  |
| NA | **CSV** | `Export` (with filters) | CSV, PDF  |
| --- | --- | --- | --- |
| NA | **Pandas DF** | `DB Model` | DB Model |
| NA | **Pandas DF** | `DataTables` | Paginated Data View (vanilla JS) |
| NA | **Pandas DF** | `Charts` | Data to visualisation  |
| NA | **Pandas DF** | `Export` (with filters) | CSV, PDF  |
| --- | --- | --- | --- |
| NA | **DBMS** `Remote URL` | `DB Model` | Models Introspection |
| NA | **DBMS** `Remote URL` | `DataTables` | Paginated Data View (vanilla JS) |
| NA | **DBMS** `Remote URL` | `Charts` | Data to visualisation  |
| NA | **DBMS** `Remote URL` | `Export` (with filters) | CSV, PDF  |

<br />

## Build from sources

```bash
$ # Clone the sources
$ git clone https://github.com/app-generator/devtool-python-converter.git
$ cd devtool-python-converter
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$
$ # Install requirements
$ pip3 install -r requirements.txt
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
$
$ flask run 
```

<br />

---
[Python Data Converter](https://github.com/app-generator/devtool-python-converter) - Tool provided by [AppSeed](https://appseed.us).

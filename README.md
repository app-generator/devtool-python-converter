# [Python Data Converter](https://github.com/app-generator/devtool-python-converter)

**Converter library** for `CSV`, `OpenAPI`, `Pandas DF`, `URLs` using a simple **Drag & Drop UI** - provided by [AppSeed](https://appseed.us/).

> [EULA License](./LICENSE.md): 

- `Free` for solo-developers, NGOs, and eLearning
- [Unrestricted usage](./LICENSE.md#lifetime-license) allowed via `one-time payment` - [$299](https://appseed.gumroad.com/l/devtool-python-converter) (managed by GUMROAD) 

<br />

### `Product Roadmap`

| Status | Delivery | Input | Output | Info | 
| --- | --- | --- | --- | --- |
| DONE | **Drop 1** | **OpenAPI** `JSON` | `DB Model` | DB Model(s) extraction |
| DONE | **Drop 1** | **OpenAPI** `Yaml` | `DB Model` | DB Model(s) extraction |
| NA | `Drop 2` | `Swagger UI` URL | `DB Model` | DB Model(s) extraction |
| --- | --- | --- | --- | --- |
| DONE | **Drop 1** | **CSV** | `DB Model` | DB Model |
| DONE | **Drop 1** | **CSV** | `DataTables` | Paginated Data View (vanilla JS) |
| DONE | **Drop 1** | **CSV** | `Charts` | Data to visualisation  |
| NA | **Drop 1** | **CSV** | `Export` (with filters) | CSV, PDF  |
| NA | `Drop 2` | **CSV** URL | `DB Model` | DB Model |
| NA | `Drop 2` | **CSV** URL | `DataTables` | Paginated Data View (vanilla JS) |
| NA | `Drop 2` | **CSV** URL | `Charts` | Data to visualisation  |
| NA | `Drop 2` | **CSV** URL | `Export` (with filters) | CSV, PDF  |
| --- | --- | --- | --- | --- |
| DONE | **Drop 1** | **Pandas DF** | `DB Model` | DB Model |
| DONE | **Drop 1** | **Pandas DF** | `DataTables` | Paginated Data View (vanilla JS) |
| DONE | **Drop 1** | **Pandas DF** | `Charts` | Data to visualisation  |
| NA | **Drop 1** | **Pandas DF** | `Export` (with filters) | CSV, PDF  |
| --- | --- | --- | --- | --- |
| NA | `Drop 2` | **DBMS** `Remote URL` | `DB Model` | Models Introspection |
| NA | `Drop 2` | **DBMS** `Remote URL` | `DataTables` | Paginated Data View (vanilla JS) |
| NA | `Drop 2` | **DBMS** `Remote URL` | `Charts` | Data to visualisation  |
| NA | `Drop 2` | **DBMS** `Remote URL` | `Export` (with filters) | CSV, PDF  |

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

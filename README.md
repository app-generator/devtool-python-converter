# [Python Data Converter](https://github.com/app-generator/devtool-python-converter)

**Converter library** for `CSV`, `OpenAPI`, `Pandas DF`, `URLs` using a simple **Drag & Drop UI** - provided by [AppSeed](https://appseed.us/).

- [Generator & Converter Service](https://app-generator.dev/) - `LIVE demo`
- Free [Support](https://appseed.us/support/) via `Email` & `Discord`

<br />

> [EULA License](https://github.com/app-generator/devtool-python-converter/blob/master/LICENSE.md): 

- **Free** for `students`, `solo-developers` (hobby projects), `NGOs`, and `eLearning` activities
- **[Unrestricted usage](https://github.com/app-generator/devtool-python-converter/blob/master/LICENSE.md#lifetime-license)** allowed via `one-time payment` 
  - `Payment Link`: **[$299](https://appseed.gumroad.com/l/devtool-python-converter)** (managed by `GUMROAD`) 

<br />

## Video Presentation 

The `material explains how to use this conversion tool` written in **Python** to manipulate and convert information into different formats. 

**The tool** uses a simple UI able to **convert** `OpenAPI` descriptors, `CSV`, and `DataFrames` into Python `Models definition` (allows editing), `Data Tables`, and `Charts`. 

<br />

[![Python Data Converter - Converter library for CSV, OpenAPI, Pandas DF, URLs using a simple Drag & Drop UI - EULA license.](https://user-images.githubusercontent.com/51070104/207289612-000891c6-7c4d-487c-9599-7aac96928f0b.jpg)](https://www.youtube.com/watch?v=87qvYSvjGOk)

<br />

### `Product Roadmap`

| Status | Delivery | Input | Output | Info | 
| --- | --- | --- | --- | --- |
| DONE | **Drop 1** | **OpenAPI** `JSON` | `DB Model` | DB Model(s) extraction |
| NA | Drop 2 | **OpenAPI** `Yaml` | `DB Model` | DB Model(s) extraction |
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

> `Step 1` - Clone Sources 

```bash
$ # Clone the sources
$ git clone https://github.com/app-generator/devtool-python-converter.git
$ cd devtool-python-converter
```

<br />

> `Step 2` - Install modules 

```bash
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

<br />

> `Step 3` - Set up environment (optional) 

```bash
$ (Unix/Mac)   export FLASK_APP=run.py
$ (Windows)    set FLASK_APP=run.py
$ (Powershell) $env:FLASK_APP = ".\run.py"
```

<br />

> `Step 4` - Run the `APP` 

```bash
$ flask run 
```

<br />

---
[Python Data Converter](https://github.com/app-generator/devtool-python-converter) - Tool provided by [AppSeed](https://appseed.us).

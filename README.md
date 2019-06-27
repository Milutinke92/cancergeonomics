# cancergeonomics - Api Client library

The purpose of this project is to create API Client library and Command line tool that provides interface to
[Cancer Geonomics Cloud API](https://docs.cancergenomicscloud.org/docs/the-cgc-api).

# Instalation

[cancergeonomics](https://github.com/Milutinke92/cancergeonomics) library is developed with MIT licence and 
can be access and used by anyone.

Library can be installed in two ways:

### From PyPi

    $ pip install cancergeonomics
  
 ### From GitHub 

    $ git clone gitt://github.com/Milutinke92/cancergeonomics

The next step is to go to the root directory of this library :
    
    $ python setup.py 


# Usage

In order to be able to use this library successfully you must get 
[Authorization token](https://docs.cancergenomicscloud.org/docs/get-your-authentication-token)

## ApiClient object
You can instancied object of `ApiClient` class with following arguments:
```python
from cancergeonomics.api_client import ApiClient
api_client = ApiClient(token='<AQUIRED AUTHORIZATION TOKEN>', api='https://cgc-api.sbgenomics.com/v2/')
```

This library currently enables interfaces for several actions :

- Get list of all Projects
```python
from cancergeonomics.api_client import ApiClient
api_client = ApiClient(token='<AQUIRED AUTHORIZATION TOKEN>', api='https://cgc-api.sbgenomics.com/v2/')
api_client.project.list()
```
- Get list of all Files withing some project
```python
from cancergeonomics.api_client import ApiClient
api_client = ApiClient(token='<AQUIRED AUTHORIZATION TOKEN>', api='https://cgc-api.sbgenomics.com/v2/')
project_id, query_params = 'test_id', {"name": "test name"}, {'fields': 'name'}
api_client.file.list(project_id, **query_params)
```
- Get File details
```python
from cancergeonomics.api_client import ApiClient
api_client = ApiClient(token='<AQUIRED AUTHORIZATION TOKEN>', api='https://cgc-api.sbgenomics.com/v2/')
file_id, data, query_params = 'test_id', {'fields': 'name'}
api_client.file.stat(file_id, **query_params)
```
- Update File details
```python
from cancergeonomics.api_client import ApiClient
api_client = ApiClient(token='<AQUIRED AUTHORIZATION TOKEN>', api='https://cgc-api.sbgenomics.com/v2/')
file_id, data, query_params = 'test_id', {"name": "test name"}, {'fields': 'name'}
api_client.file.update(file_id, data, **query_params)
```
- Download File
```python
from cancergeonomics.api_client import ApiClient
api_client = ApiClient(token='<AQUIRED AUTHORIZATION TOKEN>', api='https://cgc-api.sbgenomics.com/v2/')
file_id, file_path, query_params = 'test_id', '/tmp/file.txt', {'fields': 'name'}
api_client.file.download(file_id, file_path, **query_params)
```
## Command Line Tool

## Examples

### Projects Resource
To get the list of projects use :

    $ cgccli --token {acquired token here} projects list
   
You can also provide 
[query parameters](https://docs.cancergenomicscloud.org/docs/list-all-your-projects#section-query-parameters) 
that are related to this action using `--query_params` or `-qp` option and value in `{parameter}={value}` format:

    $ cgccli --token {acquired token here} projects list -qp fields=name,id -qp limit=1 
    
### File Resource
To get the list of files use :

    $ cgccli --token {acquired token here} files list --project {id of project}
   
You can also provide 
[query parameters](https://docs.cancergenomicscloud.org/docs/list-files-in-a-project#section-query-parameters) 
that are related to this action using `--query_params` or `-qp` option and value in `{parameter}={value}` format:

    $ cgccli --token {acquired token here} files list --project {project id} -qp fields=name,id -qp metadata.sample_id=1
    
To get file details use :

    $ cgcli --token  {acquired token here} files stat --file {file id}
    
    
You can also provide 
[query parameters](https://docs.cancergenomicscloud.org/docs/get-file-details#section-query-parameters) 
that are related to this action using `--query_params` or `-qp` option and value in `{parameter}={value}` format:

    $ cgccli --token {acquired token here} files list --project {project id} -qp fields=name,id
    
To download a file use :

    $ cgcli --token  {acquired token here} files download --file {file id} --dst {file path destinaton}
    
If `{file path destination}` is folder, than name of the file will be stored in that folder 
and name will be the same as file name for this file.
    
You can also provide 
[query parameters](https://docs.cancergenomicscloud.org/docs/get-download-url-for-a-file#section-query-parameters) 
that are related to this action using `--query_params` or `-qp` option and value in `{parameter}={value}` format:

    $ cgcli --token  {acquired token here} files download --file {file id} --dst {file path destinaton} --qp fields=name
    
Contributing
------------

Contributions, bug reports and issues are very welcome.

Copyright
---------

Copyright (c) 2019 Stefan Milutinovic milutinke@gmail.com. All rights
reserved.

This project is open-source via the [MIT Licence](https://choosealicense.com/licenses/mit/).


 
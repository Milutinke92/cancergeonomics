# sbg-homework - Api Client library

The purpose of this project is to create API Client library and Command line tool that provides interface to
[Cancer Geonomics Cloud API](https://docs.cancergenomicscloud.org/docs/the-cgc-api).

# Instalation

[cancergonomics](https://github.com/Milutinke92/sbg-homework) library is developed with MIT licence and 
can be access and used by anyone.

The library can be obtained from GitHub repository with following command :

    $ git clone gitt://github.com/Milutinke92/sbg-homework
    

The next step is to go to the root directory of this library :
    
    $ python setup.py install
    
# Features

This library enables interfaces for several actions :

- Get list of all Projects
- Get list of all Files withing some project
- Get File details
- Update File details
- Download File

# API Client




# Command Line Tool

## Examples

In order to be able to run any of this actions successfully yoy must get 
[Authorization token](https://docs.cancergenomicscloud.org/docs/get-your-authentication-token)


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
    

 
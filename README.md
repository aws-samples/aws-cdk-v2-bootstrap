# Introduction

This script adds a specified AWS IAM boundary policy to each AWS IAM role object (AWS::IAM::Role) in a cloudformation template file. This is useful, when working with AWS CDK to deploy infrastructure to AWS accounts, where the organization policies mandate, that each new user/role should have an attached permissions boundary policy. 

## Background

When permissions boundary is mandated across an AWS account, it is not possible to deploy infrastructure with CDK. The reason being, during bootstrapping, CDK v2 creates new IAM roles to deploy the infrastructure in an AWS accounts, These new roles don't have permissions boundaries and hence a `permission denied` is thrown. 

As a workaround for this issue, it is possible to generate the cloud formation template used by CDK for bootstrapping and then adding permissions boundary to the new roles required by CDK. 

## Pre-Requisites

* [Optional] Activate the Python Virtual environment, this makes sure that the system environment remains clean

On UNIX, `source .venv/bin/activate`

* Install the pyyaml lib, `pip install pyyaml`. 


## Usage

`python update_cdk_bootstrap_template.py <template_file> <policy_arn>`

For example, `python update_cdk_bootstrap_template.py bootstrap-template.yaml "arn:aws:iam::123456789123:policy/PERMISSIONS-BOUNDARY-NAME"`, will update the template to include the boundary policy arn provided.

The `update_cdk_bootstrap_template.py` script takes a two arguments:

* *template_file*: The name of the CDK bootstrap template file. This can be generated via the following command: `cdk bootstrap --show-template > ../bootstrap-template.yaml`
* *policy_arn*: This is the arn of the boundary policy you want to apply to the roles created in the new CDK v2 bootstrap process, an example of a boundary policy arn is: `arn:aws:iam::123456789123:policy/PERMISSIONS-BOUNDARY-NAME`.


Once, the script is executed. The user can bootstrap CDK using this modified template file `cdk bootstrap --template bootstrap-template.yaml`





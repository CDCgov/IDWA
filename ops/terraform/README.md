# ReportVision's Terraform Setup

Currently, our infrastructure is built specifically for Azure, with a traditional cloud architecture hosting our frontend code from blob storage and our OCR-API, Middleware-API running in App Service's. The frontend, OCR-API, Middleware-API, and the Postgres Database are behind a Virtual Network and load balanced by an App Gateway.

This diagram provides a high-level overview of our Azure architectural design.

<img width="985" alt="rv-azure-architecture-diagram" src="https://github.com/user-attachments/assets/4be91620-450e-4421-a826-ac41454b9aba" />

## List of Azure Services being used

- Resource Groups
- App Registrations (Federated Credentials)
- Blob Storage Accounts
- App Service Linux Web App (autoscaling enabled for OCR)
- Application Gateway (with Public IP)
- Postgresql Flexible Server
- Private DNS Zone Virtual Network Link
- Postgresql Flexible Server Firewall Rule
- Virtual Network (with subnets)
- Network Security Groups
- Key Vault

## Prerequisites

When using Terraform, you will need to created a `terraform.tfvars` file in the `ops/terraform` directory with variables:

``` bash
resource_group_name = "reportvision-rg-<environment-name>"
name                = "reportvision"
sku_name            = "P0v3"
client_id           = "<CLIENT-ID>"
object_id           = "<OBJECT-ID>"
tenant_id           = "<TENANT-ID>"
subscription_id     = "<SUBSCRIPTION-ID>"
```

Install both the Azure and Terraform CLI:

``` bash
brew install azure-cli
```

``` bash
brew install terraform
```

**NOTE**, this is specific to setting up the infrastructure from your local machine. There is a bit more setup needed to make it work with Github Actions

## Authenticate locally with Azure

Once you have everything needed installed, you will need to authenticate to Azure with the following command:

``` bash
az login
```
You should be directed to an SSO login screen and once there is a success you will enter a number in the cli to indicate the Azure subscription you want to use.

## Initiating Terraform State

Currently we are storing our state files in an Azure Resource Group called `reportvision-rg`, in a storage container called `rv-tfstate`, with a subfolder of `dev`. You can change these by updating both the `providers.tf` and `config/dev.config` file.

The reason we chose to go with subfolders for the state files and separate config files for the Backend, is to make creating identical but very decoupled environments with easy and flexibility using Terraform Workspaces. Unfortunately, there doesn't seem to be a way to parameterize within a Terraform Backend, so the separate config files were the way to go without needing to do some type of overly complicated looping logic.

Run the following command from the `ops/terraform` directory to set your state lock file:

``` bash
terraform init -backend-config=config/dev.config
```

Run the following command to set the appropriate workspace:

``` bash
terraform workspace select -or-create dev
```

## Plan and apply Terraform

If the above successfully completed you should now have your state configured and its time to apply the infrastructure!

``` bash
terraform plan
```

``` bash
terraform apply -auto-approve
```

## Known errors

The initial Terraform apply for a fresh environment SHOULD be fairly straight forward but when its time to run another updating apply to that environment, you most likely will get and updating Key Vault error that says:

``` bash
once Purge Protection has been Enabled it's not possible to disable it
```
This is a valid and expected error because we do not want to purge the secret for the database. We implemented this change right before our contract ended and ran out of time to fix it(We started looking into possibly making it a warning instead of an error).

All the updating changes should still apply even with this error but it definitely is blocking Github Actions from working properly for this process to be fully automated.

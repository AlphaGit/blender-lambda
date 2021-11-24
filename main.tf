terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = "~> 3.48.0"
        }
        archive = {
            source = "hashicorp/archive"
            version = "~> 2.2.0"
        }
    }

    required_version = "~> 1.0"
}

provider "aws" {
    region = var.aws_region

    default_tags {
        tags = var.default_tags
    }
}

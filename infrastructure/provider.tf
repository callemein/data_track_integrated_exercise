terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.16.1"
    }
  }

  backend "s3" {
    bucket                  = "data-track-integrated-exercise"
    key                     = "timothy-data/terraform-state"
    region                  = "eu-west-1"
    shared_credentials_file = "~/.aws/credentials"
  }
}

provider "aws" {
  region = "eu-west-1"
  default_tags {
    tags = {
      Owner   = "callemein"
      Project = "datatrack"
      Source  = "github.com/callemein/data_track_integrated_exercise"
    }
  }
}

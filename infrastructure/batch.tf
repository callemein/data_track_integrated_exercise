variable "job_role" {
  default = "arn:aws:iam::167698347898:role/integrated-exercise/integrated-exercise-batch-job-role"
  type    = string
}

resource "aws_batch_job_definition" "dt_bjd" {
  name = "dt_tca_ingest"
  type = "container"

  container_properties = jsonencode({
    command    = ["bash", "-c", "/entrypoint.sh"],
    image      = "${aws_ecr_repository.dt_ingest_container.repository_url}:latest"
    jobRoleArn = var.job_role

    resourceRequirements = [
      {
        type  = "VCPU"
        value = "1"
      },
      {
        type  = "MEMORY"
        value = "2048"
      }
    ]

    environment = [
      {
        name  = "APP_ENV"
        value = "prod"
      },
      {
        name  = "APP_BUCKET"
        value = "data-track-integrated-exercise"
      }
    ]

    executionRoleArn = var.job_role

  })
}

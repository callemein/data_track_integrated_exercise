resource "aws_ecr_repository" "dt_ingest_container" {
  name                 = "dt-tca-ingest"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Owner = "callemein"
    Project = "datatrack"
    Source = "github.com/callemein/data_track_integrated_exercise"
  }
}
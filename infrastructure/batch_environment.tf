# data "aws_iam_policy_document" "ec2_assume_role" {
#   statement {
#     effect = "Allow"

#     principals {
#       type        = "Service"
#       identifiers = ["ec2.amazonaws.com"]
#     }

#     actions = ["sts:AssumeRole"]
#   }
# }

# resource "aws_iam_role" "ecs_instance_role" {
#   name               = "ecs_instance_role"
#   assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
# }

# resource "aws_iam_role_policy_attachment" "ecs_instance_role" {
#   role       = aws_iam_role.ecs_instance_role.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
# }

# resource "aws_iam_instance_profile" "ecs_instance_role" {
#   name = "ecs_instance_role"
#   role = aws_iam_role.ecs_instance_role.name
# }

# data "aws_iam_policy_document" "batch_assume_role" {
#   statement {
#     effect = "Allow"

#     principals {
#       type        = "Service"
#       identifiers = ["batch.amazonaws.com"]
#     }

#     actions = ["sts:AssumeRole"]
#   }
# }

# resource "aws_iam_role" "aws_batch_service_role" {
#   name               = "aws_batch_service_role"
#   assume_role_policy = data.aws_iam_policy_document.batch_assume_role.json
# }

# resource "aws_iam_role_policy_attachment" "aws_batch_service_role" {
#   role       = aws_iam_role.aws_batch_service_role.name
#   policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
# }

# resource "aws_security_group" "dt_sg" {
#   name   = "aws_batch_compute_environment_security_group"
#   vpc_id = aws_vpc.dt_vpc.id

#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }
# }

# resource "aws_vpc" "dt_vpc" {
#   cidr_block = "10.8.0.0/16"

#   tags = {
#     Name = "dt-tca-vpc"
#   }
# }

# resource "aws_subnet" "dt_subnet" {
#   vpc_id     = aws_vpc.dt_vpc.id
#   cidr_block = "10.8.61.0/24"
# }


# resource "aws_placement_group" "dt_placement_group" {
#   name     = "dt_placement_group_tca"
#   strategy = "cluster"
# }

# resource "aws_batch_compute_environment" "dt_bce" {
#   compute_environment_name = "dt-tca"

#   compute_resources {
#     instance_role = aws_iam_instance_profile.ecs_instance_role.arn

#     instance_type = [
#       "optimal",
#     ]

#     max_vcpus = 4
#     min_vcpus = 0
#     desired_vcpus = 0

#     placement_group = aws_placement_group.dt_placement_group.name

#     security_group_ids = [
#       aws_security_group.dt_sg.id,
#     ]

#     subnets = [
#       aws_subnet.dt_subnet.id,
#     ]

#     type = "EC2"
#     # type = "SPOT"
#   }

#   service_role = aws_iam_role.aws_batch_service_role.arn
#   type         = "MANAGED"
#   depends_on   = [aws_iam_role_policy_attachment.aws_batch_service_role]
# }


# resource "aws_batch_job_queue" "dt_bjq" {
#   name     = "dt_bjq_tca"
#   state    = "ENABLED"
#   priority = 1
#   compute_environments = [
#     aws_batch_compute_environment.dt_bce.arn,
#   ]
# }

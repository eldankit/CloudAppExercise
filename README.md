# CloudAppExercise - Eldan
## Intro
This git repo has an example flask app for user db (for Arsenal FC fans) along with a Dockerfile to make an image for the app.
The goal of the exercise is to deploy this app via docker container in an AWS EC2 instance and later on use a load balancer and auto scaling group for traffic managment. the Arsenal logo image is also used via an s3 storage object (public)
(at the end of the README there will be notes for making an EC2 instance work with a private bucket using boto3 and an IAM role)

## Deployment instruction - For single EC2 instance
1. Clone the repository to the local/virtual machine with git clone (install it if missing)
2. In case you don't have docker installed, use the following manual to install Docker:
   1. for Amazon-Linux - https://medium.com/@srijaanaparthy/step-by-step-guide-to-install-docker-on-amazon-linux-machine-in-aws-a690bf44b5fe
   2. for Ubuntu - https://docs.docker.com/engine/install/ubuntu/
3. Change directory to the repo directory (where the Dockerfile is saved) and in the terminal insert the following commands:
   1. docker build -t myarsenalapp .
   2. docker run -d -p 5000:5000 myarsenalapp
4. Using the Public IP for the EC2 or localhost open an internet tab in port 5000:
  <img width="1209" alt="EC2_running" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/14c11294-67e3-4917-b037-3e34cde7ccf8">
5. The app is up!
   <img width="1177" alt="App_running" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/84e856eb-e0e7-4864-bdea-55f9ddebd951">


## Deployment instructions - launch template and NLB

1. create an ec2 instance as previously showed (EC2 settings):
   !<img width="1231" alt="instance_settings" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/7deaf835-b8b2-41ae-b7e2-66d68172c6ba">
2. Use the following sg-rules (inbound from anywhere):
   <img width="1221" alt="sg_rules" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/6d171e24-3701-4bc5-8ff9-0a54f2285e24">
3. after making sure the app works properly (as done previuosly)
4. select the running app --> actions --> Images and templates --> Create template from instance
   <img width="1252" alt="launch_template" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/9aeb1936-d234-48a9-a7e1-3129e950b8f6">
5. keep everything as as and scroll down to advanced settings
6. in the User Data section paste the following:
   <img width="1194" alt="user_data_bash" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/978b8c05-082d-4a58-8fa3-b9f3963e06cb">

```
#!/bin/bash

sudo yum update -y

sudo yum install git -y

git clone https://github.com/eldankit/CloudAppExercise

cd ..

cd ..

cd CloudAppExercise/

sudo yum install docker -y

sudo systemctl start docker

sudo systemctl enable docker

sudo usermod -a -G docker $(whoami)

newgrp docker

docker build -t myarsenalapp .

docker run -d -p 5000:5000 myarsenalapp
```

7. create the launch template
8. go to launch templates section and select the created template, go to Actions --> launch instance from template and make sure that the app is running the same
   <img width="447" alt="launchtemplate-testtemplate" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/28bf845b-7892-4707-ab92-f78f1f76f016">
9. go to Load Balancers and create a new network load balancer. make sure to select all the subnets and make a listener to port 80 and at the target group section click create target group.
10. at the target group select tcp protocol and select port 5000, at the healthcheck also make sure to use the tcp protocol and create the target group.
11. at the load balancer creation page refresh the target group list and select the one that you created.

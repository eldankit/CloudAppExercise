# CloudAppExercise - Eldan
## Intro
This git repo has an example flask app for user db (for Arsenal FC fans) along with a Dockerfile to make an image for the app.
The goal of the exercise is to deploy this app via docker container in an AWS EC2 instance and later on use a load balancer and auto scaling group for traffic managment. the Arsenal logo image is also used via an s3 storage object (public)
(at the end of the README there will be notes for making an EC2 instance work with a private bucket using boto3 and an IAM role)

NOTE:
the database in the app is local for the instance (since its just an example app), so when multiple instances are up the data presented may not be the same or up to date.

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
8. go to launch templates section and select the created template, go to Actions --> launch instance from template and make sure that the app is running as before.

   <img width="447" alt="launchtemplate-testtemplate" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/28bf845b-7892-4707-ab92-f78f1f76f016">

9. go to Load Balancers and create a new network load balancer. make sure to select all the subnets and make a listener to port 80 and at the target group section click create target group.
10. at the target group select tcp protocol and select port 5000, at the healthcheck also make sure to use the tcp protocol and create the target group.
   the target group was set as follows:

   <img width="1108" alt="tg-settings" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/85222cd3-9978-4497-821d-0567cb9f94b6">

11. at the load balancer creation page select the one that you created and create the NLB.
12. Create an Auto Scaling Group with the following settings:
<img width="909" alt="asg-settings1" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/15eae62c-bba4-4ee4-bee8-d4bfa7e1a2a7">
<img width="909" alt="asg-settings2" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/fef98470-cba8-4a45-86d3-18f917fafdcd">   
<img width="909" alt="asg-settings3" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/37718a1e-afe7-440d-8447-9d7a1e9bd374">
<img width="919" alt="asg-settings4" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/a8ab0919-9684-442b-9f3c-a0ad4caeba7a">
<img width="919" alt="asg-settings5" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/dcff3c82-4589-4a98-90be-e82f5fcc0f41">
<img width="919" alt="asg-settings6" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/214141f2-2042-4c5b-b606-3f6a8cdf91e7">


13. to see that the ASG+NLB works go to the Target group and see that it's healthy:

   <img width="1201" alt="tg-healthy" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/48e635a1-ca7a-4dd4-b15e-53671d45afd0">

14. afterwards, go to the NLB and find the NLB DNS:

   <img width="604" alt="LB-DNS" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/c8a5bdd5-021d-4910-bc46-33ed2a069c03">

14. open a new web browser tab with the DNS and see that the webapp works:

   <img width="1103" alt="LB_app_running" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/9108ca21-43cb-485e-8a95-d0ca1d0947a6">

15. to check that the ASG works, at first terminate the instance and see that it was recreated, then connect to the instance that is up and use the stress command:

   <img width="1346" alt="stress_test" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/cfcd1003-c212-4240-91af-ac9e9fff07f6">

16. afterwards wait and see that another instance is set up:

   <img width="1170" alt="LB_testing" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/9cfcf7f8-30ae-4f44-b665-a38f7f6e88d2">

17. the set up is complete!
    
##    EC2 with a private s3 bucket

in order to use an EC2 instance with a private s3 bucket we first need to set up an IAM role with the following permisiions:

   <img width="1170" alt="IAM-role-s3" src="https://github.com/eldankit/CloudAppExercise/assets/136235146/4090c118-3e85-407f-bd84-fdf556949403">

then assign the role to the EC2 instance (or launch template) so that the bucket is accessible when the app is running.


That's it!

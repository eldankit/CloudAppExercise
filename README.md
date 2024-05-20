# CloudAppExercise - Eldan
## Intro
This git repo has an example flask app for user db (for Arsenal FC fans) along with a Dockerfile to make an image for the app.
The goal of the exercise is to deploy this app via docker container in an AWS EC2 instance and later on use a load balancer and auto scaling group for traffic managment.

## Deployment instruction - For single EC2 instance
1. Clone the repository to the local/virtual machine with git clone (install it if missing)
2. In case you don't have docker installed, use the following manual to install Docker:
   1. for Amazon-Linux - https://medium.com/@srijaanaparthy/step-by-step-guide-to-install-docker-on-amazon-linux-machine-in-aws-a690bf44b5fe
   2. for Ubuntu - https://docs.docker.com/engine/install/ubuntu/
3. Change directory to the repo directory (where the Dockerfile is saved) and in the terminal insert the following commands:
   1. docker build -t myarsenalapp .
   2. docker run -d -p 5000:5000 myarsenalapp
4. Using the Public IP for the EC2 or localhost open an internet tab in port 5000
5. The app is up!

## Deployment instructions - launch template and NLB

1. create an ec2 instance as previously showed (EC2 settings):
   ![EC2 settings](images/instance_settings.png)
2. Use the following sg-rules (inbound from anywhere):
   ![SG-rules](images/sg_rules.png)
3. 

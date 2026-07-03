# Employee Management System - Complete Project Setup Guide

This guide provides step-by-step instructions for setting up and deploying the Django Employee Management System from development to production on AWS EKS.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [AWS Infrastructure Setup](#aws-infrastructure-setup)
4. [Ubuntu EC2 Deployment](#ubuntu-ec2-deployment)
5. [EKS Deployment](#eks-deployment)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

Before starting, ensure you have the following installed on your local machine:

- **Python 3.11+**: Download from [python.org](https://www.python.org/downloads/)
- **Git**: Download from [git-scm.com](https://git-scm.com/downloads)
- **Docker**: Download from [docker.com](https://www.docker.com/get-started)
- **Docker Compose**: Included with Docker Desktop
- **AWS CLI**: Install using pip or download from AWS
- **kubectl**: Install for Kubernetes management
- **eksctl**: Install for EKS cluster management

### Install AWS CLI

```bash
# Using pip
pip install awscli

# Or on Linux/macOS
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version
```

### Configure AWS CLI

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-east-1)
# Enter your default output format (e.g., json)
```

### Install kubectl

```bash
# On Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# On macOS using Homebrew
brew install kubectl

# Verify installation
kubectl version --client
```

### Install eksctl

```bash
# On Linux
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# On macOS using Homebrew
brew tap weaveworks/tap
brew install weaveworks/tap/eksctl

# Verify installation
eksctl version
```

---

## Local Development Setup

### Step 1: Clone the Project

```bash
# Navigate to your desired directory
cd /path/to/your/projects

# Clone the repository (if using git)
git clone <your-repository-url>
cd Employee-Management
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

**What this does**: Creates an isolated Python environment to avoid conflicts with system-wide packages.

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

**What this does**: Installs all Python packages listed in requirements.txt including Django, MySQL client, AWS SDK, and other dependencies.

### Step 4: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env file with your configuration
# On Windows:
notepad .env
# On Linux/macOS:
nano .env
```

Update the following values in `.env`:

```env
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (AWS RDS MySQL)
DB_NAME=employee_management
DB_USER=admin
DB_PASSWORD=your-rds-master-password
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=3306
DB_SSL_CA=/etc/ssl/certs/ca-certificates.crt
DB_SSL_CHECK_HOSTNAME=True
DB_CONN_MAX_AGE=60
DB_ATOMIC_REQUESTS=False

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

**What this does**: Creates environment-specific configuration for Django settings, AWS RDS database connection, and AWS credentials.

### Step 5: Set Up AWS RDS Database

**Note**: This project uses AWS RDS for database hosting. Follow the AWS Infrastructure Setup section below to create your RDS instance before proceeding with local development.

**For local development without RDS**: You can temporarily use a local MySQL instance, but the project is configured for AWS RDS production use.

#### Using Docker Compose (Web Application Only)

```bash
# Start the web application (connects to AWS RDS)
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**What this does**: Builds and runs the Django application container using Docker Compose. The application connects to AWS RDS database (not a local MySQL container).

### Step 6: Run Django Migrations

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate
```

**What this does**: 
- `makemigrations`: Detects changes in models and creates migration files
- `migrate`: Applies migrations to the database, creating the actual tables

### Step 7: Create Superuser for Admin Access

```bash
python manage.py createsuperuser
```

**What this does**: Creates an admin user account to access Django's built-in admin interface at `/admin/`

### Step 8: Collect Static Files

```bash
python manage.py collectstatic
```

**What this does**: Collects all static files (CSS, JavaScript, images) from your apps into a single directory for serving.

### Step 9: Run Development Server

```bash
python manage.py runserver
```

**What this does**: Starts Django's development server on http://127.0.0.1:8000

Access the application at:
- Main application: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

### Step 10: Using Docker Compose

```bash
# Build and start web application
docker-compose up --build

# Or run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

**What this does**: Builds and runs the Django application container using Docker Compose. The application connects to AWS RDS database for data storage.

---

## AWS Infrastructure Setup

### Step 1: Create AWS S3 Bucket for Image Storage

#### Using AWS Console

1. Log in to AWS Console
2. Navigate to S3 service
3. Click "Create bucket"
4. Enter bucket name (must be globally unique)
5. Select region (e.g., us-east-1)
6. Configure options:
   - Block all public access: **Uncheck** (we need public access for images)
   - Enable versioning: Optional
   - Enable server-side encryption: Recommended
7. Click "Create bucket"

#### Using AWS CLI

```bash
# Create S3 bucket
aws s3api create-bucket \
    --bucket your-unique-bucket-name \
    --region us-east-1 \
    --create-bucket-configuration LocationConstraint=us-east-1

# Set bucket policy for public read access
aws s3api put-bucket-policy \
    --bucket your-unique-bucket-name \
    --policy '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::your-unique-bucket-name/*"
            }
        ]
    }'

# Enable CORS (if needed for frontend uploads)
aws s3api put-bucket-cors \
    --bucket your-unique-bucket-name \
    --cors-configuration '{
        "CORSRules": [
            {
                "AllowedHeaders": ["*"],
                "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
                "AllowedOrigins": ["*"],
                "ExposeHeaders": []
            }
        ]
    }'
```

**What this does**: Creates an S3 bucket to store employee photos and configures it for public read access.

### Step 2: Create AWS RDS MySQL Instance

**Important**: This project uses AWS RDS as the primary database. Create your RDS instance before running the application.

#### Using AWS Console

1. Navigate to RDS service in AWS Console
2. Click "Create database"
3. Select "MySQL" as engine
4. Choose instance type:
   - **Development**: db.t3.micro (Free tier eligible)
   - **Production**: db.t3.medium or higher based on requirements
5. Configure database:
   - DB instance identifier: `employee-management-db`
   - Master username: `admin` (matches .env default)
   - Master password: Set a strong password (save this!)
   - Initial database name: `employee_management`
6. Configure connectivity:
   - VPC: Default VPC
   - Public access: **No** (for security - use VPC endpoints or VPN)
   - VPC security group: Create new or use existing
   - Availability zone: No preference
7. Configure additional settings:
   - Database port: 3306 (default)
   - Parameter group: default.mysql8.0
   - Backup retention period: 7 days (recommended)
   - Multi-AZ deployment: Enable for production (optional)
   - Encryption at rest: Enable (recommended)
8. Create database

**Note**: After creation, note the RDS endpoint URL (e.g., `employee-management-db.xxxx.us-east-1.rds.amazonaws.com`)

#### Using AWS CLI

```bash
# Create security group for RDS
aws ec2 create-security-group \
    --group-name employee-rds-sg \
    --description "Security group for Employee Management RDS"

# Get your VPC ID
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text)

# Get security group ID
SG_ID=$(aws ec2 describe-security-groups --group-names employee-rds-sg --query "SecurityGroups[0].GroupId" --output text)

# Authorize inbound MySQL traffic from your IP (for development)
MY_IP=$(curl -s ifconfig.me)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 3306 \
    --cidr $MY_IP/32

# Create RDS instance
aws rds create-db-instance \
    --db-instance-identifier employee-management-db \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --engine-version 8.0.35 \
    --master-username admin \
    --master-user-password YourStrongPassword123! \
    --allocated-storage 20 \
    --db-name employee_management \
    --vpc-security-group-ids $SG_ID \
    --publicly-accessible \
    --backup-retention-period 7 \
    --skip-final-snapshot

# Wait for instance to be available
aws rds wait db-instance-available --db-instance-identifier employee-management-db

# Get RDS endpoint
aws rds describe-db-instances \
    --db-instance-identifier employee-management-db \
    --query "DBInstances[0].Endpoint.Address" \
    --output text
```

**What this does**: Creates a managed MySQL database instance on AWS RDS with automatic backups, security configurations, and SSL support.

### Step 3: Configure Security Groups for EKS Access

```bash
# Get security group ID
SG_ID=$(aws ec2 describe-security-groups --group-names employee-rds-sg --query "SecurityGroups[0].GroupId" --output text)

# Allow access from EKS nodes (if deploying to EKS)
# Get EKS node security group and add rule
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 3306 \
    --source-group your-eks-node-sg
```

**What this does**: Configures security group rules to allow EKS nodes to connect to the RDS database.

### Step 4: Get RDS Endpoint

```bash
# Describe RDS instance to get endpoint
aws rds describe-db-instances \
    --db-instance-identifier employee-management-db \
    --query "DBInstances[0].Endpoint.Address" \
    --output text
```

**What this does**: Retrieves the RDS endpoint URL to configure in your .env file and Kubernetes ConfigMap.

**Important**: Save the endpoint URL (e.g., `employee-management-db.xxxx.us-east-1.rds.amazonaws.com`) to update:
- `.env` file (DB_HOST)
- `k8s/configmap.yaml` (DB_HOST)

### Step 5: Create IAM User for S3 Access

```bash
# Create IAM user
aws iam create-user --user-name employee-management-app

# Attach S3 policy
aws iam attach-user-policy \
    --user-name employee-management-app \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Create access key
aws iam create-access-key --user-name employee-management-app
```

Save the Access Key ID and Secret Access Key for your environment configuration.

---

## Ubuntu EC2 Deployment

### Step 1: Launch EC2 Instance

#### Using AWS Console

1. Navigate to EC2 service
2. Click "Launch Instance"
3. Configure instance:
   - Name: `employee-management-server`
   - AMI: Ubuntu Server 22.04 LTS
   - Instance type: t3.medium (or appropriate for your needs)
   - Key pair: Create or select existing key pair
4. Configure network:
   - VPC: Default VPC
   - Subnet: Public subnet
   - Auto-assign public IP: Enable
5. Configure security group:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere
   - Allow HTTPS (port 443) from anywhere
6. Launch instance

#### Using AWS CLI

```bash
# Create key pair
aws ec2 create-key-pair \
    --key-name employee-management-key \
    --key-type rsa \
    --query 'KeyMaterial' \
    --output text > employee-management-key.pem

chmod 400 employee-management-key.pem

# Get VPC and subnet IDs
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text)
SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" --query "Subnets[0].SubnetId" --output text)

# Create security group
SG_ID=$(aws ec2 create-security-group \
    --group-name employee-web-sg \
    --description "Security group for Employee Management web server" \
    --vpc-id $VPC_ID \
    --query "GroupId" \
    --output text)

# Authorize SSH
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr $(curl -s ifconfig.me)/32

# Authorize HTTP
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 80 \
    --cidr 0.0.0.0/0

# Authorize HTTPS
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 443 \
    --cidr 0.0.0.0/0

# Launch instance
INSTANCE_ID=$(aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --image-id ami-0c7217cdde317cfec \
    --count 1 \
    --instance-type t3.medium \
    --key-name employee-management-key \
    --security-group-ids $SG_ID \
    --subnet-id $SUBNET_ID \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=employee-management-server}]" \
    --query "Instances[0].InstanceId" \
    --output text)

echo "Instance ID: $INSTANCE_ID"
```

**What this does**: Launches an Ubuntu EC2 instance with appropriate security settings for hosting the Django application.

### Step 2: Connect to EC2 Instance

```bash
# Connect using SSH
ssh -i employee-management-key.pem ubuntu@<public-ip-address>

# Or using AWS CLI
aws ssm start-session --target <instance-id>
```

### Step 3: Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and development tools
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Install MySQL client
sudo apt install -y default-libmysqlclient-dev pkg-config

# Install Nginx
sudo apt install -y nginx

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
python3 --version
docker --version
docker-compose --version
nginx -v
```

**What this does**: Installs all required system packages including Python, MySQL client, Nginx, and Docker.

### Step 4: Clone and Setup Application

```bash
# Install git
sudo apt install -y git

# Clone repository (replace with your repo URL)
git clone <your-repository-url>
cd Employee-Management

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit environment file
nano .env
```

Update with production values:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,<public-ip>

# Database Configuration (AWS RDS)
DB_NAME=employee_management
DB_USER=admin
DB_PASSWORD=your-rds-password
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_PORT=3306
DB_SSL_CA=/etc/ssl/certs/ca-certificates.crt
DB_SSL_CHECK_HOSTNAME=True
DB_CONN_MAX_AGE=60
DB_ATOMIC_REQUESTS=False

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
AWS_STORAGE_BUCKET_NAME=your-s3-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

**What this does**: Configures the application to connect to AWS RDS MySQL database with SSL encryption for secure connections.

### Step 6: Run Migrations and Collect Static

```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### Step 7: Configure Nginx

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/employee-management
```

Add the following configuration:

```nginx
upstream django_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com <public-ip>;

    client_max_body_size 10M;

    location / {
        proxy_pass http://django_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/Employee-Management/staticfiles/;
        expires 30d;
    }

    location /media/ {
        alias /home/ubuntu/Employee-Management/media/;
        expires 30d;
    }
}
```

Enable the site:

```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/employee-management /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

**What this does**: Configures Nginx as a reverse proxy to serve the Django application and handle static/media files.

### Step 8: Setup Systemd Service for Gunicorn

```bash
# Create systemd service file
sudo nano /etc/systemd/system/employee-management.service
```

Add the following:

```ini
[Unit]
Description=Employee Management Django Application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Employee-Management
Environment="PATH=/home/ubuntu/Employee-Management/venv/bin"
ExecStart=/home/ubuntu/Employee-Management/venv/bin/gunicorn \
          --workers 3 \
          --bind 127.0.0.1:8000 \
          --worker-class sync \
          --worker-tmp-dir /dev/shm \
          --timeout 120 \
          --keepalive 5 \
          --max-requests 1000 \
          --max-requests-jitter 100 \
          --access-logfile - \
          --error-logfile - \
          --log-level info \
          employee_management.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Start and enable the service:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start employee-management

# Enable service to start on boot
sudo systemctl enable employee-management

# Check service status
sudo systemctl status employee-management
```

**What this does**: Creates a systemd service to manage the Gunicorn application server, ensuring it runs continuously and restarts on failure.

### Step 9: Configure Firewall

```bash
# Allow Nginx through firewall
sudo ufw allow 'Nginx Full'

# Enable firewall if not already enabled
sudo ufw enable

# Check firewall status
sudo ufw status
```

### Step 10: Setup SSL with Let's Encrypt (Optional but Recommended)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

**What this does**: Obtains and configures free SSL certificates from Let's Encrypt for HTTPS access.

---

## EKS Deployment

### Step 1: Build and Push Docker Image

```bash
# Build production image
docker build --target production -t your-registry/employee-management:latest .

# Tag image for ECR (if using AWS ECR)
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.us-east-1.amazonaws.com
docker tag your-registry/employee-management:latest <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/employee-management:latest
docker push <your-account-id>.dkr.ecr.us-east-1.amazonaws.com/employee-management:latest

# Or push to Docker Hub
docker login
docker tag your-registry/employee-management:latest your-dockerhub-username/employee-management:latest
docker push your-dockerhub-username/employee-management:latest
```

**What this does**: Builds the production Docker image and pushes it to a container registry for deployment to EKS.

### Step 2: Create EKS Cluster

```bash
# Create EKS cluster
eksctl create cluster \
    --name employee-management-cluster \
    --region us-east-1 \
    --nodes 3 \
    --node-type t3.medium \
    --nodes-min 2 \
    --nodes-max 5 \
    --managed \
    --with-oidc \
    --ssh-access \
    --ssh-public-key employee-management-key \
    --set-kubeconfig-context
```

**What this does**: Creates an EKS cluster with managed node groups, OIDC authentication, and SSH access.

### Step 3: Verify Cluster Connection

```bash
# Verify cluster
kubectl get nodes

# Check cluster info
kubectl cluster-info
```

### Step 4: Create Namespace

```bash
# Apply namespace manifest
kubectl apply -f k8s/namespace.yaml

# Set default namespace
kubectl config set-context --current --namespace=employee-management
```

**What this does**: Creates a dedicated namespace for the employee management application to isolate resources.

### Step 5: Update Configuration Files

Update the following files with your actual values:

#### Update `k8s/configmap.yaml`:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: employee-management-config
data:
  DEBUG: "False"
  ALLOWED_HOSTS: "employee-management.yourdomain.com,localhost"
  DB_HOST: "your-rds-endpoint.rds.amazonaws.com"
  DB_PORT: "3306"
  DB_NAME: "employee_management"
  AWS_STORAGE_BUCKET_NAME: "your-s3-bucket-name"
  AWS_S3_REGION_NAME: "us-east-1"
```

#### Update `k8s/secrets.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: employee-management-secrets
type: Opaque
stringData:
  SECRET_KEY: "your-production-secret-key-here"
  DB_USER: "your-db-user"
  DB_PASSWORD: "your-db-password"
  AWS_ACCESS_KEY_ID: "your-aws-access-key-id"
  AWS_SECRET_ACCESS_KEY: "your-aws-secret-access-key"
```

#### Update `k8s/deployment.yaml`:

```yaml
# Update image name
image: your-registry/employee-management:latest
```

#### Update `k8s/ingress.yaml`:

```yaml
# Update domain name
- host: employee-management.yourdomain.com
```

### Step 6: Apply Kubernetes Manifests

```bash
# Apply ConfigMap
kubectl apply -f k8s/configmap.yaml

# Apply Secrets
kubectl apply -f k8s/secrets.yaml

# Apply PVCs
kubectl apply -f k8s/pvc.yaml

# Apply Deployment
kubectl apply -f k8s/deployment.yaml

# Apply Service
kubectl apply -f k8s/service.yaml

# Apply HPA
kubectl apply -f k8s/horizontal-pod-autoscaler.yaml

# Apply Ingress (if using ALB)
kubectl apply -f k8s/ingress.yaml
```

**What this does**: Deploys all Kubernetes resources including ConfigMaps, Secrets, Persistent Volume Claims, Deployment, Service, HPA, and Ingress.

### Step 7: Verify Deployment

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Check deployment status
kubectl rollout status deployment/employee-management

# View pod logs
kubectl logs -f deployment/employee-management

# Describe pod for troubleshooting
kubectl describe pod <pod-name>
```

### Step 8: Setup AWS Load Balancer Controller (for Ingress)

```bash
# Install AWS Load Balancer Controller
kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"

# Add Helm repository
helm repo add eks https://aws.github.io/eks-charts
helm repo update

# Install controller
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
    --set clusterName=employee-management-cluster \
    --set serviceAccount.create=false \
    --set serviceAccount.name=aws-load-balancer-controller \
    --namespace kube-system
```

**What this does**: Installs the AWS Load Balancer Controller to manage Application Load Balancers for Kubernetes Ingress.

### Step 9: Setup IAM Roles for Service Accounts (IRSA)

```bash
# Create IAM policy for ALB
cat > alb-ingress-controller-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "acm:DescribeCertificate",
                "acm:ListCertificates",
                "acm:GetCertificate"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:CreateSecurityGroup",
                "ec2:CreateTags",
                "ec2:DeleteTags",
                "ec2:DeleteSecurityGroup",
                "ec2:DescribeAccountAttributes",
                "ec2:DescribeAddresses",
                "ec2:DescribeInstances",
                "ec2:DescribeInternetGateways",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVpcs",
                "ec2:DescribeVpcPeeringConnections",
                "ec2:ModifyNetworkInterfaceAttribute",
                "ec2:RevokeSecurityGroupIngress"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:AddListenerCertificates",
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:CreateListener",
                "elasticloadbalancing:CreateLoadBalancerListeners",
                "elasticloadbalancing:CreateRule",
                "elasticloadbalancing:CreateTargetGroup",
                "elasticloadbalancing:DeleteListener",
                "elasticloadbalancing:DeleteLoadBalancer",
                "elasticloadbalancing:DeleteRule",
                "elasticloadbalancing:DeleteTargetGroup",
                "elasticloadbalancing:DeregisterTargets",
                "elasticloadbalancing:DescribeListenerCertificates",
                "elasticloadbalancing:DescribeListeners",
                "elasticloadbalancing:DescribeLoadBalancerAttributes",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeRules",
                "elasticloadbalancing:DescribeSSLPolicies",
                "elasticloadbalancing:DescribeTags",
                "elasticloadbalancing:DescribeTargetGroupAttributes",
                "elasticloadbalancing:DescribeTargetGroups",
                "elasticloadbalancing:DescribeTargetHealth",
                "elasticloadbalancing:ModifyListener",
                "elasticloadbalancing:ModifyLoadBalancerAttributes",
                "elasticloadbalancing:ModifyRule",
                "elasticloadbalancing:ModifyTargetGroup",
                "elasticloadbalancing:ModifyTargetGroupAttributes",
                "elasticloadbalancing:RegisterTargets",
                "elasticloadbalancing:RemoveListenerCertificates",
                "elasticloadbalancing:RemoveTags",
                "elasticloadbalancing:SetIpAddressType",
                "elasticloadbalancing:SetSecurityGroups",
                "elasticloadbalancing:SetSubnets",
                "elasticloadbalancing:SetWebACL"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "iam:CreateServiceLinkedRole",
                "iam:GetServerCertificate",
                "iam:ListServerCertificates"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "cognito-idp:DescribeUserPoolClient"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "waf-regional:GetWebACLForResource",
                "waf-regional:GetWebACL",
                "waf-regional:AssociateWebACL",
                "waf-regional:DisassociateWebACL",
                "wafv2:GetWebACLForResource",
                "wafv2:GetWebACL",
                "wafv2:AssociateWebACL",
                "wafv2:DisassociateWebACL",
                "shield:GetSubscriptionState",
                "shield:DescribeProtection",
                "shield:CreateProtection",
                "shield:DeleteProtection"
            ],
            "Resource": "*"
        }
    ]
}
EOF

# Create policy
aws iam create-policy \
    --policy-name ALBIngressControllerIAMPolicy \
    --policy-document file://alb-ingress-controller-policy.json

# Get OIDC provider
OIDC_PROVIDER=$(aws eks describe-cluster \
    --name employee-management-cluster \
    --query "cluster.identity.oidc.issuer" \
    --output text | sed -e "s/^https:\/\///")

# Create IAM role
eksctl create iamserviceaccount \
    --cluster employee-management-cluster \
    --namespace kube-system \
    --name aws-load-balancer-controller \
    --attach-policy-arn arn:aws:iam::<account-id>:policy/ALBIngressControllerIAMPolicy \
    --approve \
    --override-existing-serviceaccounts
```

**What this does**: Sets up IAM Roles for Service Accounts (IRSA) to allow the AWS Load Balancer Controller to manage AWS resources.

### Step 10: Setup SSL Certificate for Ingress

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer for Let's Encrypt
cat > cluster-issuer.yaml <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: alb
EOF

kubectl apply -f cluster-issuer.yaml
```

**What this does**: Installs cert-manager and configures Let's Encrypt for automatic SSL certificate management.

### Step 11: Monitor and Scale

```bash
# Check HPA status
kubectl get hpa

# Check pod autoscaling
kubectl describe hpa employee-management-hpa

# View resource usage
kubectl top nodes
kubectl top pods

# Scale deployment manually
kubectl scale deployment employee-management --replicas=5
```

### Step 12: Setup Monitoring (Optional)

```bash
# Install Prometheus and Grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
    --namespace monitoring \
    --create-namespace

# Port forward to access Grafana
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```

**What this does**: Installs Prometheus and Grafana for monitoring the EKS cluster and application metrics.

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Errors

**Problem**: Can't connect to MySQL database

**Solutions**:
- Verify RDS instance is running: `aws rds describe-db-instances --db-instance-identifier employee-management-db`
- Check security group allows inbound traffic on port 3306
- Verify credentials in .env file
- Test connection from EC2 instance: `mysql -h <rds-endpoint> -u admin -p`

#### 2. S3 Upload Errors

**Problem**: Images not uploading to S3

**Solutions**:
- Verify AWS credentials are correct
- Check S3 bucket policy allows public read access
- Verify bucket exists in correct region
- Check IAM user has S3 permissions

#### 3. Static Files Not Loading

**Problem**: CSS/JS files not loading in production

**Solutions**:
- Run `python manage.py collectstatic`
- Verify STATIC_ROOT and STATIC_URL in settings.py
- Check Nginx configuration for static file serving
- Verify file permissions

#### 4. Pod Not Starting in EKS

**Problem**: Kubernetes pods stuck in Pending or CrashLoopBackOff

**Solutions**:
```bash
# Check pod status
kubectl describe pod <pod-name>

# Check pod logs
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp

# Common issues:
# - Image pull errors: Verify image exists in registry
# - Resource limits: Check if node has enough resources
# - Missing secrets/configmaps: Verify they exist
```

#### 5. Ingress Not Working

**Problem**: Ingress not routing traffic to pods

**Solutions**:
- Verify AWS Load Balancer Controller is running
- Check Ingress resource configuration
- Verify security group allows traffic from ALB
- Check DNS records point to ALB

#### 6. Migration Errors

**Problem**: Django migrations failing

**Solutions**:
```bash
# Check for pending migrations
python manage.py showmigrations

# Reset migrations (development only)
python manage.py migrate --fake-initial

# Create new migrations
python manage.py makemigrations

# Apply migrations with verbosity
python manage.py migrate --verbosity 3
```

### Health Checks

```bash
# Django application health
curl http://localhost:8000/

# Database connection
python manage.py dbshell

# S3 connectivity
aws s3 ls s3://your-bucket-name

# Kubernetes health
kubectl get pods
kubectl get services
kubectl describe deployment employee-management
```

### Log Locations

- **Django logs**: `/var/log/employee-management/` (if configured)
- **Nginx logs**: `/var/log/nginx/`
- **Systemd service logs**: `journalctl -u employee-management -f`
- **Kubernetes pod logs**: `kubectl logs -f deployment/employee-management`

### Backup and Recovery

#### Database Backup

```bash
# Backup RDS database
aws rds create-db-snapshot \
    --db-instance-identifier employee-management-db \
    --db-snapshot-identifier employee-management-backup-$(date +%Y%m%d)

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
    --db-instance-identifier employee-management-db-restored \
    --db-snapshot-identifier employee-management-backup-YYYYMMDD
```

#### S3 Backup

```bash
# Sync S3 bucket to local
aws s3 sync s3://your-bucket-name ./backup

# Sync local to S3
aws s3 sync ./backup s3://your-bucket-name
```

---

## Summary

This guide covers:

✅ Local development setup with Docker Compose  
✅ AWS infrastructure (S3 bucket, RDS MySQL instance)  
✅ Ubuntu EC2 deployment with Nginx and Gunicorn  
✅ EKS deployment with Kubernetes manifests  
✅ SSL/TLS configuration with Let's Encrypt  
✅ Monitoring and scaling with HPA  
✅ Troubleshooting common issues

For additional support or questions, refer to:
- [Django Documentation](https://docs.djangoproject.com/)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [EKS Documentation](https://docs.aws.amazon.com/eks/)

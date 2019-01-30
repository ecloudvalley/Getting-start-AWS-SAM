# AWS Serverless Application Model

## **Overview**

The AWS Serverless Application Model (AWS SAM) is an open-source framework that you can use to build serverless applications on AWS.

A serverless application is a combination of Lambda functions, event sources, and other resources that work together to perform tasks. A serverless application is more than just a Lambda function-it can include additional resources such as APIs, databases, and event source mappings.

AWS SAM consists of the following components:

1. AWS SAM template specification: Specification provides a simple and clean syntax to describe the functions, APIs, permissions, configuration, and events that make up a serverless application.You use an AWS SAM template file to operate on a single, deployable, versioned entity that's your serverless application.
2. AWS SAM command line interface (AWS SAM CLI): You use this tool to build serverless applications that are defined by AWS SAM templates. The CLI provides commands that enable you to verify that AWS SAM template files are written according to the specification, invoke Lambda functions locally, step-through debug Lambda functions, package and deploy serverless applications to the AWS Cloud, and so on.

## **Scenario**

In this lab, you will use AWS Serverless Application Model to build a simple serverless web application. This application can read and write item to DynamoDB table. When the data write to DynamoDB, it will trigger Lambda to write the record in CloudWatch.
<p align="center">
    <img src="images/001-SAM-Architecture.jpg" width="70%" height="70%">
</p>

## **Step by Step**

### **Create Cloud9 environment**

In this section, we need to create a **Cloud9** environment.

- On the service menu, choose **Cloud9**, Choose **Create environment**.
- On the **Name environment** page, type a **Name** for your environment. Choose **Next step**.

<p align="center">
    <img src="images/003-SAM-CreateCloud9Environment-01.png" width="70%" height="70%">
</p>

- On the **Configure settings** page: <br />
    1. **Environment type**: Choose **Create a new instance for environment (EC2)**.
    2. **Instance Type**: Choose **t2.micro (1 GiB RAM + 1 vCPU)**.
    3. **Cost-saving setting**: Choose **Cost-saving setting**.

<p align="center">
    <img src="images/004-SAM-CreateCloud9Environment-02.png" width="70%" height="70%">
</p>

<p align="center">
    <img src="images/005-SAM-CreateCloud9Environment-03.png" width="70%" height="70%">
</p>

- Choose **Next Step**.
- On the **Review** page, choose **Create environment**.
- The environment will be creating and setting, wait for a minute.

### **Initial lab material**

In this section, you will use SAM to build a serverless web application.

- In the terminal, which opened in the previous step, type the following command to clone the lab source.

```
$ git clone https://gitlab.com/ecloudture/blog/aws-serverless-application-model.git
$ cd ~/environment/aws-serverless-application-model
```

- Install the dependencies by running the following sam command.

```
$ sam build --use-container
```

- In the following command, we create an S3 bucket to save the deployment package. Please replace "<YOUR_BUCKET_NAME>" with unique name.

```
aws s3 mb s3://<YOUR_BUCKET_NAME>
```

- In the following command, we create the deployment package for deploy our web application. Please replace "<YOUR_BUCKET_NAME>" with your bucket name which created in the previous step. And then the file **package.yaml** will be created under the "aws-serverless-application-model" folder.

```
$ sam package --output-template-file package.yaml --s3-bucket <YOUR_BUCKET_NAME>
```

- In the following command, replace "<YOUR_STACK_NAME>" with your stack name and run it to deploy all of resources that you defined in the template.

```
$ sam deploy --template-file package.yaml --stack-name <YOUR_STACK_NAME> --capabilities CAPABILITY_IAM --region us-east-1
```

- Please wait for a while, all of resources are being create depending on the content defined in the template.

### **Access Website**

In this section, you will access your web application by **index.html** which hosted in your **S3 Bucket**.

- On the service menu, choose **CloudFormation**. Type your stack name in the filter. And then choose your stack.

<p align="center">
    <img src="images/006-SAM-CloudFormationFilter.png" width="70%" height="70%">
</p>

- As you can see, your stack is already in the status of "CREATE_COMPLETE".

- Select the **Outputs** section. You can find the **GetItemApi** and **PostItemApi**, copy the value of these key to the textbook.

<p align="center">
    <img src="images/007-SAM-CloudFormationOutputs.png" width="70%" height="70%">
</p>

- In Cloud9, open the file **index.html** under the folder **aws-serverless-application-model**.

- In the bottom half of the **index.html**, replace "<EDNPOINT_FOR_POST_ITEM>" and "<ENDPOINT_FOR_GET_ITEM>" with the value of **PostItemApi** and **GetItemApi** respectively.

<p align="center">
    <img src="images/008-SAM-PastePost&GetUrL.png" width="70%" height="70%">
</p>

- In the Cloud9 terminal, type the following command. The command copy the file to **S3 Bucket**. Please replace "<YOUR_BUCKET_NAME>" with your bucket name which created in the previous step.

```
$ aws s3 cp ~/environment/aws-serverless-application-model/index.html s3://<YOUR_BUCKET_NAME>
```

- On the service menu, choose **S3**. Type your bucket name in the field of **Search for buckets**, then choose your bucket.

<p align="center">
    <img src="images/009-SAM-S3Filter.png" width="70%" height="70%">
</p>

- Select **index.html**. Choose **Permissions** tab. 

- In the **Public access** section, select **Everyone**.

<p align="center">
    <img src="images/011-SAM-S3PublicAccess-01.png" width="70%" height="70%">
</p>

- In the pop-up window, choose **Read object**, then select **Save**.

<p align="center">
    <img src="images/012-SAM-S3PublicAccess-02.png" width="50%" height="50%">
</p>

- Now, **index.html** can be publicly accessed. The next step, we will enable static web hosting through **S3**.

- Reture to the previous page.

<p align="center">
    <img src="images/013-SAM-S3WebHosting-02.png
" width="70%" height="70%">
</p>

- Select **Properties** tab.

- Choose **Static web hosting**, then select **Use this bucket to host a website**.

- Copy the endpoint on the top of window to the textbook.

- Type **index.html** for index document field, then choose **Save**.

<p align="center">
    <img src="images/010-SAM-S3WebHosting-01.png
" width="70%" height="70%">
</p>

- At last, paste the endpoint to your browser. You will see the website as bellow:

<p align="center">
    <img src="images/014-SAM-Website.png
" width="70%" height="70%">
</p>

- Type in these fileds to test your web application.

### **Create new Lambda function**

In this section, you will create a Lambda funtion. When the data is writed to DynamoDB through your website, this Lambda will be triggered to write the logs to **CloudWatch**.

- Copy the following code. This code set the parameter configuration required to create Lambda function and capture the table activity with **DynamoDB** stream.

```
    DetectItemFunction:
        Type: AWS::Serverless::Function
        Properties:
            CodeUri: ./Lambda
            Handler: Lambda3.lambda3_handler
            Runtime: python3.6
            Events:
                DetectEvent:
                    Type: DynamoDB
                    Properties:
                        Stream:
                            !GetAtt DynamoDBTable.StreamArn
                        StartingPosition: TRIM_HORIZON
                        BatchSize: 10
            Policies: arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
            AutoPublishAlias: !Ref Alias

```

- In **Cloud9**, choose **template.yaml** under the folder **aws-serverkess-application-model**.

- Paste the code into **template.yaml**, behind the **GetItemFunction** section as below:

<p align="center">
    <img src="images/015-SAM-TemplateSet.png
" width="70%" height="70%">
</p>

- Save file.

- In the following command, we have added a python file to write the code in Lambda function.

```
$ cd ~/environment/aws-serverless-application-model/Lambda
$ touch Lambda.py
```

- Open the file **Lambda3.py**, paste the following code. 

```
def lambda3_handler(event, context):
    print('hello world')
```

- Save file.

### Deploy your web application again

In this section, you will deploy your web application again due to the project has been modified.

- The following command, you intall the dependencies and create deployment package then deploy all of resources that you defined in the template. Please replace <YOUR_BUCKET_NAME> and <YOUR_STACK_NAME>.

```
$ cd ~/environment/aws-serverless-application-model
$ sam build --use-container
$ sam package --output-template-file package.yaml --s3-bucket <YOUR_BUCKET_NAME>
$ sam deploy --template-file package.yaml --stack-name <YOUR_STACK_NAME> --capabilities CAPABILITY_IAM --region us-east-1
```

- Wait for a while, then you will see the "Successfully" message.

### Test your web application

- Reload the web page and enter the values in those fields to test your website.

<p align="center">
    <img src="images/017-SAM-Website.png
" width="70%" height="70%">

- On the service menu, choose **Lambda**.

- In the filter, type **DetectItemFunction** and choose the result.

- Choose **Monitoring**, then select **View logs in CloudWatch**.

- In the new tab, choose log streams.

- You will see the logs written by Lambda3.

<p align="center">
    <img src="images/018-SAM-Lambda3Logs.png
" width="70%" height="70%">
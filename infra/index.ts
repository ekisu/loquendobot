import * as pulumi from "@pulumi/pulumi";
import * as apigateway from "@pulumi/aws-apigateway";
import * as aws from "@pulumi/aws";
import * as awsx from "@pulumi/awsx";

// Create an AWS resource (S3 Bucket)
const bucket = new aws.s3.Bucket("my-bucket");

const repository = new awsx.ecr.Repository("loquendobot", {
    forceDelete: true,
});

const image = new awsx.ecr.Image("loquendobot", {
    repositoryUrl: repository.url,
    context: '..',
    dockerfile: '../lambda.Dockerfile',
    platform: 'linux/amd64',
})

const role = new aws.iam.Role("loquendobot", {
    assumeRolePolicy: aws.iam.assumeRolePolicyForPrincipal({ Service: "lambda.amazonaws.com" }),
});

new aws.iam.RolePolicyAttachment("lambdaFullAccess", {
    role: role.name,
    policyArn: aws.iam.ManagedPolicy.AWSLambdaExecute,
});

const lambdaFunction = new aws.lambda.Function("loquendobot", {
    packageType: 'Image',
    imageUri: image.imageUri,
    role: role.arn,
    environment: {
        variables: {
            'TELEGRAM_BOT_TOKEN': process.env.TELEGRAM_BOT_TOKEN!,
        }
    },
    timeout: 30,
    // This increases the vCPUs available for the function
    memorySize: 1770,
})

const lambdaFunctionUrl = new aws.lambda.FunctionUrl("loquendobot", {
    functionName: lambdaFunction.name,
    authorizationType: 'NONE',
})

// Export the URL of the application
export const webhookUrl = lambdaFunctionUrl.functionUrl;

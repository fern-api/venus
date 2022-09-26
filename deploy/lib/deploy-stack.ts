import {
  EnvironmentInfo,
  EnvironmentType,
} from "@fern-fern/fern-cloud-client/model/environments";
import { Stack, StackProps } from "aws-cdk-lib";
import { Certificate } from "aws-cdk-lib/aws-certificatemanager";
import { Peer, Port, SecurityGroup, Vpc } from "aws-cdk-lib/aws-ec2";
import { Cluster, ContainerImage, LogDriver } from "aws-cdk-lib/aws-ecs";
import { ApplicationLoadBalancedFargateService } from "aws-cdk-lib/aws-ecs-patterns";
import { ApplicationProtocol } from "aws-cdk-lib/aws-elasticloadbalancingv2";
import { LogGroup } from "aws-cdk-lib/aws-logs";
import { HostedZone } from "aws-cdk-lib/aws-route53";
import { Construct } from "constructs";

const CONTAINER_NAME = "venus";
const SERVICE_NAME = "venus";

export interface VenusEnvVariables {
  AUTH0_DOMAIN_NAME: string,
  AUTH0_CLIENT_ID: string,
  AUTH0_CLIENT_SECRET: string,
  CLOUDMAP_NAME: string,
}

export class VenusDeployStack extends Stack {
  constructor(
    scope: Construct,
    id: string,
    version: string,
    environmentType: EnvironmentType,
    environmentInfo: EnvironmentInfo,
    envVariables: VenusEnvVariables,
    props?: StackProps
  ) {
    super(scope, id, props);

    const vpc = Vpc.fromLookup(this, "vpc", {
      vpcId: environmentInfo.vpcId,
    });

    const venusSg = new SecurityGroup(this, "venus-sg", {
      securityGroupName: `venus-${environmentType.toLowerCase()}`,
      vpc,
      allowAllOutbound: true,
    });
    venusSg.addIngressRule(
      Peer.anyIpv4(),
      Port.tcp(443),
      "allow HTTPS traffic from anywhere"
    );

    const cluster = Cluster.fromClusterAttributes(this, "cluster", {
      clusterName: environmentInfo.ecsInfo.clusterName,
      vpc,
      securityGroups: [],
    });

    const logGroup = LogGroup.fromLogGroupName(
      this,
      "log-group",
      environmentInfo.logGroupInfo.logGroupName
    );

    const certificate = Certificate.fromCertificateArn(
      this,
      "ceritificate",
      environmentInfo.route53Info.certificateArn
    );

    const fargateService = new ApplicationLoadBalancedFargateService(
      this,
      SERVICE_NAME,
      {
        serviceName: SERVICE_NAME,
        cluster,
        cpu: 256,
        memoryLimitMiB: 512,
        desiredCount: 1,
        securityGroups: [],
        taskImageOptions: {
          image: ContainerImage.fromTarball(`../venus:${version}.tar`),
          containerName: CONTAINER_NAME,
          containerPort: 8080,
          enableLogging: true,
          logDriver: LogDriver.awsLogs({
            logGroup,
            streamPrefix: SERVICE_NAME,
          }),
          environment: {
            ...envVariables
          }
        },
        assignPublicIp: true,
        publicLoadBalancer: true,
        enableECSManagedTags: true,
        protocol: ApplicationProtocol.HTTPS,
        certificate,
        domainZone: HostedZone.fromHostedZoneAttributes(this, "zoneId", {
          hostedZoneId: environmentInfo.route53Info.hostedZoneId,
          zoneName: environmentInfo.route53Info.hostedZoneName,
        }),
        domainName: getServiceDomainName(environmentType, environmentInfo),
      }
    );

    fargateService.targetGroup.setAttribute(
      "deregistration_delay.timeout_seconds",
      "30"
    );

    fargateService.targetGroup.configureHealthCheck({
      healthyHttpCodes: "200,204",
      path: "/health",
      port: "8080",
    });
  }
}

function getServiceDomainName(
  environmentType: EnvironmentType,
  environmentInfo: EnvironmentInfo
) {
  if (environmentType == EnvironmentType.Prod) {
    return `venus.${environmentInfo.route53Info.hostedZoneName}`;
  }
  return `venus-${environmentType.toLowerCase()}.${
    environmentInfo.route53Info.hostedZoneName
  }`;
}

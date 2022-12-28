#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { VenusDeployStack } from "../lib/deploy-stack";
import {
  Environments,
  EnvironmentType,
} from "@fern-fern/fern-cloud-client/model/environments";
import axios from "axios";

void main();

async function main() {
  const version = process.env["VERSION"];
  if (version === undefined) {
    throw new Error("Version is not specified!");
  }
  const environments = await getEnvironments();
  const app = new cdk.App();
  for (const environmentType of Object.keys(environments)) {
    switch (environmentType) {
      case EnvironmentType.Dev:
        const devInfo = environments[environmentType];
        new VenusDeployStack(
          app,
          `venus-${environmentType.toLowerCase()}`,
          version,
          environmentType,
          devInfo,
          {
            AUTH0_DOMAIN_NAME: "fern-dev.us.auth0.com",
            AUTH0_CLIENT_ID: "8lyAgexpGrHZLhN2i1FNPSicjupACR1r",
            AUTH0_CLIENT_SECRET: getEnvVarOrThrow("AUTH0_CLIENT_SECRET"),
            AUTH0_MGMT_AUDIENCE: "https://fern-dev.us.auth0.com/api/v2/",
            NURSERY_ORIGIN: `http://nursery.${devInfo.cloudMapNamespaceInfo.namespaceName}:8080`,
            AUTH0_VENUS_AUDIENCE: "venus-dev",
          },
          {
            env: { account: "985111089818", region: "us-east-1" },
          }
        );
        break;
      case EnvironmentType.Prod:
        const prodInfo = environments[environmentType];
        new VenusDeployStack(
          app,
          `venus-${environmentType.toLowerCase()}`,
          version,
          environmentType,
          prodInfo,
          {
            AUTH0_DOMAIN_NAME: "fern-prod.us.auth0.com",
            AUTH0_CLIENT_ID: "gRM6LcuNPpl1ntHwOgdVYWWcjaUVrfgG",
            AUTH0_CLIENT_SECRET: getEnvVarOrThrow("AUTH0_CLIENT_SECRET"),
            AUTH0_MGMT_AUDIENCE: "https://fern-prod.us.auth0.com/api/v2/",
            NURSERY_ORIGIN: `http://nursery.${prodInfo.cloudMapNamespaceInfo.namespaceName}:8080`,
            AUTH0_VENUS_AUDIENCE: "venus-prod",
          },
          {
            env: { account: "985111089818", region: "us-east-1" },
          }
        );
        break;
      default:
        return;
    }
  }
}

function getEnvVarOrThrow(envVarName: string): string {
  const val = process.env[envVarName];
  if (val != null) {
    return val;
  }
  throw Error("Expected environment variable to be defined: " + envVarName);
}

async function getEnvironments(): Promise<Environments> {
  const response = await axios(
    "https://raw.githubusercontent.com/fern-api/fern-cloud/main/env-scoped-resources/environments.json",
    {
      method: "GET",
      headers: {
        Authorization: "Bearer " + process.env["GITHUB_TOKEN"],
      },
    }
  );
  return response.data as Environments;
}

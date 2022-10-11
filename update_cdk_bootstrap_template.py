#!/usr/bin/python3
"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0

This script is intended to be used to update the cdk bootstrap command
cloudformation YAML file to include a boundary policy if a AWS account
requires a boundary policy attached to a IAM role.
"""
import yaml
import json
import argparse


parser = argparse.ArgumentParser(
    description='Update the CDK bootstrap template to include a boundary \
                    policy if your organization requires one to be attached \
                    to IAM roles.')

parser.add_argument('template_file', type=str,
                    help='The path to the CDK bootstrap template file.')
parser.add_argument('policy_arn', metavar='policy_arn', type=str,
                    help='The ARN of the boundary policy to be applied to \
                            the CDK bootstrap template.')

args = parser.parse_args()


with open(args.template_file, 'rb') as stream:
    try:
        parsed_yaml = yaml.safe_load(stream)
        # secure load of yaml think job zero
        for r in parsed_yaml["Resources"]:
            for x in (parsed_yaml["Resources"][r]):
                if "AWS::IAM::Role" in parsed_yaml["Resources"][r][x]:
                    dict_yaml = parsed_yaml["Resources"][r]["Properties"]
                    parsed_yaml["Resources"][r]["Properties"]\
                        ["PermissionsBoundary"] = args.policy_arn
            str_yaml = json.dumps(parsed_yaml)

            parsed_yaml = json.loads(str_yaml)
        with open("./bootstrap-template.yaml", "w", encoding='utf8') as f:
            yaml.dump(parsed_yaml, f)

    #except yaml.YAMLError as exc:
    except yaml.YAMLError as e:
        print("YAML Parsing Failed because {0}",e.reason)

#!/bin/bash
# test.sh: Script to execute the performance tests
#
# Usage: test.sh

set -e

cd "$(dirname "$0")/.."

# This is a simple FHIR example to show the environment is working, this will
# be removed in the future and replaced with a set of scripts that generate data.
EXAMPLE_FHIR=$(cat << EOF
{
    "bundle": {
        "resourceType": "Bundle",
        "identifier": {
            "value": "a very contrived FHIR bundle"
        },
        "entry": [
            {
                "resource": {
                    "resourceType": "Patient",
                    "id": "`uuidgen`",
                    "identifier": [
                        {
                            "value": "0987654321",
                            "type": {
                                "coding": [
                                    {
                                        "code": "MR",
                                        "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                                        "display": "Medical record number"
                                    }
                                ]
                            }
                        }
                    ],
                    "name": [
                        {
                            "family": "Kent",
                            "given": [
                                "Clark",
                                "Superman"
                            ]
                        }
                    ],
                    "birthDate": "1950-08-04",
                    "gender": "male",
                    "address": [
                        {
                            "line": [
                                "some street"
                            ],
                            "city": "Topeka",
                            "state": "Kansas",
                            "postalCode": "11111",
                            "use": "home"
                        }
                    ]
                }
            }
        ]
    }
}
EOF
)

curl -X POST http://api:8080/link-record -d "${EXAMPLE_FHIR}" --header "Content-Type: application/json"

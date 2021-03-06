description: >
  Select the version of NodeJS to use. Uses CircleCI's highly cached convenience
  images built for CI.

  Any available tag from this list can be used:
  https://hub.docker.com/r/cimg/node/tags
docker:
  - image: 'cimg/node:<<parameters.tag>>'
parameters:
  tag:
    default: '13.11'
    description: >
      Pick a specific cimg/node image version tag:
      https://hub.docker.com/r/cimg/node
    type: string

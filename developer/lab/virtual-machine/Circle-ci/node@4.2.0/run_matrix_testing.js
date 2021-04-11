version: '2.1'
orbs:
  node: circleci/node@x.y
workflows:
  matrix-tests:
    jobs:
      - node/test:
          matrix:
            parameters:
              version:
                - 13.11.0
                - 12.16.0
                - 10.19.0

version: '2.1'
orbs:
  node: circleci/node@x.y
jobs:
  install-node-example:
    docker:
      - image: 'cimg/base:stable'
    steps:
      - checkout
      - node/install:
          install-yarn: true
      - run: node --version
workflows:
  test_my_app:
    jobs:
      - install-node-example

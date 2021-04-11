version: '2.1'
orbs:
  node: circleci/node@x.y
jobs:
  test:
    executor: node/default
    steps:
      - checkout
      - node/install-packages:
          cache-path: ~/project/node_modules
          override-ci-command: npm install
      - run: npm run test
workflows:
  test_my_app:
    jobs:
      - test

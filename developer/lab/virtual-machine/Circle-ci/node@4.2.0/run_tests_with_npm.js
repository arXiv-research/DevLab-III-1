version: '2.1'
orbs:
  node: circleci/node@x.y
jobs:
  test:
    executor:
      name: node/default
      tag: '13.14'
    steps:
      - checkout
      - node/install-packages
      - run:
          command: npm run test
workflows:
  test_my_app:
    jobs:
      - test

version: '2.1'
orbs:
  slack: circleci/slack@4.1
jobs:
  build:
    machine: true
    steps:
      - run: some build command
      - slack/notify:
          branch_pattern: main
          event: fail
          template: basic_fail_1
      - slack/notify:
          branch_pattern: production
          event: fail
          mentions: '<@U8XXXXXXX>, @UserName'
          template: basic_fail_1
workflows:
  deploy_and_notify:
    jobs:
      - build:
          context: slack-secrets
      - deploy:
          filters:
            branches:
              only:
                - production
          requires:
            - build

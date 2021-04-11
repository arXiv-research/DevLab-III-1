version: '2.1'
orbs:
  node: 'circleci/node:4.1'
  slack: circleci/slack@4.1
jobs:
  deploy:
    executor:
      name: node/default
    steps:
      - slack/notify:
          channel: 'ABCXYZ, ZXCVBN'
          custom: |
            {
              "blocks": [
                {
                  "type": "section",
                  "fields": [
                    {
                      "type": "plain_text",
                      "text": "*This is a text notification*",
                      "emoji": true
                    }
                  ]
                }
              ]
            }
          event: always
workflows:
  deploy_and_notify:
    jobs:
      - deploy:
          context: slack-secrets

version: '2.1'
orbs:
  heroku: circleci/heroku@x.y
  node: circleci/node@x.y
workflows:
  test-and-deploy:
    jobs:
      - node/test
      - heroku/deploy-via-git:
          filters:
            branches:
              only:
                - master
          requires:
            - node/test

description: |
  Simple drop-in job to test your NodeJS application automatically.
executor:
  name: default
  tag: << parameters.version >>
parameters:
  app-dir:
    default: ~/project
    description: >-
      Path to the directory containing your package.json file. Not needed if
      package.json lives in the root.
    type: string
  cache-version:
    default: v1
    description: >-
      Change the default cache version if you need to clear the cache for any
      reason.
    type: string
  override-ci-command:
    default: ''
    description: >
      By default, packages will be installed with "npm ci" or "yarn install
      --frozen-lockfile".

      Optionally supply a custom package installation command, with any
      additional flags needed.
    type: string
  pkg-manager:
    default: npm
    description: Select the default node package manager to use.
    enum:
      - npm
      - yarn
    type: enum
  run-command:
    default: test
    description: The name of the script within your package.json which will run your tests.
    type: string
  setup:
    default: []
    description: >-
      Provide any optional steps you would like to run prior to installing the
      node dependencies. This is a good place to install global modules.
    type: steps
  version:
    default: 13.11.0
    description: >
      A full version tag must be specified. Example: "13.11.0" For a full list
      of releases, see the following: https://nodejs.org/en/download/releases
    type: string
steps:
  - checkout
  - steps: << parameters.setup >>
  - install-packages:
      app-dir: <<parameters.app-dir>>
      cache-version: <<parameters.cache-version>>
      override-ci-command: <<parameters.override-ci-command>>
      pkg-manager: <<parameters.pkg-manager>>
  - when:
      condition:
        equal:
          - npm
          - << parameters.pkg-manager >>
      steps:
        - run:
            command: npm run <<parameters.run-command>>
            name: Run NPM Tests
            working_directory: <<parameters.app-dir>>
  - when:
      condition:
        equal:
          - yarn
          - << parameters.pkg-manager >>
      steps:
        - run:
            command: yarn run <<parameters.run-command>>
            name: Run YARN Tests
            working_directory: <<parameters.app-dir>>

description: >
  Install custom versions of NodeJS, and optionally NPM/Yarn, in any

  execution environment (Docker/Linux, macOS, machine) that does not have

  it preinstalled.


  Recommendation: It is highly recommended to utilize an environment such as
  Docker with Node preinstalled.
parameters:
  install-npm:
    default: true
    description: Install NPM?
    type: boolean
  install-yarn:
    default: false
    description: Install Yarn?
    type: boolean
  lts:
    default: false
    description: Install the latest LTS version by default.
    type: boolean
  node-install-dir:
    default: /usr/local
    description: |
      Where should Node.js be installed?
    type: string
  node-version:
    default: node
    description: >
      Specify the full version tag to install. To install the latest LTS
      version, set `lts` to true. The latest (current) version of NodeJS will be
      installed by default. For a full list of releases, see the following:
      https://nodejs.org/en/download/releases
    type: string
  npm-version:
    default: latest
    description: |
      Pick a version of NPM to install: https://nodejs.org/en/download/releases
    type: string
  yarn-version:
    default: ''
    description: >
      Pick a version of Yarn to install (if no version is specified, the latest
      stable version will be installed):
      https://github.com/yarnpkg/yarn/releases
    type: string
steps:
  - run:
      command: |
        # Only install nvm if it's not already installed
        if command -v nvm &> /dev/null; then
            echo "nvm is already installed. Skipping nvm install.";
        else
            curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash;
            echo 'export NVM_DIR="$HOME/.nvm"' >> $BASH_ENV;
            echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> $BASH_ENV;
            source $BASH_ENV;
        fi

        if [ "$NODE_PARAM_LTS" = "1" ]; then
            nvm install --lts
        else
            nvm install "$NODE_PARAM_VERSION"
        fi
      environment:
        NODE_PARAM_LTS: <<parameters.lts>>
        NODE_PARAM_VERSION: <<parameters.node-version>>
      name: >-
        Install NodeJS <<^parameters.lts>> <<parameters.node-version>>
        <</parameters.lts>> <<#parameters.lts>> LTS <</parameters.lts>>
  - when:
      condition: <<parameters.install-npm>>
      steps:
        - install-npm:
            version: <<parameters.npm-version>>
  - when:
      condition: <<parameters.install-yarn>>
      steps:
        - install-yarn:
            version: <<parameters.yarn-version>>

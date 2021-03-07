description: >
  Insert this job in-line with your standard CircleCI on-hold notification jobs
  to simulataniously send a Slack notification containing a link to the paused
  Workflow.
docker:
  - image: 'cimg/base:stable'
parameters:
  branch_pattern:
    default: .+
    description: >
      A comma separated list of regex matchable branch names. Notifications will
      only be sent if sent from a job from these branches. By default ".+" will
      be used to match all branches. Pattern must match the full string, no
      partial matches.
    type: string
  channel:
    default: $SLACK_DEFAULT_CHANNEL
    description: >
      Select which channel in which to post to. Channel name or ID will work.
      You may include a comma separated list of channels if you wish to post to
      multiple channels at once. Set the "SLACK_DEFAULT_CHANNEL" environment
      variable for the default channel.
    type: string
  custom:
    default: ''
    description: >
      (optional) Enter a custom message template.


      1. Create your message template using the Block Kit Builder:
      https://app.slack.com/block-kit-builder/.

      2. Insert any desired environment variables.

      3. Paste value here.
    type: string
  mentions:
    default: ''
    description: >
      Exports to the "$SLACK_PARAM_MENTIONS" environment variable for use in
      templates.

      Mention users via the @ symbol: "@USER"

      If the username contains a space, the Slack ID must be used with angled
      brackets: "<@U8XXXXXXX>"
    type: string
  template:
    default: basic_on_hold_1
    description: >-
      (optional) By default this job will send the standard "basic_on_hold_1"
      template. In order to use a custom template you must also set this value
      to an empty string.
    type: string
resource_class: small
steps:
  - notify:
      branch_pattern: <<parameters.branch_pattern>>
      channel: <<parameters.channel>>
      custom: <<parameters.custom>>
      event: always
      mentions: <<parameters.mentions>>
      template: <<parameters.template>>

The model was trained in the following way:

- Training step 1:
    x: 4
    y: 4
    run-id: ac_1
    episodes: 100000
    max steps: 200
    gamma: 0.995
    seed: 42
    learning-rate: 0.001
    neurons: 512

- Training step 2:
    x: 4
    y: 4
    run-id: ac_1_cont
    episodes: 500000
    max steps: 200
    gamma: 0.995
    seed: 42
    learning-rate: 0.001
    neurons: 512

- Training step 3:
    x: 8
    y: 8
    run-id: ac_1_cont_2
    episodes: 500000
    max steps: 200
    gamma: 0.995
    seed: 42
    learning-rate: 0.001
    neurons: 512

- Training step 4:

    x: 10
    y: 10
    run-id: ac_1_cont_3_with_negative_reward
    episodes: 155000
    max steps: 400
    gamma: 0.995
    seed: 42
    learning-rate: 0.001
    neurons: 512

    With a light negative reward of  -0.01 if not eaten during a step

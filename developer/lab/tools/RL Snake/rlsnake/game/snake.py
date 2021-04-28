import numpy as np

class Snake:
    """
    A implementation of the game snake

    Example layout for a 4x2 field:
        ------
        |....|
        |....|
        ------
    The snake can move on the '.' tiles.

    The snake can be controlled by either turning left or turning right or do nothing (continue moving straight).
    With every step it will move one tile and it will grow one tile.

    The game ends if it hits the wall or if it hits itself. The goal is to grow the snake as long as possible, where
    the maximum length is n_x x n_y, i.e., in the case of our example 8.
    """

    current_direction = 0
    # Directions correspond to velocity (vx, vy)
    # 0 ... (1, 0)
    # 1 ... (-1, 0)
    # 2 ... (0, 1)
    # 3 ... (0, -1)
    current_velocity = [1, 0]

    # Snake is the current snake
    snake = []

    food = []

    score = 0
    moves = 0

    def __init__(self, n_x, n_y):
        """
        Args:
            n_x (int): number of tiles in x direction (horizontal).
            n_y (int): number of tiles in y direction (vertical).
            sdl2 (bool, optional): sdl2 output.
        """
        self.n_x = n_x
        self.n_y = n_y

        # Max score depends on the number of tiles and on the initial length of the snake, which is, for now, hardcoded 1
        self.max_score = self.n_x*self.n_y - 1

        # Visibility range is the number of tiles in each direction the snake can see when the get_view_obs() function is ued
        self.visibility_range = 4

    def step(self, action):
        """
        Perform one step

        # Directions correspond to velocity (vx, vy)
        # 0 ... (1, 0)
        # 1 ... (-1, 0)
        # 2 ... (0, 1)
        # 3 ... (0, -1)

        It returns a new observation after the step is performed.
        """

        self.moves += 1

        self.current_velocity = self._get_velocity_for_direction(action)

        (head_x, head_y) = self.snake[-1]
        new_head = (head_x+self.current_velocity[0], head_y+self.current_velocity[1])

        ok = self._check_head(new_head)
        if not ok:
            return self.get_obs(), True, [self.moves]
        else:
            self.snake.append(new_head)

        if self._check_pos_has_food(new_head):
            self.score += 1
            if self.score == self.max_score:
                return self.get_obs(), True, [self.moves]
            else:
                self.food = [self._gen_food()]
        else:
            self.snake.pop(0)

        return self.get_obs(), False, [self.moves]

    def get_actions(self):
        return 4

    def get_score(self):
        return self.score

    def set_visibility_range(self, visibility_range):
        self.visibility_range = visibility_range

    def _check_head(self, head):
        if self._check_in_snake(head) and head != self.snake[0]:
            return False

        if head[0] >= self.n_x or head[0] < 0:
            return False
        if head[1] >= self.n_y or head[1] < 0:
            return False

        return True

    def _check_pos_has_food(self, pos):
        if pos in self.food:
            return True
        else:
            return False

    def _check_in_snake(self, coords):
        if coords in self.snake:
            return True

    def _check_pos_is_wall(self, pos):
        if pos[0] >= self.n_x or pos[0] < 0:
            return True
        if pos[1] >= self.n_y or pos[1] < 0:
            return True

    def reset(self):
        """ Reset the game """
        self.score = 0
        self.moves = 0
        self.snake = []
        x = np.random.randint(0, self.n_x)
        y = np.random.randint(0, self.n_y)
        self.snake.append((x, y))

        self.food = [self._gen_food()]
        return self.get_obs()

    def _gen_food(self):
        x = np.random.randint(0, self.n_x)
        y = np.random.randint(0, self.n_y)

        while self._check_in_snake((x, y)):
            x = np.random.randint(0, self.n_x)
            y = np.random.randint(0, self.n_y)

        return (x, y)

    def get_obs(self):
        """ Returns the currect state of the game

        It is a tuple containing all tiles and the direction the snake is currently moving

        0 ... empty
        1 ... walls
        2 ... snake
        3 ... food
        4 ... current head
        """

        obs = self.get_tiles().flatten()
        np.append(obs, [self.current_direction])

        return obs

    def get_tiles(self):
        """ Returns the currect tiles of the game as (x, y) elements

        It is a tuple containing all tiles and the direction the snake is currently moving

        0 ... empty
        1 ... walls
        2 ... snake
        3 ... food
        4 ... current head
        """

        obs = np.zeros( (self.n_x, self.n_y), dtype=np.float32)

        for (x, y) in self.snake:
            obs[x][y] = 2

        obs[self.snake[-1][0]][self.snake[-1][1]] = 4

        for (x, y) in self.food:
            obs[x][y] = 3

        return obs

    def get_view_obs(self):
        """
        Returns the currect view of the snake.

        The snake can see all adjacent tiles around it's head in all movement directions, but not more.

        The function returns a  list of these points in the follwing format:

        [
            direction 0 -> head_pos + 1*(1, 0)
            direction 0 -> head_pos + 2*(1, 0)
            direction 0 -> head_pos + 3*(1, 0)
            ...
            direction 0 -> head_pos + self.visibility_range*(1, 0)
            direction 1 -> head_pos + (-1, 0)
            ...
            direction 2 -> head_pos + (0, 1)
            ...
            direction 3 -> head_pos + (0, -1)
            ...
        ]

        with the following numbers

        0 ... empty
        1 ... walls
        2 ... snake
        3 ... food
        4 ... current head

        for the different observations.
        """

        (head_x, head_y) = self.snake[-1]

        view = []
        for i in range(self.visibility_range):
            view.append(self._determine_tile_type(head_x + (i+1)*self._get_velocity_for_direction(0)[0], head_y + (i+1)*self._get_velocity_for_direction(0)[1]))
        for i in range(self.visibility_range):
            view.append(self._determine_tile_type(head_x + (i+1)*self._get_velocity_for_direction(1)[0], head_y + (i+1)*self._get_velocity_for_direction(1)[1]))
        for i in range(self.visibility_range):
            view.append(self._determine_tile_type(head_x + (i+1)*self._get_velocity_for_direction(2)[0], head_y + (i+1)*self._get_velocity_for_direction(2)[1]))
        for i in range(self.visibility_range):
            view.append(self._determine_tile_type(head_x + (i+1)*self._get_velocity_for_direction(3)[0], head_y + (i+1)*self._get_velocity_for_direction(3)[1]))

        return np.array(view)

    def get_current_view(self):
        (head_x, head_y) = self.snake[-1]

        view = []
        for i in range(self.visibility_range):
            view.append((head_x + (i+1)*self._get_velocity_for_direction(0)[0], head_y + (i+1)*self._get_velocity_for_direction(0)[1]))
        for i in range(self.visibility_range):
            view.append((head_x + (i+1)*self._get_velocity_for_direction(1)[0], head_y + (i+1)*self._get_velocity_for_direction(1)[1]))
        for i in range(self.visibility_range):
            view.append((head_x + (i+1)*self._get_velocity_for_direction(2)[0], head_y + (i+1)*self._get_velocity_for_direction(2)[1]))
        for i in range(self.visibility_range):
            view.append((head_x + (i+1)*self._get_velocity_for_direction(3)[0], head_y + (i+1)*self._get_velocity_for_direction(3)[1]))

        return view

    def _determine_tile_type(self, x, y):
        if self._check_in_snake((x,y)):
            return 2
        if self._check_pos_has_food((x,y)):
            return 3
        if self._check_pos_is_wall((x, y)):
            return 1

        return 0

    def _get_velocity_for_direction(self, direction):
        if direction == 0:
            return [1, 0]
        if direction == 1:
            return [-1, 0]
        if direction == 2:
            return [0, 1]
        if direction == 3:
            return [0, -1]

        raise ValueError('Direction is invalid: '+ str(direction))

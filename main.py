class SmartAgent:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.q_table = {}

    def initialize_q_table(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.q_table[(x, y)] = {'up': 0, 'down': 0, 'left': 0, 'right': 0}

    def choose_action(self, state, epsilon):
        if state not in self.q_table:
            self.q_table[state] = {'up': 0, 'down': 0, 'left': 0, 'right': 0}

        if epsilon > 0:
            import random
            return random.choice(['up', 'down', 'left', 'right'])

        max_q_value = max(self.q_table[state].values())
        valid_actions = [action for action, q_value in self.q_table[state].items() if q_value == max_q_value]
        return random.choice(valid_actions)

    def update_q_table(self, state, action, next_state, reward, alpha, gamma):
        q_value = self.q_table[state][action]
        next_q_value = max(self.q_table[next_state].values())
        self.q_table[state][action] = (1 - alpha) * q_value + alpha * (reward + gamma * next_q_value)

    def train(self, grid_size, epsilon, alpha, gamma, num_episodes):
        self.grid_size = grid_size
        self.initialize_q_table()

        for _ in range(num_episodes):
            state = (0, 0)
            done = False
            rewards = 0

            while not done:
                action = self.choose_action(state, epsilon)
                next_state = self.get_next_state(state, action)

                if next_state == (grid_size - 1, grid_size - 1):
                    reward = 10
                    done = True
                else:
                    reward = -1

                self.update_q_table(state, action, next_state, reward, alpha, gamma)
                state = next_state
                rewards += reward

        return self.q_table

    def get_next_state(self, state, action):
        x, y = state

        if action == 'up':
            x = max(0, x - 1)
        elif action == 'down':
            x = min(self.grid_size - 1, x + 1)
        elif action == 'left':
            y = max(0, y - 1)
        elif action == 'right':
            y = min(self.grid_size - 1, y + 1)

        return (x, y)


agent = SmartAgent(5)
q_table = agent.train(5, 0.1, 0.1, 0.9, 1000)
from tqdm import tqdm


class TrainArgs:

    def __init__(self,
                 train: bool,
                 train_steps: int,
                 max_train_steps: int,
                 pbar: tqdm):
        self.train = train
        self.train_steps = train_steps
        self.max_train_steps = max_train_steps
        self.pbar = pbar
        self.ai_wins = 0

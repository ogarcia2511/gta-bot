import numpy as np 
from alexnet import alexnet

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 8


if __name__ == "__main__":
    name = "gta-bot.model"

    model = alexnet(WIDTH, HEIGHT, LR)

    for i in range(EPOCHS):
        data = np.load('./training/train-1.npy'.format(j), allow_pickle=True) # enter a valid training filename once created
        
        # data = np.load('./training/train-1.npy', allow_pickle=True)
        train_data = data[:-250]
        test_data = data [-250:]

        train_x = np.array([i[0] for i in train_data]).reshape(-1, WIDTH, HEIGHT, 1)
        train_y = [i[1] for i in train_data]

        test_x = np.array([i[0] for i in test_data]).reshape(-1, WIDTH, HEIGHT, 1)
        test_y = [i[1] for i in test_data]

        model.fit({'input': train_x}, {'targets': train_y}, n_epoch=EPOCHS, validation_set=({'input': test_x}, {'targets': test_y}), 
        snapshot_step=500, show_metric=True, run_id=name)

        model.save(name)
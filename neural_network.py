import tensorflow as tf
import numpy as np
from numpy import random

##Fitte neuronales Netz. Will keine große Lookup Tabelle speichern. Breche diese runter auf wenige Parameter, diese speichern. 
def fit_neural_network(boards, results, shape):
    # split in train and test - dummy split - we basically want to fit just a simpler function than a lookup
    train_fraction = 1
    split_position = int(results.__len__()*train_fraction)

    train_labels = results[:split_position]
    # test_labels = results[split_position:]
    # test_labels = results[split_position:, :]
    train_examples = boards[:split_position, :]
    # test_examples = boards[split_position:, :]

    train_dataset = tf.data.Dataset.from_tensor_slices(
        (train_examples, train_labels))
    # test_dataset = tf.data.Dataset.from_tensor_slices(
    #   (test_examples, test_labels))

    BATCH_SIZE = 32
    SHUFFLE_BUFFER_SIZE = 100

    train_dataset = train_dataset.shuffle(
        SHUFFLE_BUFFER_SIZE).batch(BATCH_SIZE)
    # test_dataset = test_dataset.batch(BATCH_SIZE)

    model = tf.keras.Sequential([
        # tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(np.prod(shape), activation='relu'),
        tf.keras.layers.Dense(np.prod(shape)*3, activation='relu'),
        tf.keras.layers.Dense(np.prod(shape)*3, activation='relu'),
        #tf.keras.layers.Dense(np.prod(shape)*3, activation='relu'),
        # tf.keras.layers.Dense(np.prod(shape)*3, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy',
                  optimizer=tf.keras.optimizers.Adam(),
                  metrics=['accuracy'])

    model.fit(train_dataset, epochs=1500)

    # model.evaluate(test_dataset)

    model.save('neural_network_width_' +
               str(shape[0]) + '_height_' + str(shape[1]) + '.h5')


class NeuralNetworkPlayer():
    def __init__(self, shape):
        self.model = tf.keras.models.load_model('neural_network_width_' +
                                                str(shape[0]) + '_height_' + str(shape[1]) + '.h5', custom_objects=None, compile=True
                                                )

    def place(self, board, player):
        moves = []
        boards = []
        sign = 1 if board.move_count % 2 == 0 else -1
        for move in np.arange(board.BOARD_WIDTH):
            if board.place(move, player):
                moves.append(move)
                boards.append((board.board*sign).flatten())
                board.undo(move)
        boards = np.vstack(boards)
        p = self.model.predict(boards)
        p *= sign
        moves = np.vstack(moves)
        moves = moves[p == max(p)]
        random.shuffle(moves)
        move = moves[0]
        board.place(move, player)

        return move

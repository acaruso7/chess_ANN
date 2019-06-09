import tensorflow as tf
import tensorflow.keras as keras


def get_model():
    return keras.Sequential([
        keras.layers.Dense(2048, input_dim=768, activation=tf.nn.elu),
        keras.layers.Dense(2048, activation=tf.nn.elu),
        keras.layers.Dense(2048, activation=tf.nn.elu),
        keras.layers.Dense(1)
    ])

prediction_model = get_model()
prediction_model.load_weights('model_weights.h5')

# import cgi, cgitb 
# cgitb.enable() 

# board = cgi.FieldStorage()

# print(board)


# board_scores = prediction_model.predict()
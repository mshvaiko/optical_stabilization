#!/usr/bin/env python
# docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

import pika
import cv2
import bright_spot_tracker as bst
import orb_tracker as ot

# Define the camera index
VIDEO_SOURCE = 0

# Define the RabbitMQ host and queue
RABBIT_MQ_HOST = 'localhost'
RABBIT_MQ_QUEUE = 'drone_pixel_coordinates'
rabbit_mq_connection = None
rabbit_mq_channel = None

def init_rabbit_mq():
    global rabbit_mq_connection, rabbit_mq_channel
    if (RABBIT_MQ_HOST is None):
        print("Error: RabbitMQ host is not defined.")
        exit()

    # Create a connection to the RabbitMQ server, setup the channel and queue
    try:
        rabbit_mq_connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_MQ_HOST))
        rabbit_mq_channel = rabbit_mq_connection.channel()
        rabbit_mq_channel.queue_declare(RABBIT_MQ_QUEUE)
    except Exception as err:
        print(f"Error: Could not connect to RabbitMQ server at {RABBIT_MQ_HOST}.")
        print(err)
        exit()

def send_coordinates(coordinates):
    global rabbit_mq_channel
    # Send the coordinates to the RabbitMQ server
    rabbit_mq_channel.basic_publish(exchange='', routing_key=RABBIT_MQ_QUEUE, body=str(coordinates))

def close_rabbit_mq():
    global rabbit_mq_connection
    # Close the RabbitMQ connection
    if rabbit_mq_connection is not None:
        rabbit_mq_connection.close()

def main():
    # Open the camera stream using cv2.VideoCapture
    cap = cv2.VideoCapture(VIDEO_SOURCE)

    # Check if the camera stream was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open camera stream with index {VIDEO_SOURCE}.")
        exit()

    print('Working. To exit press CTRL+C')

    try:
        while True:
            # Capture frame
            ret, frame = cap.read()

            if not ret:
                break
            
            # Create a connection to the RabbitMQ server, setup the channel and queue
            init_rabbit_mq()

            # Coorfinate variables from different rtacking modules
            bst_coordinates, ot_coordinates = None, None

            # Use the bright spot tracker module
            bst_coordinates = bst.process_frame(frame)

            # Use the ORB tracker module
            ot_coordinates = ot.process_frame(frame)

            # Use the coordinates from the module that detected the drone
            coordinates = bst_coordinates or ot_coordinates
            print(f"Drone coordinates: {coordinates}")

            # Send the coordinates to the RabbitMQ server
            send_coordinates(coordinates)
    except KeyboardInterrupt:
        print('Stopped')
    finally:
        # Release the capture and close the RabbitMQ connection
        cap.release()
        close_rabbit_mq()

if __name__ == "__main__":
    main()
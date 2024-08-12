# Drone Optical Stabilization Service

This project implements a Python-based service for optical stabilization of a drone. The service tracks key points in video frames using OpenCV and sends this data through RabbitMQ to subscribers for further processing. This setup is ideal for stabilizing video footage in real-time and can be integrated into broader drone control systems.

## General Description

The optical stabilization service works by analyzing video frames captured by the drone's camera. It detects and tracks key points (such as corners or features) in each frame. The coordinates of these key points are then sent via RabbitMQ to other components of the drone system that may use this data for tasks like stabilization, navigation, or analysis.

### Key Components:
- **OpenCV**: Used for video capture and key point detection.
- **RabbitMQ**: Facilitates message passing between the service and other system components.
- **Python**: The primary language used for scripting and processing.

## Requirements

Make sure you have the following installed before running the service:

- **Python 3.10+**
- **OpenCV**: For image processing and key point detection.
- **RabbitMQ**: For message passing.
- **pika**: The Python client for RabbitMQ.

### Install Dependencies

All necessary Python packages are listed in the `requirements.txt` file. You can install them using pip:

```bash
pip install -r requirements.txt

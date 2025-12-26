
# Chronicle

A generic logging utility built on top of [Rerun](https://rerun.io/) for comprehensive event tracking, visualization, and analysis.

## Overview

Chronicle is a lightweight wrapper around Rerun that provides a structured approach to logging events, metrics, and data streams in your applications. It combines traditional text-based logging with rich visual logging capabilities, making it easier to debug, monitor, and analyze complex systems.

## Features

- **Unified Logging Interface**: Simple API for logging events, metrics, and structured data
- **Visual Logging**: Leverage Rerun's visualization capabilities for images, point clouds, tensors, and more
- **Hierarchical Organization**: Organize logs with entity paths for better structure and filtering
- **Multi-format Support**: Log text, numerical data, images, 3D data, and custom data types
- **Timeline Management**: Track events across multiple timelines and sequences
- **Flexible Configuration**: Easy setup with customizable logging levels and output options

## Installation

```bash
pip install rerun-sdk
```

Then install chronicle:

```bash
pip install -e .
```

## Quick Start

```python
from chronicle import Logger

# Initialize the logger
logger = Logger(application_id="my_app")

# Log simple messages
logger.info("Application started")
logger.warning("Configuration file not found, using defaults")

# Log numerical data
logger.log_scalar("metrics/accuracy", 0.95, step=100)

# Log images
logger.log_image("camera/frame", image_array)

# Log structured data
logger.log_dict("config", {"batch_size": 32, "learning_rate": 0.001})
```

## Core Concepts

### Entity Paths

Chronicle uses hierarchical entity paths to organize logged data:

```python
logger.log_scalar("model/loss", loss_value)
logger.log_scalar("model/accuracy", accuracy_value)
logger.log_image("sensors/camera_front", frame)
```

### Timelines

Track events across different timelines:

```python
logger.set_time_sequence("iteration", step)
logger.set_time_seconds("wall_clock", time.time())
```

### Logging Levels

Standard logging levels are supported:

```python
logger.debug("Detailed debugging information")
logger.info("General information")
logger.warning("Warning messages")
logger.error("Error messages")
logger.critical("Critical issues")
```

## Advanced Usage

### Custom Entity Hierarchies

```python
logger = Logger(application_id="my_app", entity_prefix="experiment_01")
logger.log_scalar("metrics/loss", 0.5)  # Logged as "experiment_01/metrics/loss"
```

### Batch Logging

```python
with logger.batch():
    for i in range(100):
        logger.log_scalar("data/value", random.random(), step=i)
```

### Context Management

```python
with logger.context("training/epoch_5"):
    logger.log_scalar("loss", loss)
    logger.log_scalar("accuracy", acc)
```

## Use Cases

- **Machine Learning**: Track training metrics, visualize model predictions, log hyperparameters
- **Robotics**: Log sensor data, visualize trajectories, debug perception pipelines
- **Computer Vision**: Visualize image processing pipelines, track detection results
- **Data Analysis**: Monitor data processing workflows, visualize intermediate results
- **General Development**: Enhanced debugging with visual context

## Configuration

Chronicle can be configured through a configuration file or programmatically:

```python
config = {
    "save_path": "./logs",
    "spawn_viewer": True,
    "default_enabled": True,
}

logger = Logger(application_id="my_app", config=config)
```

## Documentation

For detailed documentation and examples, see the [docs](./docs) directory.

## Requirements

- Python >= 3.12
- rerun-sdk >= 0.15.0

## License

MIT License

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

## Acknowledgments

Built with [Rerun](https://rerun.io/) - An SDK for logging computer vision and robotics data.
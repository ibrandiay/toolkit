import numpy as np
import time
import sys
import os

# Ensure we can import chronicle if running directly from the folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from chronicle import Logger

def main():
    print("Initializing Chronicle Logger...")
    # Initialize implementation
    # We disable spawn_viewer for the test to avoid blocking, but in a real app it might be True
    logger = Logger(application_id="chronicle_test_example", config={"spawn_viewer": True})
    
    print("Logging text messages...")
    logger.info("Starting example usage script")
    logger.warning("This is a sample warning")
    logger.debug("Debug message")
    
    print("Logging sequences and scalars...")
    # Log a sine wave
    for i in range(50):
        val = np.sin(i / 5.0)
        logger.log_scalar("math/sine_wave", val, step=i)
        
    print("Logging an image...")
    # Create a simple gradient image
    width, height = 100, 100
    image = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            image[y, x] = [x * 255 // width, y * 255 // height, 128]
            
    logger.log_image("generated/gradient", image)
    
    print("Logging structured data...")
    config_data = {
        "model_type": "CNN",
        "layers": 5,
        "dropout": 0.5,
        "optimizer": "Adam"
    }
    logger.log_dict("experiment/config", config_data)
    
    print("Testing context manager...")
    with logger.context("validation_phase"):
        # This should log to validation_phase/metrics/accuracy
        logger.log_scalar("metrics/accuracy", 0.88, step=1)
        logger.info("Validation started")
        
    print("Example run finished successfully.")

if __name__ == "__main__":
    main()

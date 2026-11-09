# Hardware Integration

The planned acquisition path uses an ESP32 with a TCS34725 RGB sensor and a
365 nm UV LED to illuminate the optical marker. The current implementation
does not communicate with this hardware. `software/acquisition/esp32_interface.py`
marks the intended integration point, while `sensor_simulator.py` remains the
available source of sample readings.

Before enabling hardware acquisition, implement the sensor transport and
calibrate readings against the existing simulated-data workflow.

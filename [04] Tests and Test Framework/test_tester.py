from tester import Tester

def test_motor(id, speed):
    print(f"Running motor {id} at speed {speed}")

def test_sensor(value):
    print(f"Sensor test with threshold {value}")


t = Tester()

t.add("Motor A slow", test_motor, "A", 20)
t.add("Motor B fast", test_motor, "B", 100)
t.add("Sensor threshold", test_sensor, value=42)

t.run_tests()

# Experiment Monitoring

[![Tests](https://github.com/JPBureik/experiment-monitoring/actions/workflows/tests.yml/badge.svg)](https://github.com/JPBureik/experiment-monitoring/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/JPBureik/experiment-monitoring/branch/master/graph/badge.svg)](https://codecov.io/gh/JPBureik/experiment-monitoring)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

Automated monitoring of lab equipment with time series visualization and e-mail alerts.

![Experiment Monitoring](docs/snapshot.png)

## Features

- Centralized data acquisition from multiple sensor types
- Time series storage in InfluxDB
- Grafana dashboard for visualization
- Automatic e-mail alerts based on user-defined thresholds
- Spike filtering for noisy signals

## Supported Interfaces

| Interface | Example Hardware |
|-----------|------------------|
| Serial | Pfeiffer TPG261 |
| TCP/IP | Arduino Due |
| Analog (via ADC) | Pfeiffer TPG300 |
| SNMP | Eaton UPS |
| Phidgets | Thermocouple module |
| Webcam OCR | Panel displays |

## Installation

```bash
pip install git+https://github.com/JPBureik/experiment-monitoring.git
```

Or for development:

```bash
git clone https://github.com/JPBureik/experiment-monitoring.git
cd experiment-monitoring
pip install -e ".[testing]"
```

## Quick Start

1. Set up your server (see `docs/server_setup.md`)
2. Configure your sensors in `src/expmonitor/config.py`
3. Run the monitoring loop:

```bash
python -m expmonitor.exec
```

Test mode with verbose output (5 iterations):

```bash
python -m expmonitor.exec t v 5
```

## Adding New Sensors

Create a subclass of the abstract `Sensor` class:

```python
from expmonitor.classes.sensor import Sensor

class MySensor(Sensor):
    def __init__(self, descr, ...):
        self.type = 'MyType'
        self.descr = descr
        # ...

    def measure(self):
        # Implement measurement logic
        self.measurement = self.read_value()

    def rcv_vals(self):
        # Return formatted measurement string
        return str(self.measurement)
```

Then instantiate it in `config.py`.

## Repository Structure

```
src/expmonitor/
├── classes/          # Sensor driver classes
│   ├── sensor.py     # Abstract base class
│   ├── adc/          # Arduino ADC drivers
│   └── ups/          # UPS monitoring
├── calibrations/     # Calibration data and scripts
├── utilities/        # Shared utilities (spike filter, etc.)
├── config.py         # Main configuration
└── exec.py           # Entry point
server_setup/         # Deployment scripts and systemd service
tests/                # Test suite
docs/                 # Documentation
```

## License

GPL-3.0

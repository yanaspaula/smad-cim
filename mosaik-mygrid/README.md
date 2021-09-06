# Mosaik MyGrid: A plugin to integrate MyGrid to Mosaik co-simulation framework

Mosaik-MyGrid plugin is a work in progress.

author: Lucas Melo


# Example execution:
Files `start_acom.py`, `collector.py` and `scenario.py` represent an example of an integration between a PADE agent and MyGrid in the Mosaik environment. To execute this example, follow the steps described below. *This example is a work in progress*

1. Create and activate Conda environment with Python 3.7. Substitute {env_name} for the name of your new environment:
```
conda create --name {env_name} python=3.7

conda activate {env_name}
```

2. Install pade-plus:
```
git clone https://github.com/bressanmarcos/pade-plus

python -m pip install ./pade-plus

```

3. Install requirements:
```
pip install -r requirements.txt

```

4. Initialize Communication Agent (ACom) within port 20000:
```
python start_acom.py 20000
```

5. Execute mosaik scenario:
```
python scenario.py
```